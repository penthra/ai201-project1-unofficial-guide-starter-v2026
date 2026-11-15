"""Local wiring checks, not live acceptance trials or model-quality tests.

Run after dependency setup:
    python -m unittest discover -s tests -p 'test_capstone_contracts.py' -v

The real HTTP handler, pipeline, gate, and prompt builder run. Retrieval and
generation are stand-ins: no model downloads, API calls, or Render restarts.
"""

import contextlib
from datetime import datetime
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class HttpContracts(unittest.TestCase):
    def setUp(self):
        config = ModuleType("config")
        for name, value in {
            "CORPUS": "campus_life", "MODEL": "test-model",
            "CACHE_ENABLED": False, "THRESHOLD": 0.6, "TOP_K": 5,
        }.items():
            setattr(config, name, value)
        self.store = ModuleType("store")
        self.store.Result = SimpleNamespace
        self.store.search = Mock(return_value=[SimpleNamespace(
            text="Student permits go on sale in August.",
            source="admin_parking_permits.txt", distance=0.4196,
        )])
        self.store.index_exists = Mock(return_value=True)
        modules = patch.dict(sys.modules, {"config": config, "store": self.store})
        modules.start()
        self.addCleanup(modules.stop)
        self.gate = load_module("gate", "gate.py")
        self.generate = load_module("generate", "generate.py")
        self.generate.answer_from_chunks = Mock(
            return_value="August (admin_parking_permits.txt)."
        )
        self.pipeline = load_module("app", "app.py")
        self.web = load_module("_capstone_contract_serve", "serve.py")
        self.client = self.web.app.test_client()

    def ask(self, payload, expected_status):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            response = self.client.post("/ask", json=payload)
        lines = captured.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        record = json.loads(lines[0])
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(record["http_status"], expected_status)
        self.assertEqual(response.headers["X-Request-ID"], record["request_id"])
        return response.get_json(), record

    def test_answer_and_complete_single_log(self):
        body, record = self.ask({"question": "When are permits sold?"}, 200)
        self.assertEqual(body["answer"], "August (admin_parking_permits.txt).")
        self.assertEqual(body["sources"], ["admin_parking_permits.txt"])
        self.assertFalse(body["refused"])
        required = {
            "timestamp", "request_id", "question", "answer", "model",
            "sources", "best_distance", "refused", "http_status",
            "duration_ms", "error_type",
        }
        self.assertTrue(required <= record.keys())
        self.assertEqual(record["answer"], body["answer"])
        self.assertEqual(record["sources"], body["sources"])
        self.assertIsNotNone(datetime.fromisoformat(record["timestamp"]).tzinfo)
        self.assertGreaterEqual(record["duration_ms"], 0)
        self.assertIsNone(record["error_type"])
        self.generate.answer_from_chunks.assert_called_once()

    def test_invalid_input_then_valid_request(self):
        ids = set()
        for question in (123, True, [], {}, None, "   "):
            with self.subTest(question=question):
                _, record = self.ask({"question": question}, 400)
                self.assertEqual(record["error_type"], "ValidationError")
                self.assertNotIn(record["request_id"], ids)
                ids.add(record["request_id"])
        self.store.search.assert_not_called()
        self.generate.answer_from_chunks.assert_not_called()
        self.ask({"question": "When are permits sold?"}, 200)
        self.generate.answer_from_chunks.assert_called_once()

    def test_gate_refusal_matches_response_and_log_without_generation(self):
        self.store.search.return_value[0].distance = 0.9
        body, record = self.ask({"question": "Unrelated question"}, 200)
        self.assertEqual(body["answer"], self.gate.REFUSAL)
        self.assertTrue(body["refused"])
        self.assertTrue(record["refused"])
        self.assertEqual(record["answer"], body["answer"])
        self.generate.answer_from_chunks.assert_not_called()

    def test_empty_retrieval_also_refuses(self):
        self.store.search.return_value = []
        body, record = self.ask({"question": "No matching chunks"}, 200)
        self.assertEqual(body["answer"], self.gate.REFUSAL)
        self.assertTrue(record["refused"])
        self.generate.answer_from_chunks.assert_not_called()

    def test_pipeline_exception_logged_without_exception_message(self):
        self.store.search.side_effect = RuntimeError("private-test-value")
        _, record = self.ask({"question": "Campus question"}, 500)
        self.assertEqual(record["error_type"], "RuntimeError")
        self.assertNotIn("private-test-value", json.dumps(record))

    def test_health_reports_index_state_without_querying(self):
        for ready in (False, True):
            with self.subTest(ready=ready):
                self.store.index_exists.return_value = ready
                self.assertEqual(
                    self.client.get("/health").get_json()["index_ready"], ready
                )
        self.store.search.assert_not_called()
        self.generate.answer_from_chunks.assert_not_called()


@unittest.skipUnless(os.name == "posix", "Hosted startup uses a POSIX shell")
class StartupContracts(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix="ai201-start-contract-")
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        (self.root / "start.sh").write_bytes((ROOT / "start.sh").read_bytes())
        self.log = self.root / "calls.txt"
        executable = self.root / "python"
        executable.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$CHECK_LOG"\n')
        executable.chmod(0o700)
        self.env = {
            "PATH": str(self.root) + os.pathsep + os.defpath,
            "CHECK_LOG": str(self.log), "GEMINI_API_KEY": "test-placeholder",
            "PORT": "10000",
        }

    def start(self):
        return subprocess.run(
            ["/bin/sh", str(self.root / "start.sh")], env=self.env,
            capture_output=True, text=True,
        )

    def test_missing_build_fails_explicitly(self):
        result = self.start()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing built index", result.stderr)
        self.assertFalse(self.log.exists())

    def test_repeated_start_reuses_artifact_and_binds_host_port(self):
        (self.root / "chroma_db").mkdir()
        # This checks shell wiring only, not SQLite/Chroma persistence itself.
        (self.root / "chroma_db/chroma.sqlite3").touch()
        for _ in range(2):
            self.assertEqual(self.start().returncode, 0)
        calls = self.log.read_text().splitlines()
        self.assertEqual(len(calls), 2)
        for call in calls:
            self.assertIn("-m gunicorn --workers 1", call)
            self.assertIn("0.0.0.0:10000", call)
            self.assertIn("serve:app", call)
            self.assertNotIn("app.py", call)


if __name__ == "__main__":
    unittest.main()

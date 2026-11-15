"""Execute one hosted trial after the user confirms its separate restart.

No restart/deploy actions, automated retries, or final acceptance scoring.
See protocol.md before use. Completed evidence is never overwritten.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import time
import urllib.error
import urllib.request


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def save_json(path, value):
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def send(origin, trial, step, criteria, condition, output, commands, payload=None):
    """Save actual request command, HTTP response, and client timing."""
    method = "GET" if payload is None else "POST"
    url = origin + ("/health" if payload is None else "/ask")
    command = ["curl", "--max-time", "55", "--silent", "--show-error",
               "--include", "--request", method, url]
    headers = {}
    body = None
    if payload is not None:
        body = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
        command += ["--header", "Content-Type: application/json",
                    "--data", body.decode()]
    command_text = shlex.join(command)
    with commands.open("a", encoding="utf-8") as handle:
        handle.write(f"# Trial {trial}: {step}\n{command_text}\n")
        handle.flush()
        os.fsync(handle.fileno())
    record = {
        "record_source": "http_client", "trial": trial, "step": step,
        "criteria": criteria, "condition": condition,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "method": method, "url": url, "request": payload,
        "curl_equivalent": command_text,
    }
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    started = time.perf_counter_ns()
    try:
        try:
            response = urllib.request.urlopen(request, timeout=55)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            raw = response.read()
            elapsed_ns = time.perf_counter_ns() - started
            record.update(
                http_status=response.status,
                request_id=response.headers.get("X-Request-ID"),
                render_request_id=response.headers.get("Rndr-Id"),
                response_date=response.headers.get("Date"),
                response_text=raw.decode("utf-8", errors="replace"),
            )
        try:
            record["response"] = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            record["response"] = None
    except Exception as error:
        elapsed_ns = time.perf_counter_ns() - started
        record.update(http_status=None, request_id=None, response=None,
                      transport_error_type=type(error).__name__)
    record["elapsed_ns"] = elapsed_ns
    record["elapsed_seconds"] = elapsed_ns / 1_000_000_000
    save_json(output, record)
    print(json.dumps(record, ensure_ascii=True), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--restart-confirmed", action="store_true", required=True)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    manifest = json.loads((HERE / "manifest.json").read_text())
    for name, expected in manifest["source_sha256_normalized_newlines"].items():
        content = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(content).hexdigest() != expected:
            raise SystemExit(f"Frozen source/input changed: {name}. Stop and clarify.")
    output = HERE / f"trial_{args.trial}.client.jsonl"
    if output.exists():
        raise SystemExit(f"Evidence already exists: {output}. Do not overwrite trials.")
    output.touch(exist_ok=False)
    commands = HERE / f"trial_{args.trial}.commands.sh"
    save_json(HERE / "restart_attestations.jsonl", {
        "trial": args.trial, "recorded_at": datetime.now(timezone.utc).isoformat(),
        "restart_confirmed_by_user": args.restart_confirmed,
        "deployed_commit_user_attested": manifest["deployed_commit"],
        "dashboard_startup_log_still_required": True,
    })
    manifest["formal_runs_started"] = True
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    def request(step, criteria, condition, payload=None):
        return send(inputs["url"], args.trial, step, criteria, condition,
                    output, commands, payload)

    health = request("restart_health", ["C3"], "after_user_confirmed_restart")
    if not (health.get("response") or {}).get("index_ready"):
        raise SystemExit("Restart readiness did not pass; preserve evidence and clarify before warm trials.")
    first = request("restart_answer_and_excluded_warmup", ["C3"],
                    "first_question_after_restart_excluded_from_C1",
                    {"question": inputs["restart_question"]})
    body = first.get("response") or {}
    if first["http_status"] != 200 or body.get("refused") is not False:
        raise SystemExit("Successful warm-up not established; preserve evidence and clarify.")
    if not first.get("request_id"):
        raise SystemExit("Application request ID missing; stop before uncorrelated trials.")
    for number, entry in enumerate(inputs["in_corpus"], 1):
        request(f"project_question_{number}", ["C1", "C2"], "warm",
                {"question": entry["question"]})
    request("invalid_non_string", ["C4"], "same_running_service",
            inputs["invalid_payload"])
    request("valid_after_invalid", ["C4"], "immediately_after_invalid",
            {"question": inputs["recovery_question"]})
    for number, question in enumerate(inputs["out_of_scope"], 1):
        request(f"out_of_scope_{number}", ["C5"], "warm", {"question": question})
    print(f"Trial {args.trial} requests saved. Export matching server logs and restart evidence; no final verdict yet.", flush=True)


if __name__ == "__main__":
    main()

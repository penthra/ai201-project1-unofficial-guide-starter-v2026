#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP.

    python serve.py                          run it locally on port 5000
    gunicorn serve:app                       run it the way a host runs it

Nothing new happens in this file. It is a wrapper: a request comes in, it
hands the question to `app.py::ask_pipeline` — the exact function the command
line uses — and hands the answer back as JSON. Retrieval, the relevance gate
and the grounded prompt all still live where they lived. If you change how
your system answers, you change it in those files and this one follows.

Two routes:

    POST /ask       {"question": "..."} in, the answer and its sources out
    GET  /health    is the service up, and is there an index to search

Why this exists: `app.py` runs once and exits, which is fine on your laptop
and impossible to deploy. A hosted service has to stay up and wait for
requests. This is the smallest thing that does that.

Each POST /ask emits one structured JSON completion record to stdout,
including validation failures, gate refusals, and handled pipeline errors.
X-Request-ID connects the response to its record in Render's Logs tab.
"""

import json
import os
import time
from datetime import datetime, timezone
from uuid import uuid4

from flask import Flask, g, jsonify, request

import config

app = Flask(__name__)


@app.before_request
def start_ask_log():
    if request.path == "/ask" and request.method == "POST":
        g.ask_started = time.perf_counter()
        g.ask_timestamp = datetime.now(timezone.utc).isoformat()
        g.ask_request_id = str(uuid4())


@app.after_request
def finish_ask_log(response):
    if not hasattr(g, "ask_request_id"):
        return response

    payload = request.get_json(silent=True)
    question = payload.get("question") if isinstance(payload, dict) else None
    question = question.strip() if isinstance(question, str) else None
    outcome = response.get_json(silent=True)
    outcome = outcome if isinstance(outcome, dict) else {}
    error_type = getattr(g, "ask_error_type", None)
    if error_type is None and response.status_code >= 400:
        error_type = "ValidationError" if response.status_code == 400 else "HTTPError"

    record = {
        "event": "rag_request",
        "timestamp": g.ask_timestamp,
        "request_id": g.ask_request_id,
        "question": question,
        "answer": outcome.get("answer"),
        "corpus": config.CORPUS,
        "model": config.MODEL,
        "cache_enabled": config.CACHE_ENABLED,
        "sources": outcome.get("sources", []),
        "best_distance": outcome.get("best_distance"),
        "threshold": outcome.get("threshold", config.THRESHOLD),
        "refused": outcome.get("refused"),
        "http_status": response.status_code,
        "duration_ms": round((time.perf_counter() - g.ask_started) * 1000, 3),
        "error_type": error_type,
    }
    # Exclude environment values, prompts, and exception messages.
    print(json.dumps(record, ensure_ascii=True), flush=True)
    response.headers["X-Request-ID"] = g.ask_request_id
    return response


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?

    Two different questions, and the second one is the one that bites. A
    freshly deployed service answers this route happily while every /ask
    returns "no index" — hosts give you no disk that survives a restart, so
    the index has to be built as part of getting the service up. Checking
    here means you find that out in one request instead of five.
    """
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.post("/ask")
def ask():
    """One question in, one grounded answer out.

    A refused question is a 200, not an error. The gate refusing is your
    system working — it is an answer, and the JSON says so with
    `"refused": true` so whatever calls this can tell the two apart.
    """
    from app import ask_pipeline

    payload = request.get_json(silent=True)
    question = payload.get("question") if isinstance(payload, dict) else None

    if not isinstance(question, str) or not question.strip():
        return (
            jsonify(
                {
                    "error": "Send JSON with a question in it, like "
                    '{"question": "is the housing lottery random?"}'
                }
            ),
            400,
        )

    question = question.strip()

    try:
        outcome = ask_pipeline(question, corpus=config.CORPUS)
    except Exception as exc:  # noqa: BLE001 — a reader gets this, not a traceback
        g.ask_error_type = type(exc).__name__
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500

    return jsonify(
        {
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
        }
    )


def main():
    # Hosts tell you which port to listen on through PORT, and they expect you
    # on 0.0.0.0. Binding 127.0.0.1 instead works perfectly on your laptop and
    # then answers nothing at all once deployed, because the host's router
    # can't reach a socket that only accepts connections from inside the
    # container. It is the single most common way a first deploy "succeeds"
    # and is unreachable.
    port = int(os.getenv("PORT", "5000"))

    # Debug mode reloads on save, which is handy, and prints a console that
    # runs arbitrary code, which is not something to leave switched on where
    # strangers can reach it. Off unless you ask for it.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Try it from another terminal:\n")
    print(f"  curl http://localhost:{port}/health")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()

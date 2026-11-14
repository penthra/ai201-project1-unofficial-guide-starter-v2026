#!/bin/sh
# Hosted Linux entry point. Invoke with: sh start.sh
set -eu
cd "$(dirname "$0")"

# Require the host secret before downloading models or building the index.
: "${GEMINI_API_KEY:?Set GEMINI_API_KEY in the host secret environment}"
export AI201_CORPUS="${AI201_CORPUS:-campus_life}"
export PYTHONUNBUFFERED=1
# Include a Python traceback if a native dependency aborts (e.g. SIGILL).
# This identifies the failing call without changing the model or retrieval.
export PYTHONFAULTHANDLER=1

# Rebuild on every start so an empty/ephemeral disk is supported.
# Failure stops startup rather than serving an API without an index.
python app.py --corpus "$AI201_CORPUS" index
exec python -m gunicorn --workers 1 --bind "0.0.0.0:${PORT:-5000}" --timeout 120 serve:app

#!/bin/sh
# Hosted Linux entry point. Invoke with: sh start.sh
set -eu
cd "$(dirname "$0")"

# Require the host secret before starting the question-answering service.
: "${GEMINI_API_KEY:?Set GEMINI_API_KEY in the host secret environment}"
export AI201_CORPUS="${AI201_CORPUS:-campus_life}"
export PYTHONUNBUFFERED=1
# Include a Python traceback if a native dependency aborts (e.g. SIGILL).
# This identifies the failing call without changing the model or retrieval.
export PYTHONFAULTHANDLER=1
export AI201_EMBED_CACHE_DIR="$PWD/.cache/embedding-models"

# The build packages the index; fail clearly if that build step was skipped.
if [ ! -f chroma_db/chroma.sqlite3 ]; then
    echo "Missing built index. Set Render Build Command to: sh build.sh" >&2
    exit 1
fi
exec python -m gunicorn --workers 1 --bind "0.0.0.0:${PORT:-5000}" --timeout 120 serve:app

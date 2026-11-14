#!/bin/sh
# Render build: compile Chroma's native index for a portable CPU target.
set -eu
cd "$(dirname "$0")"

python -m pip install -r requirements-runtime.txt
# Replace any installed/cached wheel compiled for a different machine's CPU.
# --no-deps preserves the versions selected above.
HNSWLIB_NO_NATIVE=1 python -m pip install --force-reinstall --no-cache-dir --no-binary=chroma-hnswlib --no-deps chroma-hnswlib==0.7.6
python -m pip check
# Catch an import-time native crash during build instead of service startup.
python -X faulthandler -c 'import hnswlib; print("hnswlib import OK")'

#!/bin/sh
set -eu

SCRIPT_DIR="/epics/ioc/config"
PYTHON_BIN="${OVERLAY_RND_PYTHON:-/venv/bin/python3}"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

if [ -f "$REQ_FILE" ]; then
  if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
    "$PYTHON_BIN" -m ensurepip --upgrade >/dev/null 2>&1 || true
  fi
  "$PYTHON_BIN" -m pip install --quiet -r "$REQ_FILE"
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/overlay_rnd.py" \
  --camera "$CAM" \
  --prefix "$PREFIX" \
  --pvout "$SCRIPT_DIR/pvlist.txt"

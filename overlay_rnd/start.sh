#!/bin/sh
set -eu

SCRIPT_DIR="/epics/ioc/config"
PYTHON_BIN="${OVERLAY_RND_PYTHON:-/venv/bin/python3}"

exec "$PYTHON_BIN" "$SCRIPT_DIR/overlay_rnd.py" \
  --camera "$CAM" \
  --prefix "$PREFIX"

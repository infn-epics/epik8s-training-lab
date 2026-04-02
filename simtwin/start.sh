#!/bin/sh
set -eu

SCRIPT_DIR="/epics/ioc/config"
CONFIG_FILE="${SIMTWIN_CONFIG:-$SCRIPT_DIR/config.json}"
PVOUT_FILE="${SIMTWIN_PVOUT:-/workdir/simtwin/pvlist.txt}"
PYTHON_BIN="${SIMTWIN_PYTHON:-/venv/bin/python3}"

mkdir -p "$(dirname "$PVOUT_FILE")"

exec "$PYTHON_BIN" "$SCRIPT_DIR/laser_reflection_twin.py" \
  --config "$CONFIG_FILE" \
  --pvout "$PVOUT_FILE"
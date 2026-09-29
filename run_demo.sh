#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
elif [ -f "$HOME/deal-intelligence-agent/venv/bin/activate" ]; then
    source "$HOME/deal-intelligence-agent/venv/bin/activate"
fi

python3 demo.py "$@"

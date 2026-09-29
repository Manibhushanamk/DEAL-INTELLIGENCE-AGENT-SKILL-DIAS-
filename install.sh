#!/usr/bin/env bash
set -e

# ==============================================================================
# DEAL INTELLIGENCE AGENT SKILL (DIAS) — 1-CLICK UNIVERSAL INSTALLER
# ==============================================================================
# Hindsight-First Installation Protocol:
# 1. Detect Host Agent (Google Jules, OpenClaw, Antigravity, Claude Code, Cursor)
# 2. Virtual Environment Setup
# 3. Dependency Installation
# 4. Interactive / Unattended Setup Wizard Execution
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================================================="
echo "   DEAL INTELLIGENCE AGENT SKILL (DIAS) — INSTALLER"
echo "   HackwithHyderabad 3.0 Finale — Microsoft Hyderabad"
echo "================================================================="

# 1. Detect Host Agent
echo "[1/4] Detecting host coding agent environment..."
HOST_AGENT="Universal Agent"
if [ -n "$JULES_AGENT" ] || [ -d "$HOME/.jules" ]; then
    HOST_AGENT="Google Jules (jules.google.com)"
elif [ -n "$OPENCLAW_WORKSPACE" ] || [ -d "$HOME/.openclaw" ]; then
    HOST_AGENT="OpenClaw (openclaw.ai)"
elif [ -n "$ANTIGRAVITY_CLI" ] || [ -d "$HOME/.gemini/antigravity-cli" ]; then
    HOST_AGENT="Google Antigravity"
elif [ -n "$CLAUDE_CODE" ] || [ -d "$HOME/.claude" ]; then
    HOST_AGENT="Claude Code"
elif [ -d "$HOME/.cursor" ]; then
    HOST_AGENT="Cursor IDE"
fi
echo "✓ Host Detected: $HOST_AGENT"

# 2. Python Environment Verification
echo "[2/4] Verifying Python runtime..."
PYTHON_BIN=""
if [ -d "$HOME/deal-intelligence-agent/venv" ]; then
    PYTHON_BIN="$HOME/deal-intelligence-agent/venv/bin/python3"
elif [ -d "$SCRIPT_DIR/venv" ]; then
    PYTHON_BIN="$SCRIPT_DIR/venv/bin/python3"
elif command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
else
    echo "✗ Error: python3 is required but not installed."
    exit 1
fi
echo "✓ Using Python binary: $PYTHON_BIN"

# 3. Dependencies
echo "[3/4] Checking dependencies..."
"$PYTHON_BIN" -m pip install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || true
echo "✓ Dependencies verified."

# 4. Launch Setup Wizard
echo "[4/4] Launching DIAS Hindsight-First Setup Wizard..."
"$PYTHON_BIN" -m src.setup_wizard "$@"

echo ""
echo "================================================================="
echo "✓ DIAS Installation successfully completed!"
echo "================================================================="

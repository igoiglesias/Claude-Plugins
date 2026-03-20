#!/usr/bin/env bash
# =============================================================================
# browser-devtools plugin — auto-setup (runs on SessionStart)
#
# Creates a Python venv in $CLAUDE_PLUGIN_DATA and installs deps.
# Only reinstalls when requirements.txt changes (or first run).
# =============================================================================
set -e

ROOT="${CLAUDE_PLUGIN_ROOT}"
DATA="${CLAUDE_PLUGIN_DATA}"

# Ensure data dir exists
mkdir -p "${DATA}"

# --- Compare requirements.txt: skip if unchanged ---
if diff -q "${ROOT}/requirements.txt" "${DATA}/requirements.txt" >/dev/null 2>&1; then
    # Already installed and up to date
    exit 0
fi

# --- Find Python 3.10+ ---
PY=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "[browser-devtools] ERROR: Python 3.10+ not found." >&2
    exit 1
fi

# --- Create venv if missing ---
if [ ! -f "${DATA}/venv/bin/python" ]; then
    echo "[browser-devtools] Creating Python virtual environment..."
    "$PY" -m venv "${DATA}/venv"
fi

# --- Install/update deps ---
echo "[browser-devtools] Installing dependencies..."
"${DATA}/venv/bin/pip" install --quiet --upgrade pip >/dev/null 2>&1
"${DATA}/venv/bin/pip" install --quiet -r "${ROOT}/requirements.txt" >/dev/null 2>&1

if [ $? -eq 0 ]; then
    cp "${ROOT}/requirements.txt" "${DATA}/requirements.txt"
    echo "[browser-devtools] Setup complete."
else
    rm -f "${DATA}/requirements.txt"
    echo "[browser-devtools] ERROR: pip install failed." >&2
    exit 1
fi

# --- Check Chrome/Chromium (informational, non-blocking) ---
CHROME_OK=false
for cmd in google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$cmd" >/dev/null 2>&1; then
        CHROME_OK=true
        break
    fi
done

if [ "$CHROME_OK" = false ]; then
    echo "[browser-devtools] WARNING: Chrome/Chromium not found in PATH."
    echo "  Install: sudo apt install chromium-browser  OR  brew install --cask google-chrome"
fi

# --- Check Lighthouse (informational, non-blocking) ---
if ! command -v lighthouse >/dev/null 2>&1; then
    echo "[browser-devtools] NOTE: Lighthouse CLI not found (optional)."
    echo "  Install: npm install -g lighthouse"
fi

exit 0

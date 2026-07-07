#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV_PYTHON="$ROOT/.venv/bin/python"
SYSTEM_PYTHON="$(command -v python3 || true)"
REQUIREMENTS="$ROOT/hooks/agent-bridge/requirements.txt"
LOG_DIR="${TMPDIR:-/tmp}/agent-bridge/agent-mecha"
LOG_FILE="$LOG_DIR/setup.log"
LOCK_DIR="$ROOT/.venv.agent-mecha.lock"

mkdir -p "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" >> "$LOG_FILE"
}

has_webview() {
  local python="$1"
  [ -x "$python" ] || return 1
  "$python" - <<'PY' >/dev/null 2>&1
import webview
PY
}

if has_webview "$VENV_PYTHON"; then
  exit 0
fi

if [ -z "$SYSTEM_PYTHON" ]; then
  log "python3 not found; cannot create .venv"
  exit 0
fi

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  log "another setup process is running; waiting briefly"
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 1
    if has_webview "$VENV_PYTHON"; then
      exit 0
    fi
  done
  log "setup lock still present; continuing without blocking"
  exit 0
fi

cleanup() {
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup EXIT

log "creating .venv and installing agent-bridge dependencies"

if ! "$SYSTEM_PYTHON" -m venv "$ROOT/.venv" >> "$LOG_FILE" 2>&1; then
  log "failed to create .venv"
  exit 0
fi

if ! "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS" >> "$LOG_FILE" 2>&1; then
  log "failed to install requirements from $REQUIREMENTS"
  exit 0
fi

if has_webview "$VENV_PYTHON"; then
  log "agent-bridge dependencies are ready"
else
  log "pywebview still unavailable after install"
fi

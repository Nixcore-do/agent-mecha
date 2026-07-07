#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

bash "$ROOT/hooks/agent-bridge/setup.sh" >/dev/null 2>&1 || true

PYTHON="$ROOT/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON="$(command -v python3)"
fi

exec "$PYTHON" "$ROOT/hooks/agent-bridge/bridge.py" "$@"

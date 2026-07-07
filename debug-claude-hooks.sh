#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export AGENT_BRIDGE_DEBUG=1
exec claude --plugin-dir "$SCRIPT_DIR" --debug hooks

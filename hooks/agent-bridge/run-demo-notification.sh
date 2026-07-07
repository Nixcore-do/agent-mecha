#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

bash hooks/agent-bridge/launch.sh <<'JSON'
{"hook_event_name":"Stop"}
JSON

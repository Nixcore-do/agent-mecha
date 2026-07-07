#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

bash hooks/agent-bridge/launch.sh <<'JSON'
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/test",
    "description": "测试权限弹窗"
  }
}
JSON

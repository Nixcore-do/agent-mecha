#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

bash hooks/agent-bridge/launch.sh <<'JSON'
{
  "hook_event_name": "Elicitation",
  "message": "请选择安装层级：",
  "requested_schema": {
    "type": "object",
    "title": "安装层级",
    "required": ["scope"],
    "properties": {
      "scope": {
        "type": "string",
        "title": "安装层级",
        "enum": ["global", "project"],
        "enumNames": ["global（用户级别）", "project（项目级别）"],
        "enumDescriptions": [
          "安装到 ~/.claude/，所有项目自动生效",
          "安装到当前项目的 .claude/，仅本项目生效"
        ]
      }
    }
  }
}
JSON

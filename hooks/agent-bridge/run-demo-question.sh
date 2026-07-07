#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

bash hooks/agent-bridge/launch.sh <<'JSON'
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "AskUserQuestion",
  "tool_input": {
    "questions": [
      {
        "question": "请选择安装层级",
        "header": "安装范围",
        "options": [
          {"label": "global（用户级别）", "description": "安装到 ~/.claude/，所有项目生效"},
          {"label": "project（项目级别）", "description": "安装到当前项目的 .claude/，仅本项目生效"}
        ],
        "multiSelect": false
      }
    ]
  }
}
JSON

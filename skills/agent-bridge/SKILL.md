---
name: agent-bridge
description: 用于设计、审查或实现 agent bridge 工作流，让 Agent 能与 hooks、外部工具、后台进程或另一个 agent 协作。
---

# Agent Bridge

## 目标

构建 bridge 工作流，让 Agent 能和其他进程或工具交换结构化事件，同时不向用户隐藏控制流。

当前仓库已经包含一套 bridge 实现，位置在 `hooks/agent-bridge/`。

## 检查清单

1. 识别 bridge 参与方：Agent、hook、外部进程、UI、daemon 或远程 agent。
2. 定义事件契约：事件名、请求 payload schema、响应 schema、超时和失败行为。
3. 选择传输方式：stdin/stdout JSON、本地 HTTP、Unix socket、文件投递，或其他明确机制。
4. 定义用户可见的审批点。
5. 将脚本放在 `scripts/agent-bridge/` 下。
6. 将 hook 配置或示例放在 `hooks/agent-bridge/` 下。
7. 用最小成功路径和至少一个失败路径测试 bridge。

## 已有实现入口

- `hooks/agent-bridge/launch.sh`: hook 命令入口。
- `hooks/agent-bridge/bridge.py`: Python 事件分发入口。
- `hooks/agent-bridge/config/agent-bridge.json`: 默认 UI 和行为配置。
- `hooks/agent-bridge/claude-settings.example.json`: Claude Code hook 注册示例。
- `hooks/agent-bridge/tests/`: 不需要 GUI 的单元测试。

## 规则

- 机器边界优先使用结构化 JSON，不使用自由文本。
- bridge 行为必须可审计：记录事件名、决策和错误。
- bridge 不得静默执行破坏性动作。
- 超时和取消行为必须明确。

## 相关 skill

- `agent-brgidge-skins`: 切换 agent-bridge 弹窗皮肤，支持 `default`、`claude`、`codex`。

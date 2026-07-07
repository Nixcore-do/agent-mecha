# Agent Bridge

`agent-bridge` 是 agent 与用户之间的本地交互桥。

它主要做两件事：

1. 当 agent 需要用户注意时发出提示，例如完成、失败或空闲提醒。
2. 当 agent 需要授权、确认、选项选择或表单输入时收集用户反馈。

## 事件路由

当前实现兼容 Claude Code hook 事件。所有支持的事件都通过 `launch.sh` 进入，再由 `bridge.py` 路由到对应处理器。

| Hook 事件 | Tool | 处理器 | 用途 |
| --- | --- | --- | --- |
| `Stop` | n/a | `events.notification` | 显示完成提示 |
| `StopFailure` | n/a | `events.notification` | 显示失败提示 |
| `Notification` | n/a | `events.notification` | 显示通知提示 |
| `PermissionRequest` | `Bash`, `Edit`, `Write` 等 | `events.permission` | 让用户同意或拒绝工具调用 |
| `PermissionRequest` | `AskUserQuestion`, `SendUserMessage` | `events.question` | 收集回答并返回 `updatedInput.answers` |
| `Elicitation` | n/a | `events.elicitation` | 收集表单输入并返回 `action/content` |

未知的 `PermissionRequest` 工具默认放行，避免 bridge 阻塞自己不理解的工具。

## 分层边界

`bridge.py`
: 读取 stdin JSON，加载配置，路由到一个处理器，并输出 JSON。

`core/`
: 共享基础设施：JSON IO、配置加载、运行日志、hook 协议辅助方法和事件路由。

`events/`
: hook 协议处理器。这里理解事件结构，并返回 hook 输出。

`forms/`
: 纯表单转换。这里把 JSON schema 或 `AskUserQuestion.questions[]` 转成字段，再把字段内容转回 `updatedInput.answers`。它不导入 UI 代码。

`ui/`
: 窗口实现。这里展示对话框和 toast，并返回用户动作。它不理解具体 hook 协议。

`web/`
: pywebview 使用的静态资源。

`config/`
: 可调整的 bridge 配置。

## Hook 注册

Claude Code 的 hook 示例配置见：

```text
hooks/agent-bridge/claude-settings.example.json
```

如果把这份配置合并到项目的 `.claude/settings.json`，请确认命令路径能从目标项目根目录访问：

```text
bash hooks/agent-bridge/launch.sh
```

## 运行时文件

日志会写入系统临时目录：

```text
/tmp/agent-bridge/<project-name>/
```

运行时日志、`.pyc` 和 `.DS_Store` 不应提交。

## 验证

运行不需要 GUI 的单元测试：

```bash
env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover hooks/agent-bridge/tests
```

冒烟测试非交互放行路径：

```bash
bash hooks/agent-bridge/launch.sh <<'JSON'
{"hook_event_name":"PermissionRequest","tool_name":"UnknownTool","tool_input":{"x":1}}
JSON
```

手动 GUI demo：

```bash
bash hooks/agent-bridge/run-demo-notification.sh
bash hooks/agent-bridge/run-demo-permission.sh
bash hooks/agent-bridge/run-demo-question.sh
bash hooks/agent-bridge/run-demo-elicitation.sh
```

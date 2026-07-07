# Agent Mecha

Agent Mecha 是 Agent 的工程外骨骼。

当前版本只聚焦一个能力：`agent-bridge`。它用于帮助 Agent 与 hooks、外部工具、后台进程、UI 或另一个 agent 通过结构化事件协作。

## 项目结构

```text
agent-mecha/
  .claude-plugin/
    plugin.json
    marketplace.json
  .codex-plugin/
    plugin.json
  skills/
    agent-bridge/
      SKILL.md
  hooks/
    agent-bridge/
      bridge.py
      launch.sh
      config/
      core/
      events/
      forms/
      ui/
      web/
      tests/
    README.md
  scripts/
    agent-bridge/
    README.md
  assets/
    README.md
  docs/
    architecture.md
  tests/
    README.md
```

## 技能能力

- `agent-bridge`: 设计和接入 agent bridge 工作流。

后续如果新增能力，再按同样结构添加新的 `skills/<capability>/SKILL.md`。

## 当前实现

`hooks/agent-bridge/` 已集成一套可运行的本地 bridge：

- `launch.sh`: hook 入口脚本。
- `bridge.py`: 读取 stdin JSON，加载配置，并路由事件。
- `events/`: 处理通知、权限、问题和表单事件。
- `forms/`: 把问题或 JSON schema 转成 UI 字段。
- `ui/` 和 `web/`: 展示权限弹窗、表单和 toast。
- `config/agent-bridge.json`: 默认文案和窗口配置。
- `claude-settings.example.json`: Claude Code hook 注册示例。

## Bridge 依赖

弹窗 UI 依赖 `pywebview`。

通过 `/plugin install` 安装插件时，Claude 只会安装插件文件和注册 hooks/skills，不会执行 `pip install`。Agent Mecha 通过 `SessionStart` hook 做运行时自举：首次启动时会异步创建 `.venv` 并安装 `hooks/agent-bridge/requirements.txt`。

也可以手动安装依赖：

```bash
cd <path-to>/agent-mecha
./setup-agent-bridge.sh
```

`launch.sh` 会优先使用插件根目录下的 `.venv`。如果没有安装 `pywebview`，hook 会触发，但权限弹窗、表单和 toast 无法显示；错误会写入 bridge 日志。

## 安装说明

### 开发直连

Claude Code 本地开发时，可以直接指定插件目录，不需要先安装。

如果当前目录是 `agent-mecha` 的上一级目录：

```bash
claude --plugin-dir ./agent-mecha
```

如果当前目录是 `agent-mecha` 根目录：

```bash
claude --plugin-dir .
```

也可以从任意目录运行项目自带启动脚本：

```bash
<path-to>/agent-mecha/start-claude-plugin.sh
```

### 本地安装

`/plugin install` 不能直接安装本地路径。需要先把本地目录添加为 marketplace，再从该 marketplace 安装插件。

在 Claude Code 会话里运行：

```text
/plugin marketplace add <path-to>/agent-mecha
/plugin install agent-mecha@agent-mecha
```

等价的终端命令：

```bash
claude plugin marketplace add <path-to>/agent-mecha
claude plugin install agent-mecha@agent-mecha
```

安装后重新启动 Claude Code，让 hooks 和 skills 在新会话中生效。

确认 Claude 已识别插件组件：

```bash
claude --plugin-dir ./agent-mecha plugin details agent-mecha
```

也可以直接运行项目自带脚本：

```bash
<path-to>/agent-mecha/check-claude-plugin.sh
```

输出里应该能看到：

```text
Hooks (...) SessionStart, Stop, StopFailure, Elicitation, PermissionRequest
```

如果是通过 `/plugin install` 安装的版本，也可以这样查看：

```text
/plugin details agent-mecha
```

或使用终端命令：

```bash
claude plugin details agent-mecha
```

注意：这些 hook 不是启动时都会触发。`Stop` 在 agent 回复结束时触发，`PermissionRequest` 只在需要权限审批时触发，`Elicitation` 只在需要表单输入时触发。调试 hook 时可以启动：

```bash
claude --plugin-dir ./agent-mecha --debug hooks
```

也可以直接运行项目自带脚本：

```bash
<path-to>/agent-mecha/debug-claude-hooks.sh
```

如果要同时打开 bridge 自身的日志：

```bash
AGENT_BRIDGE_DEBUG=1 claude --plugin-dir ./agent-mecha --debug hooks
```

bridge 日志位于系统临时目录。macOS 上通常类似：

```text
/var/folders/.../T/agent-bridge/agent-mecha/
```

### 卸载

在 Claude Code 会话里卸载插件：

```text
/plugin uninstall agent-mecha
```

如果不再需要这个 marketplace，也可以移除 marketplace：

```text
/plugin marketplace remove agent-mecha
```

等价的终端命令：

```bash
claude plugin uninstall agent-mecha
claude plugin marketplace remove agent-mecha
```

卸载只会移除 Claude Code 已安装的插件和 marketplace 配置，不会删除本地源码目录 `<path-to>/agent-mecha`。

如果只想清理运行时依赖，可以删除本地虚拟环境，下一次启动时会重新自举安装：

```bash
rm -rf <path-to>/agent-mecha/.venv
```

本地 Codex 开发时，插件入口由 `.codex-plugin/plugin.json` 描述，技能目录来自 `./skills/`。

发布前，请在 `.claude-plugin/plugin.json` 和 `.codex-plugin/plugin.json` 中补充最终的作者、仓库、主页、隐私政策和服务条款信息。

## 开发说明

新增能力时，建议保持以下结构：

```text
skills/<capability>/SKILL.md
hooks/<capability>/
scripts/<capability>/
docs/<capability>.md
tests/<capability>/
```

先定义技能和接口契约，再实现脚本或 hook。

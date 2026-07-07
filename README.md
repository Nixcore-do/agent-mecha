# Agent Mecha

Agent Mecha 是 Agent 的工程外骨骼。

当前版本只聚焦一个能力：`agent-bridge`。它用于帮助 Agent 与 hooks、外部工具、后台进程、UI 或另一个 agent 通过结构化事件协作。

## 项目结构

```text
agent-mecha/
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

## 安装说明

本地 Codex 开发时，插件入口由 `.codex-plugin/plugin.json` 描述，技能目录来自 `./skills/`。

发布前，请在 `.codex-plugin/plugin.json` 中补充最终的作者、仓库、主页、隐私政策和服务条款信息。

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

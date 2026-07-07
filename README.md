# Agent Mecha

Agent Mecha 是 Agent CLI 的工程外骨骼。

Agent Mecha is an engineering exoskeleton for agent CLIs.

它用于沉淀可复用的 agent CLI 扩展能力，例如 hook runner、agent bridge、权限门禁、通知路由和本地自动化工作流。

It packages reusable skills and project structure for building agent CLI extensions such as hook runners, agent bridge workflows, permission gates, notification routing, and local automation.

## Structure

## 项目结构

```text
agent-mecha/
  .codex-plugin/
    plugin.json
  skills/
    agent-mecha/
      SKILL.md
    agent-bridge/
      SKILL.md
    hook-runner/
      SKILL.md
    permission-gate/
      SKILL.md
    notification-router/
      SKILL.md
  hooks/
    agent-bridge/
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

## Skills

## 技能能力

- `agent-mecha`: 项目总览和能力路由 skill。
  Project overview and routing skill.
- `agent-bridge`: 设计和接入 agent bridge 工作流。
  Design and integrate agent bridge workflows.
- `hook-runner`: 定义 CLI hook 生命周期和执行契约。
  Define CLI hook lifecycle and execution contracts.
- `permission-gate`: 建模 agent 行为的审批流和策略门禁。
  Model approval and policy gates for agent actions.
- `notification-router`: 设计 agent 工作流事件通知。
  Design event notifications for agent workflows.

## Install Direction

## 安装说明

本地 Codex 开发时，插件入口由 `.codex-plugin/plugin.json` 描述，技能目录来自 `./skills/`。

For local Codex development, this plugin is described by `.codex-plugin/plugin.json` and exposes skills from `./skills/`.

发布前，请在 `.codex-plugin/plugin.json` 中补充最终的作者、仓库、主页、隐私政策和服务条款信息。

Before publishing, add your final author, repository, homepage, privacy, and terms metadata to `.codex-plugin/plugin.json`.

## Development Notes

## 开发说明

新增能力时，建议保持以下结构：

When adding a new capability, keep this structure:

```text
skills/<capability>/SKILL.md
hooks/<capability>/
scripts/<capability>/
docs/<capability>.md
tests/<capability>/
```

先定义 skill 和接口契约，再实现脚本或 hook。

Define the skill and contract first, then implement scripts or hooks.

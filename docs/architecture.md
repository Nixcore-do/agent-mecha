# Agent Mecha 架构

Agent Mecha 按独立能力组织。当前只有一个能力：`agent-bridge`。

## 组件

- `skills/agent-bridge/SKILL.md` 定义 agent 什么时候、如何使用 agent bridge 能力。
- Hooks 定义生命周期接入点。
- Scripts 提供 hook 和本地工作流可调用的命令实现。
- Docs 记录跨实现需要保持稳定的契约。

## 能力目录

当前能力遵循这个结构：

```text
skills/agent-bridge/SKILL.md
hooks/agent-bridge/
scripts/agent-bridge/
docs/architecture.md
tests/
```

先写技能和契约文档，再实现脚本。未来新增能力时，再复制这个结构扩展。

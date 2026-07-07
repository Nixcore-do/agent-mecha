# Agent Mecha

Agent Mecha 是面向 Agent 的工程化实用插件。

## 功能概览

- **agent-bridge 本地交互桥**：在 Agent 需要用户注意、确认、授权或输入时，弹出本地 UI 或通知。

- **插件化安装**：提供标准插件入口，安装后可通过 skills 和 hooks 复用这些能力。

## 支持 Agent

- Claude Code
- Codex

本页只说明如何从 GitHub 安装。

## Codex 安装

在终端运行：

```bash
codex plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
codex plugin add agent-mecha@agent-mecha
```

安装后重启 Codex，让插件的 skills 和 hooks 生效。

确认安装结果：

```bash
codex plugin list
```

## Claude Code 安装

在 Claude Code 会话里运行：

```text
/plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
/plugin install agent-mecha@agent-mecha
```

也可以在终端运行：

```bash
claude plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
claude plugin install agent-mecha@agent-mecha
```

安装后重启 Claude Code，让插件的 skills 和 hooks 生效。

确认安装结果：

```text
/plugin details agent-mecha
```

或在终端运行：

```bash
claude plugin details agent-mecha
```

# Agent Mecha

Agent Mecha 是面向 Agent 的工程化实用插件。

## 功能概览

- **agent-bridge 本地交互桥**：在 Agent 需要用户注意、确认、授权或输入时，弹出本地 UI 或通知。

- **agent-bridge 皮肤切换**：内置 `default`、`claude`、`codex` 三套弹窗皮肤，可通过 `agent-brgidge-skins` skill 或脚本切换。

- **插件化安装**：提供标准插件入口，安装后可通过 skills 和 hooks 复用这些能力。

## 支持 Agent

- Claude Code
- Codex

本页说明如何从 GitHub 安装和卸载。

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

## 卸载

### Codex 卸载

在终端运行：

```bash
codex plugin remove agent-mecha@agent-mecha
```

如果不再需要这个 marketplace 源，可以继续移除：

```bash
codex plugin marketplace list
codex plugin marketplace remove agent-mecha
```

`agent-mecha@agent-mecha` 的格式是 `插件名@marketplace 名`。如果先用 `codex plugin marketplace list` 看到的 marketplace 名不是 `agent-mecha`，请替换为实际名称。

卸载后重启 Codex，让插件的 skills 和 hooks 停止生效。

确认卸载结果：

```bash
codex plugin list
```

### Claude Code 卸载

在 Claude Code 会话里运行：

```text
/plugin uninstall agent-mecha@agent-mecha
```

如果不再需要这个 marketplace 源，可以继续移除：

```text
/plugin marketplace list
/plugin marketplace remove agent-mecha
```

也可以在终端运行：

```bash
claude plugin uninstall agent-mecha@agent-mecha
claude plugin marketplace list
claude plugin marketplace remove agent-mecha
```

`agent-mecha@agent-mecha` 的格式是 `插件名@marketplace 名`。如果先用 `/plugin marketplace list` 或 `claude plugin marketplace list` 看到的 marketplace 名不是 `agent-mecha`，请替换为实际名称。

卸载后运行 `/reload-plugins`，或重启 Claude Code，让插件的 skills 和 hooks 停止生效。

确认卸载结果：

```text
/plugin list
```

或在终端运行：

```bash
claude plugin list
```

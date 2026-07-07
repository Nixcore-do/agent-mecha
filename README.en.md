# Agent Mecha

Agent Mecha is a practical engineering plugin for agents.

## Feature Overview

- **agent-bridge local interaction bridge**: shows local UI or notifications when an agent needs user attention, confirmation, authorization, or input.

- **Plugin installation**: provides standard plugin entry points so these capabilities can be reused through skills and hooks after installation.

## Supported Agents

- Claude Code
- Codex

This page covers installing and uninstalling from GitHub.

## Codex Installation

Run in your terminal:

```bash
codex plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
codex plugin add agent-mecha@agent-mecha
```

Restart Codex after installation so the plugin skills and hooks take effect.

Confirm the installation:

```bash
codex plugin list
```

## Claude Code Installation

Run inside a Claude Code session:

```text
/plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
/plugin install agent-mecha@agent-mecha
```

Or run in your terminal:

```bash
claude plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
claude plugin install agent-mecha@agent-mecha
```

Restart Claude Code after installation so the plugin skills and hooks take effect.

Confirm the installation:

```text
/plugin details agent-mecha
```

Or run in your terminal:

```bash
claude plugin details agent-mecha
```

## Uninstall

### Codex Uninstall

Run in your terminal:

```bash
codex plugin remove agent-mecha@agent-mecha
```

If you no longer need this marketplace source, remove it too:

```bash
codex plugin marketplace list
codex plugin marketplace remove agent-mecha
```

`agent-mecha@agent-mecha` means `plugin-name@marketplace-name`. If `codex plugin marketplace list` shows a different marketplace name, use that name instead.

Restart Codex after uninstalling so the plugin skills and hooks stop taking effect.

Confirm the result:

```bash
codex plugin list
```

### Claude Code Uninstall

Run inside a Claude Code session:

```text
/plugin uninstall agent-mecha@agent-mecha
```

If you no longer need this marketplace source, remove it too:

```text
/plugin marketplace list
/plugin marketplace remove agent-mecha
```

Or run in your terminal:

```bash
claude plugin uninstall agent-mecha@agent-mecha
claude plugin marketplace list
claude plugin marketplace remove agent-mecha
```

`agent-mecha@agent-mecha` means `plugin-name@marketplace-name`. If `/plugin marketplace list` or `claude plugin marketplace list` shows a different marketplace name, use that name instead.

Run `/reload-plugins` after uninstalling, or restart Claude Code, so the plugin skills and hooks stop taking effect.

Confirm the result:

```text
/plugin list
```

Or run in your terminal:

```bash
claude plugin list
```

# Agent Mecha

Agent Mecha is a practical engineering plugin for agents.

## Feature Overview

- **agent-bridge local interaction bridge**: shows local UI or notifications when an agent needs user attention, confirmation, authorization, or input.

- **Plugin installation**: provides standard plugin entry points so these capabilities can be reused through skills and hooks after installation.

## Supported Agents

- Claude Code
- Codex

This page only covers installing from GitHub.

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

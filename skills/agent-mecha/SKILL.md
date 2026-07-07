---
name: agent-mecha
description: Use when working on Agent Mecha itself or deciding which Agent Mecha capability applies to an agent CLI extension task.
---

# Agent Mecha

Agent Mecha is an engineering exoskeleton for agent CLIs. It organizes reusable capabilities for hooks, bridge workflows, permission gates, notifications, and automation.

## Route The Work

- Use `agent-bridge` when the task connects an agent CLI to another process, UI, daemon, or external workflow.
- Use `hook-runner` when the task defines lifecycle events, hook payloads, command execution, or hook installation.
- Use `permission-gate` when the task involves approvals, policy decisions, restricted actions, or user confirmation.
- Use `notification-router` when the task emits, formats, filters, or delivers workflow events.

## Project Rules

- Keep each capability in its own skill directory.
- Put reusable command implementations under `scripts/<capability>/`.
- Put runtime hook examples and hook configs under `hooks/<capability>/`.
- Document contracts before adding implementation code.
- Verify generated plugin metadata before publishing.

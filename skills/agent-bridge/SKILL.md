---
name: agent-bridge
description: Use when designing, reviewing, or implementing an agent bridge workflow that lets an agent CLI coordinate with hooks, external tools, background processes, or another agent.
---

# Agent Bridge

## Goal

Build bridge workflows that let an agent CLI exchange structured events with another process or tool without hiding control flow from the user.

## Checklist

1. Identify the bridge participants: agent CLI, hook, external process, UI, daemon, or remote agent.
2. Define the event contract: event name, payload schema, response schema, timeout, and failure behavior.
3. Choose the transport: stdin/stdout JSON, local HTTP, Unix socket, file drop, or another explicit mechanism.
4. Define user-visible approval points.
5. Add scripts under `scripts/agent-bridge/`.
6. Add hook config or examples under `hooks/agent-bridge/`.
7. Test the bridge with a minimal happy path and at least one failure path.

## Rules

- Prefer structured JSON over free-form text for machine boundaries.
- Keep bridge actions auditable: log event names, decisions, and errors.
- Do not let a bridge silently execute destructive actions.
- Make timeouts and cancellation behavior explicit.

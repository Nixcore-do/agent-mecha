---
name: hook-runner
description: Use when defining agent CLI hook lifecycles, hook configuration, hook command execution, or hook testing.
---

# Hook Runner

## Goal

Create predictable hook workflows for agent CLI lifecycle events.

## Hook Design Checklist

1. Name the lifecycle event.
2. Define when the hook runs.
3. Define input payload fields.
4. Define output payload fields.
5. Specify whether the hook is blocking or async.
6. Specify timeout and retry behavior.
7. Provide a local test command.

## Rules

- Hooks should be deterministic when possible.
- Use explicit exit codes and structured output.
- Keep side effects visible in logs or returned payloads.
- Put reusable hook commands in `scripts/`.

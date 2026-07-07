# Agent Mecha Architecture

Agent Mecha is organized around independent capabilities.

## Components

- Skills define when and how the agent should use a capability.
- Hooks define lifecycle integration points.
- Scripts provide executable helpers for hooks and local workflows.
- Docs capture contracts that should stay stable across implementations.

## Capability Layout

Each capability should follow this pattern:

```text
skills/<capability>/SKILL.md
hooks/<capability>/
scripts/<capability>/
docs/<capability>.md
tests/<capability>/
```

Start with the skill and contract docs before implementing scripts.

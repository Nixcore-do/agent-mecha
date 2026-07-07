---
name: permission-gate
description: Use when modeling approval flows, safety policies, restricted command decisions, or user confirmation gates for agent CLI actions.
---

# Permission Gate

## Goal

Add clear approval boundaries around actions that can affect files, credentials, external systems, money, or user trust.

## Policy Checklist

1. Classify the action: read, write, execute, network, destructive, credential, or external side effect.
2. Define the default decision.
3. Define what context is shown to the user.
4. Define allowed responses.
5. Define what gets logged.
6. Define how denial and timeout are handled.

## Rules

- Default to explicit approval for destructive or external side-effect actions.
- Make the requested action concrete, not vague.
- Avoid broad persistent approvals unless the scope is narrow and understandable.
- Never hide a denied action by trying a different route.

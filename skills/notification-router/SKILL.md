---
name: notification-router
description: Use when designing or implementing notifications for agent CLI events, hook results, bridge events, approvals, failures, or long-running tasks.
---

# Notification Router

## Goal

Route agent CLI events to useful notifications without creating noise.

## Event Checklist

1. Identify the source event.
2. Classify severity: info, success, warning, error, or approval-needed.
3. Choose the destination: terminal, desktop notification, log file, webhook, chat, or UI panel.
4. Define the message format.
5. Define deduplication and rate limits.
6. Define failure behavior if delivery fails.

## Rules

- Notify on state changes, not every internal step.
- Keep messages short and actionable.
- Include enough context to resume work.
- Do not leak secrets in notifications.

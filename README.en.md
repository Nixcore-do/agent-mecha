# Agent Mecha

Agent Mecha is an engineering exoskeleton for agents.

The current version focuses on one capability: `agent-bridge`. It helps agents collaborate with hooks, external tools, background processes, UIs, or another agent through structured events.

## Project Structure

```text
agent-mecha/
  .claude-plugin/
    plugin.json
    marketplace.json
  .codex-plugin/
    plugin.json
  skills/
    agent-bridge/
      SKILL.md
  hooks/
    agent-bridge/
      bridge.py
      launch.sh
      config/
      core/
      events/
      forms/
      ui/
      web/
      tests/
    README.md
  scripts/
    agent-bridge/
    README.md
  assets/
    README.md
  docs/
    architecture.md
  tests/
    README.md
```

## Skills

- `agent-bridge`: Design and connect agent bridge workflows.

When new capabilities are added, follow the same structure with `skills/<capability>/SKILL.md`.

## Current Implementation

`hooks/agent-bridge/` includes a runnable local bridge:

- `launch.sh`: Hook entry script.
- `bridge.py`: Reads stdin JSON, loads configuration, and routes events.
- `events/`: Handles notification, permission, question, and form events.
- `forms/`: Converts questions or JSON schemas into UI fields.
- `ui/` and `web/`: Shows permission dialogs, forms, and toast notifications.
- `config/agent-bridge.json`: Default text and window configuration.
- `claude-settings.example.json`: Claude Code hook registration example.

## Bridge Dependencies

The popup UI depends on `pywebview`.

When installed through `/plugin install`, Claude installs plugin files and registers hooks/skills, but it does not run `pip install`. Agent Mecha uses a `SessionStart` hook for runtime bootstrap: on first startup, it asynchronously creates `.venv` and installs `hooks/agent-bridge/requirements.txt`.

You can also install dependencies manually:

```bash
cd <path-to>/agent-mecha
./setup-agent-bridge.sh
```

`launch.sh` prefers the `.venv` under the plugin root. If `pywebview` is missing, the hook can still trigger, but permission dialogs, forms, and toast notifications cannot be displayed. Errors are written to the bridge logs.

## Installation

### Local Development

For local development, Claude Code can load this plugin directory directly without installing it first.

If the current directory is the parent directory of `agent-mecha`:

```bash
claude --plugin-dir ./agent-mecha
```

If the current directory is the `agent-mecha` root:

```bash
claude --plugin-dir .
```

You can also run the included startup script from any directory:

```bash
<path-to>/agent-mecha/start-claude-plugin.sh
```

### Install From GitHub

Run these commands inside a Claude Code session:

```text
/plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
/plugin install agent-mecha@agent-mecha
```

Equivalent terminal commands:

```bash
claude plugin marketplace add https://github.com/Nixcore-do/agent-mecha.git
claude plugin install agent-mecha@agent-mecha
```

Restart Claude Code after installation so hooks and skills are loaded in the new session.

Confirm the installed plugin:

```text
/plugin details agent-mecha
```

Or with the terminal command:

```bash
claude plugin details agent-mecha
```

### Local Install

`/plugin install` does not install a local path directly. Add the local directory as a marketplace first, then install the plugin from that marketplace.

Run these commands inside a Claude Code session:

```text
/plugin marketplace add <path-to>/agent-mecha
/plugin install agent-mecha@agent-mecha
```

Equivalent terminal commands:

```bash
claude plugin marketplace add <path-to>/agent-mecha
claude plugin install agent-mecha@agent-mecha
```

Confirm that Claude recognizes the plugin components:

```bash
claude --plugin-dir ./agent-mecha plugin details agent-mecha
```

Or run the included helper script:

```bash
<path-to>/agent-mecha/check-claude-plugin.sh
```

The output should include:

```text
Hooks (...) SessionStart, Stop, StopFailure, Elicitation, PermissionRequest
```

If the plugin was installed through `/plugin install`, you can also check it with:

```text
/plugin details agent-mecha
```

Or with the terminal command:

```bash
claude plugin details agent-mecha
```

Note that these hooks do not all trigger at startup. `Stop` triggers when an agent response ends, `PermissionRequest` triggers only when permission approval is needed, and `Elicitation` triggers only when form input is needed. To debug hooks, start Claude with:

```bash
claude --plugin-dir ./agent-mecha --debug hooks
```

Or run the included helper script:

```bash
<path-to>/agent-mecha/debug-claude-hooks.sh
```

To also enable bridge-level debug logs:

```bash
AGENT_BRIDGE_DEBUG=1 claude --plugin-dir ./agent-mecha --debug hooks
```

Bridge logs are stored in the system temp directory. On macOS, the path is usually similar to:

```text
/var/folders/.../T/agent-bridge/agent-mecha/
```

### Uninstall

Uninstall the plugin inside a Claude Code session:

```text
/plugin uninstall agent-mecha
```

If you no longer need this marketplace, remove it too:

```text
/plugin marketplace remove agent-mecha
```

Equivalent terminal commands:

```bash
claude plugin uninstall agent-mecha
claude plugin marketplace remove agent-mecha
```

Uninstalling removes the installed Claude Code plugin and marketplace configuration. It does not delete the local source directory at `<path-to>/agent-mecha`.

If you only want to clean runtime dependencies, delete the local virtual environment. It will be bootstrapped again on the next startup:

```bash
rm -rf <path-to>/agent-mecha/.venv
```

For local Codex development, the plugin entry is described by `.codex-plugin/plugin.json`, skills are loaded from `./skills/`, and hooks are loaded from `./hooks/codex-hooks.json`.

Claude Code uses `./hooks/hooks.json`, where `SessionStart`, `Stop`, and `StopFailure` can be declared as async hooks. Codex does not support async hooks yet, so the Codex entry references a separate `./hooks/codex-hooks.json` file without `async` fields.

The Codex hook file keeps the same hook events, but runs them synchronously: `SessionStart`, `Stop`, `StopFailure`, `PermissionRequest`, and `Elicitation` are all registered in `./hooks/codex-hooks.json`.

Before publishing, update `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` with the final author, repository, homepage, privacy policy, and terms of service information.

## Development

When adding a new capability, use this structure:

```text
skills/<capability>/SKILL.md
hooks/<capability>/
scripts/<capability>/
docs/<capability>.md
tests/<capability>/
```

Define the skill and interface contract first, then implement scripts or hooks.

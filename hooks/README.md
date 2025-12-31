# Hooks

Hooks are shell commands that execute automatically at specific Claude lifecycle events. They enable automation, validation, and integration with external tools.

## Available Hooks

| Hook | Trigger | Security Level |
|------|---------|----------------|
| [auto-format](./auto-format/) | After file edits | LOW |
| [lint-check](./lint-check/) | After file edits | LOW |
| [notification](./notification/) | On task completion | LOW |
| [command-logger](./command-logger/) | After bash commands | LOW |
| [pre-commit-check](./pre-commit-check/) | Before git commits | MEDIUM |

## Security Levels

- **LOW**: Read-only operations, well-known tools, no network access
- **MEDIUM**: File modifications, known network endpoints, build/test execution
- **HIGH**: Dynamic execution, user-controlled network, system modifications

## Hook Events

| Event | Description |
|-------|-------------|
| `PreToolUse` | Before a tool is executed (can block) |
| `PostToolUse` | After a tool completes |
| `Stop` | When Claude stops working |
| `Notification` | When Claude sends a notification |
| `SessionStart` | When a session begins |
| `SessionEnd` | When a session ends |

## Installation

Each hook includes a `settings.json` that can be merged into your Claude settings:

1. Review the hook's README.md for security disclosure
2. Copy the settings.json content
3. Merge into `~/.claude/settings.json` or `.claude/settings.json`

Or use the installer:
```bash
./install.sh --hooks auto-format,lint-check
```

## Creating New Hooks

See [templates/hook/](../templates/hook/) for templates.

Required files:
- `README.md` with security disclosure
- `settings.json` with hook configuration

## Security Review

Before using a hook:
1. Read the security disclosure
2. Understand what commands will execute
3. Verify the commands are from trusted sources
4. Consider the impact of the hook failing

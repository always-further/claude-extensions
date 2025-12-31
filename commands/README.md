# Commands

Custom slash commands that provide specialized workflows. Invoke these with `/<command-name>` in Claude Code.

## Available Commands

| Command | Description |
|---------|-------------|
| [/merge-conflict](./merge-conflict.md) | Interactive merge conflict resolution |
| [/dependency-audit](./dependency-audit.md) | Audit dependencies for security and updates |
| [/project-summary](./project-summary.md) | Generate project overview |
| [/tech-debt](./tech-debt.md) | Identify technical debt |
| [/onboarding](./onboarding.md) | Generate developer onboarding guide |

## Usage

```
/merge-conflict
/merge-conflict src/file.js

/dependency-audit
/dependency-audit security

/project-summary
/project-summary detailed

/tech-debt
/tech-debt src/

/onboarding
/onboarding setup
```

## Creating New Commands

See [templates/command.md.template](../templates/command.md.template).

Commands are markdown files with YAML frontmatter:

```yaml
---
description: What this command does
arguments: Description of expected arguments
---

# Instructions for the command
```

## Command Location

- Project commands: `.claude/commands/`
- Global commands: `~/.claude/commands/`

Project commands take precedence over global commands with the same name.

# Contributing to Claude Code Community Extensions

Thank you for your interest in contributing! This guide will help you add new skills, agents, hooks, commands, or MCP configurations.

## Quick Start

1. Fork the repository
2. Create a branch: `git checkout -b add-my-component`
3. Add your component using the templates in `templates/`
4. Run validation: `./scripts/validate.py path/to/your/component`
5. Submit a pull request

## Component Types

### Skills

Skills are domain expertise that Claude loads on-demand. They live in `skills/<skill-name>/`.

**Required files:**
- `SKILL.md` - The skill definition (Claude loads this)
- `README.md` - Human documentation

**Optional files:**
- `examples.md` - Usage examples
- `reference.md` - Additional reference material
- `scripts/` - Helper scripts

**SKILL.md format:**
```yaml
---
name: my-skill
description: When and how to use this skill. Triggers include "keyword1", "keyword2". Max 1024 characters.
allowed-tools: Bash, Read, Grep, Glob
---

# Skill Title

You are an expert in [domain].

## Capabilities
- Capability 1
- Capability 2

## Guidelines
- Guideline 1
- Guideline 2
```

**Requirements:**
- [ ] `name` is lowercase alphanumeric with hyphens only
- [ ] `description` is under 1024 characters
- [ ] `description` includes trigger keywords/phrases
- [ ] SKILL.md is under 500 lines (use reference files for more)
- [ ] README.md explains purpose and usage

### Agents

Agents are specialized sub-agents. They live in `agents/<agent-name>.md`.

**Format:**
```yaml
---
name: my-agent
description: When to invoke this agent. Triggers on "keyword1", "keyword2".
tools: Glob, Grep, Read, Bash
model: sonnet
---

# Agent Title

You are a specialized agent for [purpose].

## Your Role
[Detailed instructions]

## Process
1. Step 1
2. Step 2

## Output Format
[Expected output structure]
```

**Requirements:**
- [ ] `name` is lowercase alphanumeric with hyphens
- [ ] `description` clearly describes trigger conditions
- [ ] `tools` is appropriate for the task
- [ ] `model` is `haiku`, `sonnet`, or `opus` (default: inherit)
- [ ] Instructions are clear and actionable

### Hooks

Hooks execute shell commands at Claude lifecycle events. They live in `hooks/<hook-name>/`.

**Required files:**
- `README.md` - Documentation with security disclosure
- `settings.json` - Hook configuration snippet

**Optional files:**
- `scripts/` - Helper scripts referenced by hook

**README.md must include:**
```markdown
# Hook Name

## Overview
What this hook does.

## Security Disclosure

**Security Level:** LOW | MEDIUM | HIGH

**Commands executed:**
\`\`\`bash
# Exact commands that will run
your-command-here
\`\`\`

**Trigger:** When this runs (e.g., "After Claude edits files")

**Risk assessment:** Why this is LOW/MEDIUM/HIGH risk

## Configuration
[How to configure]

## Requirements
[Dependencies needed]
```

**settings.json format:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

**Requirements:**
- [ ] Security level accurately reflects risk
- [ ] All executed commands documented
- [ ] No use of `eval` or dynamic command execution
- [ ] Input validation for any user-provided data
- [ ] File operations scoped appropriately

### Commands

Commands are custom slash commands. They live in `commands/<command-name>.md`.

**Format:**
```yaml
---
description: What this command does
arguments: Optional - describes expected arguments
---

# Command instructions

[Instructions that Claude follows when command is invoked]
```

**Requirements:**
- [ ] `description` is clear and concise
- [ ] Instructions are actionable
- [ ] `$ARGUMENTS` placeholder used if arguments expected

### MCP Presets

MCP presets are pre-configured server bundles. They live in:
- `mcp/claude-code/<preset-name>.json` - For Claude Code
- `mcp/claude-desktop/<preset-name>.json` - For Claude Desktop

**Claude Code format (.mcp.json style):**
```json
{
  "mcpServers": {
    "server-name": {
      "transport": "http",
      "url": "https://api.example.com/mcp"
    }
  }
}
```

**Claude Desktop format (claude_desktop_config.json style):**
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["@example/mcp-server"]
    }
  }
}
```

**Requirements:**
- [ ] README in parent mcp/ directory documents environment variables needed
- [ ] Servers are from reputable sources
- [ ] Configuration uses environment variable placeholders for secrets

## Validation

Before submitting, run the validation script:

```bash
./scripts/validate.py path/to/your/component
```

This checks:
- YAML frontmatter validity
- Required files present
- Description length limits
- Name format compliance
- Security disclosure for hooks

## Pull Request Process

1. **Title format:** `Add [type]: [name]`
   - Example: `Add skill: kubernetes-helper`
   - Example: `Add hook: auto-lint`

2. **Description should include:**
   - What the component does
   - Why it's useful
   - Any dependencies or requirements

3. **Checks must pass:**
   - Validation script
   - CI workflow

4. **Review process:**
   - Skills/Agents/Commands: 1 maintainer approval
   - Hooks: Security review + 2 maintainer approvals
   - MCP presets: 1 maintainer approval

## Security Review for Hooks

Hooks execute shell commands and require extra scrutiny:

### LOW Risk
- Read-only operations
- Formatting/linting tools
- Logging/notification
- Examples: prettier, eslint --fix, echo

### MEDIUM Risk
- File modifications (restricted scope)
- Network requests (known endpoints)
- Build/test execution
- Examples: npm test, build scripts

### HIGH Risk
- Arbitrary command execution
- Network requests (user-specified)
- File operations outside project
- Examples: eval, curl with user input

HIGH risk hooks require:
- Detailed security justification
- 2 maintainer approvals
- Explicit documentation of all risks

## Templates

Use these templates to get started:

- `templates/skill/SKILL.md.template`
- `templates/agent.md.template`
- `templates/hook/README.md.template`
- `templates/command.md.template`

## Code of Conduct

- Be respectful and constructive
- Focus on improving the community
- Help others learn

## Questions?

Open an issue or discussion if you need help!

# User Guide

This guide explains how to use each type of extension in Claude Code.

---

## Table of Contents

- [Skills](#skills)
- [Agents](#agents)
- [Hooks](#hooks)
- [Commands](#commands)
- [MCP Presets](#mcp-presets)

---

## Skills

Skills are domain-specific knowledge modules that Claude loads on-demand when it recognizes relevant tasks. They provide specialized expertise without cluttering Claude's base knowledge.

### How Skills Work

Skills are markdown files in `~/.claude/skills/` that contain instructions, best practices, and patterns for specific domains. Claude automatically loads relevant skills based on context.

### Using Skills

Skills are **automatic** - you don't need to explicitly invoke them. Claude detects when a skill is relevant and applies it.

**Examples:**

```
You: Help me resolve this git merge conflict

Claude: [Automatically loads git-workflow skill]
        I'll help you resolve the merge conflict. Let me analyze the conflicting files...
```

```
You: Review this code for security issues

Claude: [Automatically loads security-auditor skill]
        I'll perform a security review focusing on OWASP Top 10 vulnerabilities...
```

```
You: Write tests for this authentication module

Claude: [Automatically loads testing-assistant skill]
        I'll create comprehensive tests for your auth module using your testing framework...
```

### Available Skills

| Skill | Triggers On | What It Does |
|-------|-------------|--------------|
| **git-workflow** | Merge conflicts, rebasing, branching | Git best practices, conflict resolution strategies |
| **code-review** | Code review requests | Structured review checklist, common issues |
| **testing-assistant** | Test writing, TDD | Framework-specific test patterns |
| **documentation-writer** | Doc generation | API docs, README templates, JSDoc/docstrings |
| **security-auditor** | Security review | OWASP checks, vulnerability scanning |
| **performance-optimizer** | Performance issues | Profiling, optimization strategies |
| **api-designer** | API design | REST/GraphQL patterns, versioning |
| **database-assistant** | Schema, queries | Migration strategies, query optimization |

### Creating Custom Skills

Create a new directory in `~/.claude/skills/your-skill-name/` with:

```
your-skill-name/
  README.md          # Skill documentation
  instructions.md    # Main instructions Claude will follow
```

**Example `instructions.md`:**

```markdown
# React Component Skill

When the user asks about React components, follow these guidelines:

## Patterns
- Use functional components with hooks
- Prefer composition over inheritance
- Keep components small and focused

## File Structure
- One component per file
- Co-locate tests with components
- Use index.ts for exports

## Examples
[Include code examples here]
```

---

## Agents

Agents are specialized sub-agents that Claude can spawn for specific tasks. They run autonomously with their own context and tools, then return results.

### How Agents Work

Agents are markdown files in `~/.claude/agents/` that define specialized behaviors. When Claude recognizes a task suited for an agent, it spawns that agent to handle it.

### Using Agents

Agents are typically invoked **automatically** by Claude when appropriate, but you can also request them explicitly.

**Automatic invocation:**

```
You: I need to commit these changes

Claude: I'll use the commit-message-writer agent to generate an appropriate commit message.
        [Spawns agent, analyzes diff, returns message]

        Suggested commit message:
        feat(auth): add OAuth2 support for Google login

        - Add GoogleAuthProvider component
        - Implement token refresh logic
        - Add user profile sync on login
```

**Explicit request:**

```
You: Use the pr-reviewer agent to review PR #42

Claude: [Spawns pr-reviewer agent]

        ## PR Review: Add user authentication (#42)

        ### Summary
        This PR adds JWT-based authentication...

        ### Issues Found
        1. **Security**: Token stored in localStorage (line 45)
        2. **Performance**: Unnecessary re-renders in AuthContext

        ### Suggestions
        ...
```

### Available Agents

| Agent | Best For | Example Request |
|-------|----------|-----------------|
| **commit-message-writer** | Git commits | "Help me write a commit message" |
| **pr-reviewer** | PR review | "Review this pull request" |
| **architecture-reviewer** | Codebase analysis | "Analyze the architecture of this project" |
| **debug-assistant** | Debugging | "Help me debug this failing test" |
| **refactor-planner** | Refactoring | "Plan how to refactor this module" |
| **dependency-manager** | Dependencies | "Check for outdated dependencies" |
| **migration-assistant** | Migrations | "Help migrate from v2 to v3 API" |
| **release-manager** | Releases | "Generate release notes for v1.2.0" |

### Creating Custom Agents

Create a markdown file in `~/.claude/agents/my-agent.md`:

```markdown
---
name: my-custom-agent
description: Specialized agent for [purpose]
tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# My Custom Agent

You are a specialized agent for [purpose].

## Your Role
[Describe what this agent does]

## Process
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output Format
[Define expected output]
```

---

## Hooks

Hooks are shell commands that execute automatically at specific points in Claude's lifecycle. They enable automation like auto-formatting, linting, and notifications.

### How Hooks Work

Hooks are configured in `~/.claude/settings.json` under the `hooks` key. They trigger on specific events like file edits, bash commands, or task completion.

### Hook Events

| Event | Triggers When | Use Cases |
|-------|---------------|-----------|
| **PreToolUse** | Before a tool runs | Validation, confirmation prompts |
| **PostToolUse** | After a tool completes | Auto-format, lint, logging |
| **Notification** | Task completes | Desktop notifications, Slack alerts |

### Available Hooks

#### auto-format
Automatically formats files after Claude edits them.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

**What happens:**
```
You: Add a new function to utils.js

Claude: [Edits utils.js]
        [auto-format hook runs: prettier --write utils.js]

        Done! I've added the function and it's been auto-formatted.
```

#### lint-check
Runs linter after file changes to catch issues immediately.

#### notification
Sends desktop notification when Claude completes a task.

#### command-logger
Logs all bash commands Claude executes (useful for auditing).

#### pre-commit-check
Validates changes before committing (runs tests, linting).

### Configuring Hooks

Hooks are stored in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here \"$FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

### Environment Variables in Hooks

| Variable | Description |
|----------|-------------|
| `$TOOL_INPUT` | JSON input passed to the tool |
| `$TOOL_OUTPUT` | JSON output from the tool |
| `$FILE_PATH` | Path of the affected file (for Edit/Write) |

### Security Considerations

Hooks execute shell commands automatically. Review each hook's commands before installing:

- **LOW risk**: Read-only operations (formatting, linting)
- **MEDIUM risk**: Write operations (auto-fix, file modifications)
- **HIGH risk**: Network operations, external API calls

---

## Commands

Commands are custom slash commands that provide shortcuts for common workflows. They're like macros that expand into full prompts.

### How Commands Work

Commands are markdown files in `~/.claude/commands/` that define reusable prompts. Invoke them with `/command-name`.

### Using Commands

```
You: /merge-conflict

Claude: I'll help you resolve merge conflicts. Let me scan for conflicts...

        Found 3 files with conflicts:
        - src/auth/login.ts
        - src/api/users.ts
        - package.json

        Let's resolve them one by one...
```

```
You: /tech-debt

Claude: I'll analyze your codebase for technical debt...

        ## Technical Debt Report

        ### High Priority
        1. **Deprecated API usage** in src/api/legacy.ts
        2. **Missing error handling** in 12 async functions

        ### Medium Priority
        ...
```

### Available Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/merge-conflict` | Interactive conflict resolution | After a failed merge/rebase |
| `/dependency-audit` | Check dependencies | Before releases, security audits |
| `/project-summary` | Generate project overview | Onboarding, documentation |
| `/tech-debt` | Find technical debt | Sprint planning, refactoring |
| `/onboarding` | New developer guide | When joining a project |

### Creating Custom Commands

Create a markdown file in `~/.claude/commands/my-command.md`:

```markdown
---
name: my-command
description: Short description shown in /help
---

# My Custom Command

[Full prompt that Claude will execute when /my-command is invoked]

## Steps
1. First, analyze...
2. Then, check...
3. Finally, report...

## Output Format
Provide results in this format:
- Section 1
- Section 2
```

### Command Arguments

Commands can accept arguments:

```
You: /dependency-audit --security-only

You: /project-summary --format=markdown
```

Handle arguments in your command file:

```markdown
---
name: dependency-audit
description: Audit project dependencies
args:
  - name: security-only
    description: Only check for security vulnerabilities
---

# Dependency Audit

{{#if args.security-only}}
Focus only on security vulnerabilities (CVEs, advisories).
{{else}}
Check for outdated packages, security issues, and license compliance.
{{/if}}
```

---

## MCP Presets

MCP (Model Context Protocol) presets are pre-configured bundles of MCP servers that extend Claude's capabilities with external tools and services.

### How MCP Works

MCP servers connect Claude to external tools like databases, APIs, and services. Presets bundle related servers together for common workflows.

### Available Presets

#### Claude Code Presets

| Preset | Servers | Use Case |
|--------|---------|----------|
| **web-dev** | Playwright, Puppeteer, GitHub | Web development, testing |
| **data-science** | Jupyter, databases | Data analysis, ML |
| **devops** | Docker, K8s, Terraform | Infrastructure, deployment |
| **security** | Security scanners | Vulnerability assessment |
| **full-stack** | All of the above | Complete dev environment |

#### Claude Desktop Presets

| Preset | Servers | Use Case |
|--------|---------|----------|
| **productivity** | Calendar, notes, files | Personal organization |
| **research** | Web search, documents | Research tasks |
| **development** | GitHub, docs | Light development |
| **communication** | Email, messaging | Communication tasks |
| **data-analysis** | Spreadsheets, databases | Data work |

### Installing MCP Presets

```bash
# Install a specific preset
./install.sh --mcp web-dev

# Install multiple presets
./install.sh --mcp web-dev,devops

# Install with a role preset (includes relevant MCP)
./install.sh --preset backend-developer
```

### Using MCP Tools

Once installed, MCP tools are available automatically:

```
You: Run the Playwright test suite

Claude: [Uses Playwright MCP server]
        Running tests...

        Results: 42 passed, 0 failed
```

```
You: Query the production database for active users

Claude: [Uses database MCP server]

        Active users (last 30 days): 1,247

        | Plan     | Count |
        |----------|-------|
        | Free     | 892   |
        | Pro      | 312   |
        | Business | 43    |
```

### Configuring MCP Servers

MCP configuration is stored in:
- **Claude Code**: `~/.mcp.json`
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      }
    }
  }
}
```

---

## Quick Reference

### Invoking Features

| Feature | How to Use |
|---------|------------|
| Skills | Automatic - just describe your task |
| Agents | Automatic or ask: "Use the X agent to..." |
| Hooks | Automatic - triggers on events |
| Commands | Type `/command-name` |
| MCP | Automatic - ask Claude to use the tool |

### File Locations

| Component | Location |
|-----------|----------|
| Skills | `~/.claude/skills/` |
| Agents | `~/.claude/agents/` |
| Commands | `~/.claude/commands/` |
| Hooks | `~/.claude/settings.json` |
| MCP (Code) | `~/.mcp.json` |
| MCP (Desktop) | `~/Library/Application Support/Claude/claude_desktop_config.json` |

### Getting Help

```
You: What skills are available?
You: List all commands
You: What MCP servers are configured?
```

---

## Troubleshooting

### Skills not loading
- Check the skill exists in `~/.claude/skills/`
- Verify `instructions.md` file is present
- Try being more explicit: "Using the git-workflow skill, help me..."

### Hooks not running
- Verify `settings.json` syntax is valid JSON
- Check the matcher regex matches the tool name
- Ensure the command is executable

### Commands not found
- Verify the `.md` file exists in `~/.claude/commands/`
- Check the filename matches the command name
- Restart Claude Code after adding new commands

### MCP servers not connecting
- Check credentials/tokens are set in environment
- Verify the server package is installed
- Check logs: `claude --mcp-debug`

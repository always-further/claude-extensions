# Claude Code Always Further Extensions

A collection of skills, agents, hooks, commands, and MCP configurations for Claude Code and Claude Desktop. Clone this repository and run the installation.

Find any new hacks that you think would be useful? Feel free to contribute!

## Quick Start

```bash
# Clone the repository
git clone https://github.com/always-further/claude-extensions.git
cd claude-extensions

# Install everything (Claude Code + Claude Desktop)
./install.sh --global --target both

# Or install selectively with interactive mode
./install.sh --interactive
```

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| **Skills** | 8+ | Domain expertise that Claude loads on-demand |
| **Agents** | 8+ | Specialized sub-agents for specific tasks |
| **Hooks** | 5+ | Automated actions triggered by Claude events |
| **Commands** | 5+ | Custom slash commands for common workflows |
| **MCP Presets** | 10+ | Pre-configured MCP server bundles |

## Installation Options

### Full Installation

```bash
# Install to Claude Code global config (~/.claude/)
./install.sh --global

# Install to Claude Desktop
./install.sh --global --target claude-desktop

# Install to both Claude Code and Claude Desktop
./install.sh --global --target both
```

### Selective Installation

```bash
# Interactive TUI for picking components
./install.sh --interactive

# Install specific components
./install.sh --skills git-workflow,code-review --agents commit-message-writer

# Install a preset bundle
./install.sh --preset backend-developer
```

### Project-Local Installation

```bash
# Install to current project's .claude/ directory
./install.sh --project .

# Install to another project
./install.sh --project /path/to/project
```

### Installation Modes

```bash
# Symlink mode (default) - easy updates via git pull
./install.sh --global --mode symlink

# Copy mode - standalone, no repo dependency
./install.sh --global --mode copy
```

## Components

### Skills

Skills provide domain expertise that Claude loads on-demand when it recognizes relevant tasks.

| Skill | Description |
|-------|-------------|
| [git-workflow](skills/git-workflow/) | Git operations, rebasing, conflict resolution |
| [code-review](skills/code-review/) | Code review assistance with checklists |
| [testing-assistant](skills/testing-assistant/) | Test writing for multiple frameworks |
| [documentation-writer](skills/documentation-writer/) | Generate documentation from code |
| [security-auditor](skills/security-auditor/) | Security review and vulnerability scanning |
| [performance-optimizer](skills/performance-optimizer/) | Performance analysis and optimization |
| [api-designer](skills/api-designer/) | REST/GraphQL API design patterns |
| [database-assistant](skills/database-assistant/) | Schema design, queries, migrations |

### Agents

Agents are specialized sub-agents that focus on specific domains with their own tools and capabilities.

| Agent | Description |
|-------|-------------|
| [commit-message-writer](agents/commit-message-writer.md) | Generate conventional commit messages |
| [pr-reviewer](agents/pr-reviewer.md) | Review pull requests and provide feedback |
| [architecture-reviewer](agents/architecture-reviewer.md) | Analyze codebase architecture |
| [debug-assistant](agents/debug-assistant.md) | Systematic debugging assistance |
| [refactor-planner](agents/refactor-planner.md) | Plan refactoring strategies |
| [dependency-manager](agents/dependency-manager.md) | Dependency updates and audits |
| [migration-assistant](agents/migration-assistant.md) | Code/data migration planning |
| [release-manager](agents/release-manager.md) | Release notes and versioning |

### Hooks

Hooks are shell commands that execute automatically at specific Claude lifecycle points.

| Hook | Trigger | Security |
|------|---------|----------|
| [auto-format](hooks/auto-format/) | After file edits | LOW |
| [lint-check](hooks/lint-check/) | After file edits | LOW |
| [notification](hooks/notification/) | On task completion | LOW |
| [command-logger](hooks/command-logger/) | After bash commands | LOW |
| [pre-commit-check](hooks/pre-commit-check/) | Before commits | MEDIUM |

### Commands

Custom slash commands for common workflows.

| Command | Description |
|---------|-------------|
| [/merge-conflict](commands/merge-conflict.md) | Interactive merge conflict resolution |
| [/dependency-audit](commands/dependency-audit.md) | Check for outdated/vulnerable dependencies |
| [/project-summary](commands/project-summary.md) | Generate project overview |
| [/tech-debt](commands/tech-debt.md) | Identify technical debt |
| [/onboarding](commands/onboarding.md) | New developer onboarding guide |

### MCP Presets

Pre-configured MCP server bundles for common workflows.

#### Claude Code Presets

| Preset | Servers |
|--------|---------|
| [web-dev](mcp/claude-code/web-dev.json) | Playwright, GitHub, Puppeteer |
| [data-science](mcp/claude-code/data-science.json) | Jupyter, database connectors |
| [devops](mcp/claude-code/devops.json) | Docker, Kubernetes, Terraform |
| [security](mcp/claude-code/security.json) | Security scanning tools |
| [full-stack](mcp/claude-code/full-stack.json) | Comprehensive development setup |

#### Claude Desktop Presets

| Preset | Servers |
|--------|---------|
| [productivity](mcp/claude-desktop/productivity.json) | Calendar, notes, file management |
| [research](mcp/claude-desktop/research.json) | Web search, document processing |
| [development](mcp/claude-desktop/development.json) | GitHub, code search, documentation |
| [communication](mcp/claude-desktop/communication.json) | Email, messaging integrations |
| [data-analysis](mcp/claude-desktop/data-analysis.json) | Spreadsheets, databases, visualization |

## Presets

Role-based bundles for quick setup:

- **minimal** - Essential components for any developer
- **full** - Everything in this repository
- **backend-developer** - Backend-focused tools and agents
- **frontend-developer** - Frontend-focused tools and agents
- **devops-engineer** - DevOps-focused tools and MCP servers

```bash
./install.sh --preset backend-developer
```

## Updating

If you installed with symlink mode (default):

```bash
cd claude-extensions
git pull
```

If you installed with copy mode:

```bash
cd claude-extensions
git pull
./install.sh --global --mode copy --force
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution

1. Fork the repository
2. Create your component using templates in `templates/`
3. Run validation: `./scripts/validate.py path/to/your/component`
4. Submit a pull request

### Security Note

Hooks execute shell commands automatically. All hook contributions require:
- Security disclosure in README
- Maintainer review before merge
- See [SECURITY.md](SECURITY.md) for details

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Claude Code Documentation](https://code.claude.com/docs/en)
- [Skills Guide](https://code.claude.com/docs/en/skills)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [MCP Documentation](https://code.claude.com/docs/en/mcp)

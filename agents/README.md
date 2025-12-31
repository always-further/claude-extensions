# Agents

Agents are specialized sub-agents that focus on specific domains. They can be invoked by the main Claude instance to handle particular types of tasks.

## Available Agents

| Agent | Description | Model |
|-------|-------------|-------|
| [commit-message-writer](./commit-message-writer.md) | Generate conventional commit messages | haiku |
| [pr-reviewer](./pr-reviewer.md) | Review pull requests | sonnet |
| [architecture-reviewer](./architecture-reviewer.md) | Analyze codebase architecture | sonnet |
| [debug-assistant](./debug-assistant.md) | Systematic debugging assistance | sonnet |
| [refactor-planner](./refactor-planner.md) | Plan refactoring strategies | sonnet |
| [dependency-manager](./dependency-manager.md) | Manage and audit dependencies | haiku |
| [migration-assistant](./migration-assistant.md) | Plan database/framework migrations | sonnet |
| [release-manager](./release-manager.md) | Manage releases and changelogs | haiku |

## How Agents Work

1. Claude recognizes a request matching an agent's description
2. Claude spawns the agent as a sub-process
3. The agent works autonomously with its specified tools
4. The agent returns results to the main Claude instance

## Agent Properties

- **name**: Unique identifier (lowercase with hyphens)
- **description**: When to invoke this agent
- **tools**: Available tools for the agent
- **model**: haiku (fast/cheap), sonnet (balanced), or opus (most capable)

## Model Selection

- **haiku**: Simple, well-defined tasks (commit messages, basic audits)
- **sonnet**: Complex analysis requiring reasoning (code review, architecture)
- **opus**: Most complex tasks requiring deep understanding

## Creating New Agents

See the [templates/agent.md.template](../templates/agent.md.template) file.

Required frontmatter:
```yaml
---
name: agent-name
description: When to invoke this agent
tools: Tool1, Tool2
model: sonnet
---
```

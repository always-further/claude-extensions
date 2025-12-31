# Skills

Skills are domain expertise that Claude loads on-demand when it recognizes relevant tasks. Each skill provides specialized knowledge and instructions for a specific area.

## Available Skills

| Skill | Description |
|-------|-------------|
| [git-workflow](./git-workflow/) | Git operations, rebasing, conflict resolution |
| [code-review](./code-review/) | Code review with quality checklists |
| [testing-assistant](./testing-assistant/) | Test writing across frameworks |
| [documentation-writer](./documentation-writer/) | README, API docs, code comments |
| [security-auditor](./security-auditor/) | Security review and vulnerability scanning |
| [performance-optimizer](./performance-optimizer/) | Performance analysis and optimization |
| [api-designer](./api-designer/) | REST and GraphQL API design |
| [database-assistant](./database-assistant/) | Schema design, queries, migrations |

## How Skills Work

1. Claude automatically discovers skills at startup
2. When you make a request, Claude matches it against skill descriptions
3. If a match is found, Claude asks permission to load the skill
4. Once loaded, Claude uses the skill's instructions to help you

## Creating New Skills

See the [templates/skill/](../templates/skill/) directory for templates.

Required files:
- `SKILL.md` - The skill definition (Claude loads this)
- `README.md` - Human documentation

Optional files:
- `examples.md` - Usage examples
- `reference.md` - Additional reference material
- `scripts/` - Helper scripts

## Skill Discovery

Skills are matched based on their `description` field in the YAML frontmatter. Write descriptions that:
- Explain when the skill should activate
- Include trigger phrases users might say
- Stay under 1024 characters

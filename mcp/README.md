# MCP Presets

Pre-configured MCP (Model Context Protocol) server bundles for common workflows. These extend Claude's capabilities with external tools and integrations.

## Claude Code Presets

Located in `claude-code/`. These use the `.mcp.json` format.

| Preset | Description |
|--------|-------------|
| [web-dev](./claude-code/web-dev.json) | Playwright, GitHub, Puppeteer |
| [data-science](./claude-code/data-science.json) | Jupyter, database connectors |
| [devops](./claude-code/devops.json) | Docker, Kubernetes, Terraform |
| [security](./claude-code/security.json) | Security scanning tools |
| [full-stack](./claude-code/full-stack.json) | Comprehensive development setup |

## Claude Desktop Presets

Located in `claude-desktop/`. These use the `claude_desktop_config.json` format.

| Preset | Description |
|--------|-------------|
| [productivity](./claude-desktop/productivity.json) | Calendar, notes, file management |
| [research](./claude-desktop/research.json) | Web search, document processing |
| [development](./claude-desktop/development.json) | GitHub, code search |
| [communication](./claude-desktop/communication.json) | Email, messaging |
| [data-analysis](./claude-desktop/data-analysis.json) | Spreadsheets, databases |

## Installation

### Claude Code

Copy the preset content to your `.mcp.json` file:

```bash
# View a preset
cat mcp/claude-code/web-dev.json

# Copy to project root
cp mcp/claude-code/web-dev.json .mcp.json

# Or merge with existing config
jq -s '.[0] * .[1]' .mcp.json mcp/claude-code/web-dev.json > .mcp.json.tmp
mv .mcp.json.tmp .mcp.json
```

### Claude Desktop

Merge into your Claude Desktop configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

## Environment Variables

Many MCP servers require API keys or configuration. Set these in your environment:

```bash
# GitHub
export GITHUB_TOKEN="your-token"

# Database connections
export DATABASE_URL="postgresql://..."

# Cloud providers
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

## Security Notes

- MCP servers can access external services
- Review server capabilities before enabling
- Use environment variables for secrets (never hardcode)
- Project-scoped servers require user approval

## Creating Custom Presets

Combine servers from different presets:

```json
{
  "mcpServers": {
    "server1": { /* from preset 1 */ },
    "server2": { /* from preset 2 */ }
  }
}
```

## Transport Types

- **http**: Remote REST endpoints
- **stdio**: Local processes (commands)

## Troubleshooting

### Server not connecting

1. Check the server is installed
2. Verify environment variables
3. Check network connectivity for HTTP servers
4. Review Claude Code logs

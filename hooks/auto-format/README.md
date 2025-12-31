# Auto-Format Hook

## Overview

Automatically formats code files after Claude edits them. Supports Prettier (JavaScript/TypeScript), Black (Python), and gofmt (Go).

## Security Disclosure

**Security Level:** LOW

**Commands executed:**
```bash
# For JavaScript/TypeScript files:
npx prettier --write "$file_path"

# For Python files:
black "$file_path"

# For Go files:
gofmt -w "$file_path"
```

**Trigger conditions:** After Claude edits or writes files with supported extensions (.js, .jsx, .ts, .tsx, .py, .go)

**File access:**
- Reads: The file that was just edited
- Writes: Overwrites the same file with formatted content

**Network access:** None (formatters run locally)

**Risk assessment:**
This hook is classified as LOW risk because:
- Only runs well-known formatting tools
- Only modifies files Claude already edited
- No network access
- No arbitrary command execution

## Configuration

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "file_path=$(echo '$TOOL_INPUT' | jq -r '.file_path // .path'); if echo \"$file_path\" | grep -qE '\\.(js|jsx|ts|tsx)$'; then npx prettier --write \"$file_path\" 2>/dev/null; elif echo \"$file_path\" | grep -qE '\\.py$'; then black \"$file_path\" 2>/dev/null; elif echo \"$file_path\" | grep -qE '\\.go$'; then gofmt -w \"$file_path\" 2>/dev/null; fi"
          }
        ]
      }
    ]
  }
}
```

## Requirements

Install the formatters you want to use:

```bash
# JavaScript/TypeScript (Prettier)
npm install -g prettier
# or use npx (no install required)

# Python (Black)
pip install black

# Go (gofmt)
# Included with Go installation
```

## Customization

### Prettier Configuration

Create a `.prettierrc` in your project:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2
}
```

### Black Configuration

Create a `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py39']
```

### Adding More File Types

Modify the command to include additional file types:

```bash
# Add CSS/SCSS support
if echo "$file_path" | grep -qE '\\.(css|scss)$'; then npx prettier --write "$file_path"; fi
```

## Troubleshooting

### Formatter not running

1. Verify the formatter is installed: `which prettier` or `which black`
2. Check file extension matches the pattern
3. Ensure `jq` is installed for JSON parsing

### Formatting conflicts with project settings

Use project-local configuration files (.prettierrc, pyproject.toml) to customize formatter behavior.

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release with Prettier, Black, gofmt support

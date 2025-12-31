# Lint Check Hook

## Overview

Runs linters on files after Claude edits them and reports any issues. Supports ESLint (JavaScript/TypeScript), Flake8/Ruff (Python), and golangci-lint (Go).

## Security Disclosure

**Security Level:** LOW

**Commands executed:**
```bash
# For JavaScript/TypeScript files:
npx eslint "$file_path" --format compact

# For Python files:
ruff check "$file_path"
# or: flake8 "$file_path"

# For Go files:
golangci-lint run "$file_path"
```

**Trigger conditions:** After Claude edits or writes files with supported extensions

**File access:**
- Reads: The file that was just edited
- Writes: None (read-only check)

**Network access:** None (linters run locally)

**Risk assessment:**
This hook is classified as LOW risk because:
- Read-only operation (no file modifications)
- Runs well-known linting tools
- No network access
- Output displayed to user for review

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
            "command": "file_path=$(echo '$TOOL_INPUT' | jq -r '.file_path // .path'); if echo \"$file_path\" | grep -qE '\\.(js|jsx|ts|tsx)$'; then npx eslint \"$file_path\" --format compact 2>/dev/null || true; elif echo \"$file_path\" | grep -qE '\\.py$'; then ruff check \"$file_path\" 2>/dev/null || true; elif echo \"$file_path\" | grep -qE '\\.go$'; then golangci-lint run \"$file_path\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

## Requirements

Install the linters you want to use:

```bash
# JavaScript/TypeScript (ESLint)
npm install -g eslint

# Python (Ruff - fast, recommended)
pip install ruff

# Python (Flake8 - traditional)
pip install flake8

# Go (golangci-lint)
brew install golangci-lint
# or: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

## Customization

### ESLint Configuration

Create an `.eslintrc.js` in your project:

```javascript
module.exports = {
  extends: ['eslint:recommended'],
  rules: {
    // Your rules
  }
};
```

### Ruff Configuration

Create a `ruff.toml` or add to `pyproject.toml`:

```toml
[tool.ruff]
select = ["E", "F", "W"]
ignore = ["E501"]
```

### golangci-lint Configuration

Create a `.golangci.yml`:

```yaml
linters:
  enable:
    - gofmt
    - govet
    - errcheck
```

## Troubleshooting

### Linter not running

1. Verify the linter is installed
2. Check that the file extension matches
3. Ensure project has linter configuration

### Too many errors

Configure your linter to ignore certain rules or use project-specific configuration.

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release with ESLint, Ruff, golangci-lint support

# Command Logger Hook

## Overview

Logs all bash commands executed by Claude to a file for auditing and review. Useful for tracking what Claude does and for security compliance.

## Security Disclosure

**Security Level:** LOW

**Commands executed:**
```bash
echo "[$(date -Iseconds)] $TOOL_NAME: $TOOL_INPUT" >> ~/.claude/command-log.txt
```

**Trigger conditions:** After any tool use (Bash, Write, Edit, etc.)

**File access:**
- Reads: None
- Writes: Appends to `~/.claude/command-log.txt`

**Network access:** None

**Risk assessment:**
This hook is classified as LOW risk because:
- Only appends to a local log file
- No command execution based on input
- No network access
- Simple logging operation

## Configuration

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date -Iseconds)] Bash: $(echo '$TOOL_INPUT' | jq -r '.command')\" >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Log All Tool Usage

To log all tool usage, not just Bash:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date -Iseconds)] $TOOL_NAME: $(echo '$TOOL_INPUT' | head -c 500)\" >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Log to Project Directory

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date -Iseconds)] $TOOL_NAME: $(echo '$TOOL_INPUT' | jq -r '.command')\" >> .claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

## Log Format

Each log entry includes:
- ISO 8601 timestamp
- Tool name
- Command or tool input

Example log:
```
[2025-01-15T10:30:45+00:00] Bash: git status
[2025-01-15T10:30:47+00:00] Bash: npm install express
[2025-01-15T10:31:02+00:00] Bash: npm test
```

## Requirements

- `jq` for JSON parsing (optional but recommended)
- Write permissions to log file location

## Customization

### Log Rotation

Add to cron to rotate logs monthly:
```bash
0 0 1 * * mv ~/.claude/command-log.txt ~/.claude/command-log-$(date +%Y%m).txt
```

### Include Session ID

```bash
echo "[$(date -Iseconds)] [$SESSION_ID] $TOOL_NAME: ..." >> ~/.claude/command-log.txt
```

### Filter Sensitive Commands

```bash
# Don't log commands containing passwords or tokens
if ! echo "$TOOL_INPUT" | grep -qiE '(password|token|secret|key)'; then
  echo "..." >> ~/.claude/command-log.txt
fi
```

## Viewing Logs

```bash
# View recent commands
tail -50 ~/.claude/command-log.txt

# Search for specific commands
grep "npm" ~/.claude/command-log.txt

# View commands from today
grep "$(date +%Y-%m-%d)" ~/.claude/command-log.txt
```

## Troubleshooting

### Log file not being created

1. Check write permissions: `touch ~/.claude/command-log.txt`
2. Verify `.claude` directory exists: `mkdir -p ~/.claude`

### Log entries truncated

Increase the character limit in the `head -c 500` command.

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release with Bash command logging

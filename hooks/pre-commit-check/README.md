# Pre-Commit Check Hook

## Overview

Runs validation checks before Claude creates git commits. Ensures tests pass, linting succeeds, and no secrets are being committed.

## Security Disclosure

**Security Level:** MEDIUM

**Commands executed:**
```bash
# Check for secrets
git diff --cached --name-only | xargs grep -l -E '(api[_-]?key|password|secret|token).*=' || true

# Run tests
npm test --passWithNoTests

# Run linter
npm run lint --if-present
```

**Trigger conditions:** Before Claude executes a `git commit` command (PreToolUse on Bash with git commit)

**File access:**
- Reads: Staged files via git diff
- Writes: None

**Network access:** May download packages if tests require them (npm test)

**Risk assessment:**
This hook is classified as MEDIUM risk because:
- Runs test suites which may have side effects
- May execute arbitrary scripts defined in package.json
- Could download packages (npm)
- However, these are standard development operations

## Configuration

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo '$TOOL_INPUT' | jq -r '.command' | grep -q 'git commit'; then echo 'Running pre-commit checks...'; npm test --passWithNoTests 2>/dev/null || { echo 'Tests failed!'; exit 1; }; npm run lint --if-present 2>/dev/null || { echo 'Linting failed!'; exit 1; }; echo 'Pre-commit checks passed!'; fi"
          }
        ]
      }
    ]
  }
}
```

### With Secret Detection

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo '$TOOL_INPUT' | jq -r '.command' | grep -q 'git commit'; then if git diff --cached | grep -qiE '(api[_-]?key|password|secret|private[_-]?key)\\s*[=:]'; then echo 'WARNING: Possible secrets detected in staged files!'; exit 1; fi; fi"
          }
        ]
      }
    ]
  }
}
```

### Python Projects

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo '$TOOL_INPUT' | jq -r '.command' | grep -q 'git commit'; then pytest --tb=short 2>/dev/null || { echo 'Tests failed!'; exit 1; }; ruff check . 2>/dev/null || { echo 'Linting failed!'; exit 1; }; fi"
          }
        ]
      }
    ]
  }
}
```

## Checks Performed

1. **Secret Detection**: Scans staged files for potential secrets
2. **Test Execution**: Runs the project's test suite
3. **Linting**: Runs the project's linter

If any check fails, the commit is blocked.

## Requirements

### Node.js Projects
- `npm test` script defined in package.json
- Optional: `npm run lint` script

### Python Projects
- pytest installed
- ruff or flake8 installed

## Customization

### Skip Checks for WIP Commits

```bash
if echo '$TOOL_INPUT' | grep -qv 'WIP'; then
  # Run checks only for non-WIP commits
fi
```

### Add Type Checking

```bash
npm run typecheck 2>/dev/null || { echo 'Type errors!'; exit 1; }
```

### Add Build Check

```bash
npm run build 2>/dev/null || { echo 'Build failed!'; exit 1; }
```

## Troubleshooting

### Hook blocking all commits

1. Check that your test command works: `npm test`
2. Verify lint command exists: `npm run lint`
3. Temporarily disable hook to debug

### Secret detection false positives

Adjust the regex pattern to be more specific or add exceptions:

```bash
if ! echo "$file" | grep -q 'test\|spec\|example'; then
  # Check for secrets only in non-test files
fi
```

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release with test, lint, and secret detection

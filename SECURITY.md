# Security Policy

This document outlines the security considerations for using and contributing to this repository, with particular focus on hooks that execute shell commands.

## Security Model

### Component Risk Levels

| Component Type | Risk Level | Reason |
|---------------|------------|--------|
| Skills | LOW | Text-based instructions only, no code execution |
| Agents | LOW | Text-based instructions only, no code execution |
| Commands | LOW | Text-based instructions only, no code execution |
| MCP Presets | MEDIUM | External service connections, may require API keys |
| Hooks | VARIES | Execute shell commands automatically |

### Hook Security Classification

Hooks are classified by their potential impact:

#### LOW Risk
- **Characteristics:**
  - Read-only operations
  - Well-known tools with predictable behavior
  - No network access
  - No file modifications outside standard tooling

- **Examples:**
  - Formatting code with prettier/black
  - Running linters
  - Displaying notifications
  - Logging to local files

#### MEDIUM Risk
- **Characteristics:**
  - File modifications within project scope
  - Network requests to known, trusted endpoints
  - Execution of build/test scripts
  - Package manager operations

- **Examples:**
  - Running `npm test`
  - Executing build scripts
  - Sending notifications to Slack/Discord
  - Updating dependency lock files

#### HIGH Risk
- **Characteristics:**
  - Dynamic command execution (eval, shell expansion)
  - User-controlled network requests
  - File operations outside project directory
  - Credential handling
  - System-level changes

- **Examples:**
  - Commands using `eval`
  - `curl` with user-specified URLs
  - Writing to system directories
  - Environment variable manipulation

## For Users

### Before Installing Hooks

1. **Review the hook's README.md** - Check the security disclosure section
2. **Examine settings.json** - Understand exactly what commands will run
3. **Check the security level** - Be extra cautious with MEDIUM/HIGH risk hooks
4. **Verify dependencies** - Ensure required tools are from trusted sources

### Installation Safety

The installer displays hook commands before installation:

```
HOOK: auto-format (Security Level: LOW)

This hook executes:
  npx prettier --write "$file_path"

Trigger: After Claude edits TypeScript/JavaScript files

Install this hook? [y/N/v to view source]
```

**Always review before accepting.**

### Recommended Practices

1. **Use symlink mode** - Easier to audit changes via git history
2. **Review updates** - Check git diff before pulling updates
3. **Start minimal** - Install only what you need
4. **Test in a sandbox** - Try hooks in a test project first

### Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. Email security concerns to the maintainers
3. Include:
   - Component name and path
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact

## For Contributors

### Hook Security Requirements

All hooks MUST include a security disclosure in README.md:

```markdown
## Security Disclosure

**Security Level:** [LOW | MEDIUM | HIGH]

**Commands executed:**
\`\`\`bash
# List every command that will run
command-1
command-2
\`\`\`

**Trigger conditions:** [When this hook runs]

**File access:** [What files are read/written]

**Network access:** [What network requests are made, if any]

**Risk assessment:** [Why this security level was chosen]
```

### Prohibited Patterns

The following are NOT allowed in hooks:

1. **Dynamic execution:**
   ```bash
   # PROHIBITED
   eval "$user_input"
   bash -c "$command"
   ```

2. **Unvalidated network requests:**
   ```bash
   # PROHIBITED
   curl "$user_url"
   wget "$external_source"
   ```

3. **Credential exposure:**
   ```bash
   # PROHIBITED
   echo $API_KEY
   cat ~/.ssh/id_rsa
   ```

4. **Arbitrary file access:**
   ```bash
   # PROHIBITED
   cat /etc/passwd
   rm -rf /
   ```

5. **Hidden commands:**
   ```bash
   # PROHIBITED - not documented
   secret_command_not_in_readme
   ```

### Required Validations

Before submitting a hook PR:

1. **All commands documented** - Every command in README.md
2. **Input validation** - Sanitize any external input
3. **Scope limitation** - Operations restricted to project directory
4. **Failure handling** - Graceful handling of errors
5. **No secrets** - No hardcoded credentials or API keys

### Review Process

Hook PRs require:

1. **Automated validation** - CI checks pass
2. **Security review** - Maintainer examines all commands
3. **Dual approval** - Two maintainers for HIGH risk
4. **Testing** - Verified in isolated environment

## MCP Security Considerations

### API Key Handling

MCP presets should:
- Use environment variable placeholders: `${API_KEY}`
- Document required environment variables
- Never include actual credentials

### Server Verification

Before adding MCP presets:
- Verify the server is from a reputable source
- Check the server's security practices
- Document the server's privacy policy

## Vulnerability Disclosure Timeline

| Day | Action |
|-----|--------|
| 0 | Vulnerability reported |
| 1-3 | Initial assessment |
| 7 | Fix development begins |
| 14 | Fix ready for review |
| 21 | Fix deployed |
| 30 | Public disclosure (if applicable) |

## Updates to This Policy

This security policy may be updated. Check the git history for changes.

Last updated: 2025

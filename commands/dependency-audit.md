---
description: Audit dependencies for security vulnerabilities and updates
arguments: Optional - 'security' for security-only or 'outdated' for updates-only
---

# Dependency Audit

Analyze project dependencies for security vulnerabilities and available updates.

## Process

1. **Detect Package Manager**
   - Check for package.json (npm/yarn)
   - Check for requirements.txt or pyproject.toml (Python)
   - Check for go.mod (Go)
   - Check for Cargo.toml (Rust)

2. **Security Audit**
   ```bash
   # Node.js
   npm audit --json

   # Python
   pip-audit --format json

   # Go
   govulncheck ./...
   ```

3. **Check for Updates**
   ```bash
   # Node.js
   npm outdated --json

   # Python
   pip list --outdated --format json
   ```

4. **Generate Report**
   Summarize findings with actionable recommendations.

## Output Format

### Security Vulnerabilities

| Package | Severity | CVE | Current | Fixed In | Description |
|---------|----------|-----|---------|----------|-------------|
| lodash | High | CVE-2021-XXXX | 4.17.20 | 4.17.21 | Prototype pollution |

### Outdated Packages

| Package | Current | Wanted | Latest | Type |
|---------|---------|--------|--------|------|
| express | 4.17.0 | 4.18.0 | 5.0.0 | dependencies |

### Recommendations

#### Immediate (Security)
- [ ] Update `lodash` to 4.17.21 (fixes High severity CVE)

#### Soon (Minor Updates)
- [ ] Update `express` to 4.18.0

#### Planned (Major Updates)
- [ ] Consider `express` 5.0.0 (breaking changes, review changelog)

## Arguments

- `security` - Only run security audit
- `outdated` - Only check for updates
- No argument - Run full audit

## Commands to Run

```bash
# Fix security issues automatically
npm audit fix

# Update to latest minor/patch versions
npm update

# Update a specific package
npm install package@version
```

## Guidelines

- Prioritize security vulnerabilities
- Note breaking changes in major updates
- Consider the stability of new versions
- Check changelogs for important changes

---
description: Identify and catalog technical debt in the codebase
arguments: Optional path to focus on specific directory
---

# Technical Debt Analysis

Scan the codebase to identify and catalog technical debt, including TODOs, FIXMEs, deprecated code, and code quality issues.

## Process

1. **Find Explicit Markers**
   ```bash
   grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG\|DEPRECATED" src/
   ```

2. **Analyze Code Quality**
   - Check for large files (>500 lines)
   - Find complex functions (high cyclomatic complexity)
   - Identify duplicated code
   - Look for outdated patterns

3. **Check Dependencies**
   - Find deprecated dependencies
   - Identify outdated major versions
   - Look for security advisories

4. **Review Documentation**
   - Missing documentation
   - Outdated documentation
   - Incomplete API docs

## Output Format

### Technical Debt Summary

| Category | Count | Priority |
|----------|-------|----------|
| TODOs | 15 | Medium |
| FIXMEs | 3 | High |
| Deprecated Code | 5 | Medium |
| Large Files | 8 | Low |

### Explicit Markers

#### High Priority (FIXME/BUG)
| File | Line | Comment |
|------|------|---------|
| src/auth.js | 42 | FIXME: Race condition in token refresh |
| src/api.js | 156 | BUG: Doesn't handle network errors |

#### Medium Priority (TODO)
| File | Line | Comment |
|------|------|---------|
| src/utils.js | 23 | TODO: Add input validation |

### Code Quality Issues

#### Large Files (>500 lines)
| File | Lines | Suggestion |
|------|-------|------------|
| src/UserService.js | 850 | Split into smaller modules |

#### Complex Functions
| Function | File | Complexity | Suggestion |
|----------|------|------------|------------|
| processOrder | orders.js | High | Extract sub-functions |

### Deprecated Dependencies

| Package | Current | Status | Action |
|---------|---------|--------|--------|
| moment | 2.29.0 | Deprecated | Migrate to date-fns or dayjs |

### Recommended Actions

#### Immediate
1. Fix FIXME items (security/correctness)
2. Update deprecated dependencies

#### Short-term
1. Address TODO items
2. Refactor large files

#### Long-term
1. Reduce code duplication
2. Improve documentation coverage

## Arguments

If `$ARGUMENTS` contains a path, focus analysis on that directory.

## Guidelines

- Prioritize by impact and risk
- Group related issues
- Suggest concrete solutions
- Estimate effort where possible

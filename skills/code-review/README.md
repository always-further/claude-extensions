# Code Review Skill

## Overview

This skill enables thorough, professional code reviews that identify bugs, security issues, and opportunities for improvement while remaining constructive and educational.

## Activation Triggers

This skill activates when you:
- Ask for code to be reviewed
- Want feedback on implementation
- Need a quality check
- Ask about best practices for specific code

Example prompts:
- "Review this function for me"
- "Is this implementation correct?"
- "Find potential bugs in this code"
- "How can I improve this class?"
- "Check this for security issues"

## Review Categories

### Correctness
- Logic errors
- Edge cases
- Null handling
- Race conditions

### Security
- Input validation
- Injection vulnerabilities
- Authentication issues
- Data exposure

### Performance
- Algorithm efficiency
- Memory usage
- Database queries
- Caching

### Maintainability
- Code clarity
- Naming conventions
- DRY principle
- SOLID principles

## Example Usage

### Example 1: Function Review

**User**: "Review this authentication function"

**Claude**: Analyzes the function for security vulnerabilities (password handling, timing attacks), correctness (edge cases, error handling), and best practices. Provides specific line-by-line feedback.

### Example 2: Pull Request Review

**User**: "Review the changes in this PR"

**Claude**: Examines the diff, identifies issues, suggests improvements, and provides an overall assessment with clear approve/request changes recommendation.

## Output Format

Reviews are structured as:
1. **Summary**: Overall assessment
2. **Critical Issues**: Must-fix problems
3. **Suggestions**: Nice-to-have improvements
4. **Positive Aspects**: What's done well

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release

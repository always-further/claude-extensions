# Testing Assistant Skill

## Overview

This skill helps you write effective tests, improve test coverage, and understand testing best practices across multiple languages and frameworks.

## Activation Triggers

This skill activates when you:
- Need to write tests for code
- Want to improve test coverage
- Need help with mocking
- Have questions about testing patterns
- Want to set up a testing framework

Example prompts:
- "Write unit tests for this function"
- "How do I mock this API call?"
- "Help me improve test coverage"
- "What's the best way to test this async code?"
- "Set up Jest for my project"

## Supported Frameworks

### JavaScript/TypeScript
- Jest, Vitest, Mocha
- React Testing Library
- Playwright, Cypress

### Python
- pytest, unittest

### Go
- testing, testify

### Other
- JUnit, RSpec

## Example Usage

### Example 1: Writing Unit Tests

**User**: "Write tests for this validation function"

**Claude**: Analyzes the function, identifies test cases (valid input, invalid input, edge cases, error conditions), and generates comprehensive tests using your project's testing framework.

### Example 2: Mocking Dependencies

**User**: "How do I mock the database in these tests?"

**Claude**: Provides mocking strategies appropriate to your framework, shows how to set up mocks, and demonstrates proper mock verification.

### Example 3: Testing Async Code

**User**: "My async tests are flaky, help!"

**Claude**: Reviews the tests, identifies race conditions or timing issues, and suggests fixes using proper async testing patterns.

## Testing Principles Applied

- **AAA Pattern**: Arrange, Act, Assert
- **Single Responsibility**: One assertion focus per test
- **Independence**: No test depends on another
- **Descriptive Names**: Tests document behavior

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release

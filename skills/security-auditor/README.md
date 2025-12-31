# Security Auditor Skill

## Overview

This skill performs security audits on code, identifies vulnerabilities, and provides remediation guidance following OWASP guidelines and security best practices.

## Activation Triggers

This skill activates when you:
- Need a security review of code
- Want to find vulnerabilities
- Have questions about secure coding
- Need to fix security issues
- Want to understand security risks

Example prompts:
- "Is this authentication code secure?"
- "Find vulnerabilities in this endpoint"
- "How do I prevent SQL injection here?"
- "Security audit this module"
- "Check this for XSS vulnerabilities"

## Security Areas Covered

### OWASP Top 10
- Injection attacks
- Broken authentication
- Sensitive data exposure
- XSS vulnerabilities
- Access control issues
- Security misconfigurations

### Common Vulnerabilities
- SQL/NoSQL injection
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Insecure direct object references
- Security misconfiguration
- Sensitive data exposure

## Example Usage

### Example 1: Authentication Review

**User**: "Review this login function for security issues"

**Claude**: Examines password handling, session management, rate limiting, and provides specific recommendations for hardening authentication.

### Example 2: API Security

**User**: "Is this API endpoint secure?"

**Claude**: Checks for injection vulnerabilities, authorization issues, input validation, and secure headers. Provides code fixes.

### Example 3: Dependency Audit

**User**: "Check my dependencies for vulnerabilities"

**Claude**: Reviews package.json/requirements.txt, identifies known vulnerabilities, and suggests updates or alternatives.

## Output Format

Findings include:
- Severity rating (Critical/High/Medium/Low)
- Specific location (file:line)
- Detailed explanation
- Remediation code

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release

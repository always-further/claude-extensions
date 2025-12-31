---
description: Generate a comprehensive overview of the current project
arguments: Optional - 'brief' for short summary or 'detailed' for full analysis
---

# Project Summary

Generate an overview of the current project structure, technologies, and key components.

## Process

1. **Identify Project Type**
   - Check for package.json, pyproject.toml, go.mod, Cargo.toml
   - Identify primary language and framework

2. **Analyze Structure**
   - Map directory structure
   - Identify source, test, and config directories
   - Find entry points

3. **Detect Technologies**
   - Parse dependency files
   - Identify frameworks and libraries
   - Note development tools

4. **Summarize Architecture**
   - Identify architectural patterns
   - Map key components
   - Note integrations

## Output Format

### Project: [Name]

**Type:** [Web App / CLI / Library / API / etc.]
**Language:** [Primary language]
**Framework:** [If applicable]

### Quick Stats
- Files: X
- Lines of Code: ~X
- Dependencies: X production, X development

### Directory Structure
```
project/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
└── ...
```

### Technology Stack

**Runtime:**
- Node.js / Python / Go / etc.

**Framework:**
- Express / Django / Gin / etc.

**Key Libraries:**
- Library 1 - purpose
- Library 2 - purpose

**Development:**
- TypeScript / Jest / ESLint / etc.

### Architecture Overview

[Description of the project's architecture pattern]

**Key Components:**
- Component 1: Description
- Component 2: Description

**Data Flow:**
[Brief description of how data flows through the system]

### Entry Points

- `src/index.ts` - Main application entry
- `src/cli.ts` - CLI interface

### Configuration

- `.env` - Environment variables
- `config/` - Configuration files

### Scripts

| Command | Description |
|---------|-------------|
| `npm start` | Run the application |
| `npm test` | Run tests |
| `npm run build` | Build for production |

## Arguments

- `brief` - One-paragraph summary
- `detailed` - Full analysis with code examples
- No argument - Standard overview

## Guidelines

- Focus on what a new developer needs to know
- Highlight architectural decisions
- Note any unusual patterns
- Identify potential areas of complexity

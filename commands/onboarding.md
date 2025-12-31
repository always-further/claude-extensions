---
description: Generate a new developer onboarding guide for the project
arguments: Optional - 'setup' for setup focus or 'architecture' for architecture focus
---

# Developer Onboarding Guide

Generate a comprehensive onboarding document for new developers joining the project.

## Process

1. **Analyze Project**
   - Read README.md and existing documentation
   - Examine package.json/requirements.txt for dependencies
   - Identify key configuration files

2. **Document Setup**
   - Prerequisites
   - Installation steps
   - Environment configuration
   - Running locally

3. **Explain Architecture**
   - Project structure
   - Key components
   - Data flow
   - Important patterns

4. **Identify Key Areas**
   - Critical code paths
   - Common development tasks
   - Testing approach
   - Deployment process

## Output Format

# Onboarding Guide: [Project Name]

## Prerequisites

Before you begin, ensure you have:
- [ ] [Runtime] version X.X or higher
- [ ] [Database] running locally or access to dev instance
- [ ] [Other tools]

## Getting Started

### 1. Clone the Repository
```bash
git clone [repo-url]
cd [project-name]
```

### 2. Install Dependencies
```bash
npm install
# or
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

Required environment variables:
- `DATABASE_URL` - Connection string for database
- `API_KEY` - API key for [service]

### 4. Run the Application
```bash
npm run dev
# or
python manage.py runserver
```

The app will be available at http://localhost:3000

## Project Structure

```
[project-name]/
├── src/
│   ├── components/   # UI components
│   ├── services/     # Business logic
│   ├── utils/        # Helper functions
│   └── index.js      # Entry point
├── tests/            # Test files
└── docs/             # Documentation
```

## Key Concepts

### [Concept 1]
[Explanation of important concept]

### [Concept 2]
[Explanation of important concept]

## Development Workflow

### Running Tests
```bash
npm test
```

### Code Style
We use [ESLint/Prettier/Black] for code formatting.
```bash
npm run lint
```

### Creating a Branch
```bash
git checkout -b feature/your-feature
```

## Common Tasks

### Adding a New [Feature Type]
1. Step 1
2. Step 2
3. Step 3

### Debugging
- Use [debugger/logging]
- Check [common issue locations]

## Getting Help

- Slack: #[channel-name]
- Documentation: [link]
- Team Lead: @[name]

## Next Steps

After setup, we recommend:
1. [ ] Read the architecture documentation
2. [ ] Review recent PRs to understand code style
3. [ ] Pick up a "good first issue"

## Arguments

- `setup` - Focus on getting environment running
- `architecture` - Focus on understanding the codebase
- No argument - Full onboarding guide

## Guidelines

- Assume no prior knowledge of the project
- Include all environment setup steps
- Highlight common gotchas
- Provide working code examples

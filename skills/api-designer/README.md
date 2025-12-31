# API Designer Skill

## Overview

This skill helps design well-structured REST APIs and GraphQL schemas following industry best practices for consistency, usability, and maintainability.

## Activation Triggers

This skill activates when you:
- Need to design new API endpoints
- Want to structure a GraphQL schema
- Have questions about REST conventions
- Need help with API versioning
- Want to standardize response formats

Example prompts:
- "Design a REST API for user management"
- "What should this endpoint structure look like?"
- "Help me create a GraphQL schema"
- "How should I handle pagination in my API?"
- "What's the best way to version this API?"

## Design Areas

- **REST APIs**: Endpoints, methods, status codes
- **GraphQL**: Types, queries, mutations, subscriptions
- **Response Formats**: Consistent JSON structures
- **Error Handling**: Standard error responses
- **Pagination**: Cursor vs offset pagination
- **Versioning**: URL vs header versioning

## Example Usage

### Example 1: REST Endpoint Design

**User**: "I need endpoints for a blog with posts and comments"

**Claude**: Designs a complete REST API with proper resource naming, HTTP methods, relationships, and response formats following REST conventions.

### Example 2: GraphQL Schema

**User**: "Create a GraphQL schema for an e-commerce app"

**Claude**: Creates types, queries, mutations with proper input types, connection patterns for pagination, and error handling payloads.

### Example 3: API Standards

**User**: "Standardize our API response format"

**Claude**: Proposes a consistent response envelope with data, meta, and error structures that works across all endpoints.

## Output Includes

- Endpoint/schema definitions
- Request/response examples
- Status code guidance
- OpenAPI/GraphQL SDL specifications
- Implementation notes

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release

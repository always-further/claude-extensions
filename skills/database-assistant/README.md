# Database Assistant Skill

## Overview

This skill helps with database schema design, SQL query writing and optimization, migrations, and ORM configuration across multiple database systems.

## Activation Triggers

This skill activates when you:
- Need to design a database schema
- Want to optimize SQL queries
- Need help with migrations
- Have ORM questions (Prisma, TypeORM, SQLAlchemy)
- Want to understand indexing strategies

Example prompts:
- "Design a schema for a social media app"
- "Why is this query slow?"
- "How do I add an index for this query?"
- "Write a migration to add a new column"
- "Convert this SQL to Prisma"

## Supported Technologies

### Databases
- PostgreSQL
- MySQL/MariaDB
- SQLite
- MongoDB

### ORMs
- Prisma
- TypeORM
- SQLAlchemy
- Drizzle
- Sequelize

## Example Usage

### Example 1: Schema Design

**User**: "Design a database for an e-commerce platform"

**Claude**: Creates a normalized schema with tables for users, products, orders, order_items, with proper relationships, indexes, and constraints.

### Example 2: Query Optimization

**User**: "This query takes 5 seconds, help me optimize"

**Claude**: Uses EXPLAIN ANALYZE to identify bottlenecks, suggests appropriate indexes, rewrites the query for efficiency.

### Example 3: Migration Planning

**User**: "I need to split this column into two without downtime"

**Claude**: Provides a multi-step migration plan: add new columns, backfill data, update application, remove old column.

## Topics Covered

- Schema normalization/denormalization
- Index strategy and types
- Query optimization
- Relationship modeling
- Migration best practices
- ORM-specific patterns

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release

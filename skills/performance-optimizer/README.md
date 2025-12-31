# Performance Optimizer Skill

## Overview

This skill helps identify performance bottlenecks, optimize algorithms, reduce memory usage, and improve overall code efficiency.

## Activation Triggers

This skill activates when you:
- Have slow code that needs optimization
- Want to analyze algorithm complexity
- Need to reduce memory usage
- Have database performance issues
- Want to profile your application

Example prompts:
- "This function is slow, can you optimize it?"
- "Find performance bottlenecks in this code"
- "How can I reduce memory usage here?"
- "Optimize these database queries"
- "Profile this endpoint"

## Optimization Areas

- **Algorithms**: Time/space complexity improvements
- **Database**: Query optimization, indexing, N+1 queries
- **Frontend**: Bundle size, rendering, lazy loading
- **Backend**: Async processing, caching, memory management

## Example Usage

### Example 1: Algorithm Optimization

**User**: "This search is slow for large lists"

**Claude**: Analyzes the algorithm, identifies O(n^2) complexity, suggests using a hash map or binary search to achieve O(n) or O(log n).

### Example 2: Database Queries

**User**: "This page loads slowly"

**Claude**: Reviews SQL queries, identifies N+1 problems, missing indexes, and suggests optimizations like eager loading or query batching.

### Example 3: Memory Leak

**User**: "My app's memory keeps growing"

**Claude**: Looks for common leak patterns (uncleaned event listeners, growing caches, circular references) and provides fixes.

## Profiling Guidance

The skill helps with:
- Setting up profiling tools
- Interpreting profiler output
- Identifying hot paths
- Measuring improvement

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release

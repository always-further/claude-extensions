# Git Workflow Skill

## Overview

This skill enhances Claude Code's ability to assist with Git version control operations, from basic commands to advanced workflows like interactive rebasing and conflict resolution.

## Activation Triggers

This skill activates when you:
- Ask about git operations ("help me rebase", "how do I merge")
- Need to resolve conflicts
- Want to manipulate git history
- Ask about branching strategies
- Need to recover lost work

Example prompts:
- "Help me rebase my feature branch onto main"
- "I have a merge conflict, can you help?"
- "How do I squash my last 3 commits?"
- "I accidentally committed to the wrong branch"
- "What's the best branching strategy for my team?"

## Capabilities

- **Branch Management**: Create, rename, delete branches
- **Rebasing**: Interactive and standard rebasing
- **Merging**: Merge strategies and conflict resolution
- **History Editing**: Squash, reorder, amend commits
- **Recovery**: Reflog, cherry-pick, undo operations
- **Stashing**: Manage work-in-progress

## Example Usage

### Example 1: Resolving Merge Conflicts

**User**: "I have conflicts after rebasing, help me fix them"

**Claude**: Will check `git status`, identify conflicting files, show you the conflicts, explain the different versions, and guide you through resolution.

### Example 2: Squashing Commits

**User**: "Squash my last 5 commits into one"

**Claude**: Will guide you through `git rebase -i HEAD~5`, explain the squash/fixup options, and help craft a good commit message.

### Example 3: Recovering Lost Work

**User**: "I accidentally deleted my branch!"

**Claude**: Will use `git reflog` to find the lost commits and help you recover them with `git checkout` or `git cherry-pick`.

## Requirements

- Git installed and available in PATH
- Repository must be a valid git repository
- For remote operations, proper authentication must be configured

## Safety Features

- Always checks `git status` before destructive operations
- Warns about force push implications
- Recommends backup branches before risky operations
- Explains what each command does before execution

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release

#!/bin/bash
#
# Update Claude Code Community Extensions
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "Updating Claude Code Community Extensions..."
echo ""

cd "$REPO_DIR"

# Check for local changes
if [[ -n $(git status --porcelain) ]]; then
    echo "Warning: You have local changes. Stashing them..."
    git stash
    STASHED=true
fi

# Pull latest
echo "Pulling latest changes..."
git pull origin main

# Pop stash if we stashed
if [[ "$STASHED" == true ]]; then
    echo "Restoring local changes..."
    git stash pop
fi

echo ""
echo "Update complete!"
echo ""
echo "If you installed with copy mode, run:"
echo "  ./install.sh --global --mode copy --force"

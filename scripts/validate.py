#!/usr/bin/env python3
"""
Validate Claude Code Community Extension components.

Usage:
    ./scripts/validate.py                     # Validate all components
    ./scripts/validate.py skills/git-workflow # Validate specific component
    ./scripts/validate.py --changed-only      # Validate only changed files (for CI)
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("Warning: PyYAML not installed. Install with: pip install pyyaml")
    yaml = None


class ValidationError:
    def __init__(self, path: str, message: str, severity: str = "error"):
        self.path = path
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"[{self.severity.upper()}] {self.path}: {self.message}"


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    try:
        if yaml:
            metadata = yaml.safe_load(parts[1])
        else:
            # Basic parsing without yaml
            metadata = {}
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
        return metadata, parts[2]
    except Exception:
        return None, content


def validate_skill(skill_path: Path) -> List[ValidationError]:
    """Validate a skill directory."""
    errors = []
    skill_name = skill_path.name

    # Check required files
    skill_md = skill_path / "SKILL.md"
    readme = skill_path / "README.md"

    if not skill_md.exists():
        errors.append(ValidationError(str(skill_path), "Missing required SKILL.md"))
        return errors

    if not readme.exists():
        errors.append(ValidationError(str(skill_path), "Missing required README.md"))

    # Parse SKILL.md
    content = skill_md.read_text()
    metadata, body = parse_frontmatter(content)

    if metadata is None:
        errors.append(ValidationError(str(skill_md), "SKILL.md must start with YAML frontmatter (---)"))
        return errors

    # Validate required fields
    if "name" not in metadata:
        errors.append(ValidationError(str(skill_md), "Missing required 'name' field in frontmatter"))
    elif not re.match(r"^[a-z0-9-]+$", str(metadata["name"])):
        errors.append(ValidationError(str(skill_md), f"Name must be lowercase alphanumeric with hyphens, got: {metadata['name']}"))
    elif metadata["name"] != skill_name:
        errors.append(ValidationError(str(skill_md), f"Name '{metadata['name']}' doesn't match directory name '{skill_name}'", "warning"))

    if "description" not in metadata:
        errors.append(ValidationError(str(skill_md), "Missing required 'description' field in frontmatter"))
    elif len(str(metadata["description"])) > 1024:
        errors.append(ValidationError(str(skill_md), f"Description too long ({len(metadata['description'])} > 1024 characters)"))

    # Check line count
    lines = content.split("\n")
    if len(lines) > 500:
        errors.append(ValidationError(str(skill_md), f"SKILL.md too long ({len(lines)} > 500 lines). Use reference files for additional content.", "warning"))

    # Validate allowed-tools if present
    if "allowed-tools" in metadata:
        valid_tools = {"Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch", "Task", "NotebookEdit"}
        tools = [t.strip() for t in str(metadata["allowed-tools"]).split(",")]
        for tool in tools:
            if tool and tool not in valid_tools:
                errors.append(ValidationError(str(skill_md), f"Unknown tool in allowed-tools: {tool}", "warning"))

    return errors


def validate_agent(agent_path: Path) -> List[ValidationError]:
    """Validate an agent file."""
    errors = []

    content = agent_path.read_text()
    metadata, body = parse_frontmatter(content)

    if metadata is None:
        errors.append(ValidationError(str(agent_path), "Agent must start with YAML frontmatter (---)"))
        return errors

    # Validate required fields
    required_fields = ["name", "description"]
    for field in required_fields:
        if field not in metadata:
            errors.append(ValidationError(str(agent_path), f"Missing required '{field}' field in frontmatter"))

    # Validate name format
    if "name" in metadata:
        if not re.match(r"^[a-z0-9-]+$", str(metadata["name"])):
            errors.append(ValidationError(str(agent_path), f"Name must be lowercase alphanumeric with hyphens, got: {metadata['name']}"))

        expected_name = agent_path.stem
        if metadata["name"] != expected_name:
            errors.append(ValidationError(str(agent_path), f"Name '{metadata['name']}' doesn't match filename '{expected_name}'", "warning"))

    # Validate model if present
    if "model" in metadata:
        valid_models = {"haiku", "sonnet", "opus", "inherit"}
        if str(metadata["model"]).lower() not in valid_models:
            errors.append(ValidationError(str(agent_path), f"Invalid model: {metadata['model']}. Must be one of: {valid_models}"))

    # Check body has content
    if len(body.strip()) < 50:
        errors.append(ValidationError(str(agent_path), "Agent body seems too short. Include detailed instructions.", "warning"))

    return errors


def validate_hook(hook_path: Path) -> List[ValidationError]:
    """Validate a hook directory."""
    errors = []

    readme = hook_path / "README.md"
    settings = hook_path / "settings.json"

    if not readme.exists():
        errors.append(ValidationError(str(hook_path), "Missing required README.md"))
    else:
        content = readme.read_text().lower()
        if "security" not in content:
            errors.append(ValidationError(str(readme), "README.md must include security disclosure section"))
        if "security level" not in content:
            errors.append(ValidationError(str(readme), "README.md must specify security level (LOW/MEDIUM/HIGH)"))

    if not settings.exists():
        errors.append(ValidationError(str(hook_path), "Missing required settings.json"))
    else:
        try:
            with open(settings) as f:
                config = json.load(f)

            if "hooks" not in config:
                errors.append(ValidationError(str(settings), "settings.json must contain 'hooks' key"))

        except json.JSONDecodeError as e:
            errors.append(ValidationError(str(settings), f"Invalid JSON: {e}"))

    return errors


def validate_command(command_path: Path) -> List[ValidationError]:
    """Validate a command file."""
    errors = []

    content = command_path.read_text()
    metadata, body = parse_frontmatter(content)

    if metadata is None:
        errors.append(ValidationError(str(command_path), "Command must start with YAML frontmatter (---)"))
        return errors

    if "description" not in metadata:
        errors.append(ValidationError(str(command_path), "Missing required 'description' field in frontmatter"))

    if len(body.strip()) < 20:
        errors.append(ValidationError(str(command_path), "Command body seems too short. Include instructions.", "warning"))

    return errors


def validate_mcp_preset(preset_path: Path) -> List[ValidationError]:
    """Validate an MCP preset file."""
    errors = []

    try:
        with open(preset_path) as f:
            config = json.load(f)

        if "mcpServers" not in config:
            errors.append(ValidationError(str(preset_path), "MCP preset must contain 'mcpServers' key"))
        else:
            for server_name, server_config in config["mcpServers"].items():
                # Check for required fields based on transport type
                if "transport" in server_config:
                    if server_config["transport"] == "http" and "url" not in server_config:
                        errors.append(ValidationError(str(preset_path), f"Server '{server_name}' with http transport must have 'url'"))
                    elif server_config["transport"] == "stdio" and "command" not in server_config:
                        errors.append(ValidationError(str(preset_path), f"Server '{server_name}' with stdio transport must have 'command'"))
                elif "command" not in server_config and "url" not in server_config:
                    errors.append(ValidationError(str(preset_path), f"Server '{server_name}' must have either 'url' or 'command'"))

    except json.JSONDecodeError as e:
        errors.append(ValidationError(str(preset_path), f"Invalid JSON: {e}"))

    return errors


def validate_all(repo_root: Path) -> List[ValidationError]:
    """Validate all components in the repository."""
    errors = []

    # Validate skills
    skills_dir = repo_root / "skills"
    if skills_dir.exists():
        for skill in skills_dir.iterdir():
            if skill.is_dir() and not skill.name.startswith("."):
                errors.extend(validate_skill(skill))

    # Validate agents
    agents_dir = repo_root / "agents"
    if agents_dir.exists():
        for agent in agents_dir.glob("*.md"):
            if agent.name != "README.md":
                errors.extend(validate_agent(agent))

    # Validate hooks
    hooks_dir = repo_root / "hooks"
    if hooks_dir.exists():
        for hook in hooks_dir.iterdir():
            if hook.is_dir() and not hook.name.startswith("."):
                errors.extend(validate_hook(hook))

    # Validate commands
    commands_dir = repo_root / "commands"
    if commands_dir.exists():
        for command in commands_dir.glob("*.md"):
            if command.name != "README.md":
                errors.extend(validate_command(command))

    # Validate MCP presets
    for mcp_dir in [repo_root / "mcp" / "claude-code", repo_root / "mcp" / "claude-desktop"]:
        if mcp_dir.exists():
            for preset in mcp_dir.glob("*.json"):
                errors.extend(validate_mcp_preset(preset))

    return errors


def validate_path(path: Path) -> List[ValidationError]:
    """Validate a specific path."""
    errors = []

    if path.is_dir():
        # Determine type by location
        if "skills" in path.parts:
            errors.extend(validate_skill(path))
        elif "hooks" in path.parts:
            errors.extend(validate_hook(path))
        else:
            errors.append(ValidationError(str(path), "Unknown component type for directory"))
    elif path.is_file():
        if "agents" in path.parts:
            errors.extend(validate_agent(path))
        elif "commands" in path.parts:
            errors.extend(validate_command(path))
        elif "mcp" in path.parts:
            errors.extend(validate_mcp_preset(path))
        else:
            errors.append(ValidationError(str(path), "Unknown component type for file"))

    return errors


def main():
    repo_root = Path(__file__).parent.parent

    if len(sys.argv) > 1:
        if sys.argv[1] == "--changed-only":
            # Get changed files from git
            import subprocess

            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~1"],
                capture_output=True,
                text=True,
                cwd=repo_root,
            )

            changed_files = result.stdout.strip().split("\n")
            errors = []

            for file in changed_files:
                if not file:
                    continue
                path = repo_root / file
                if path.exists():
                    errors.extend(validate_path(path))
        elif sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)
        else:
            # Validate specific path
            path = Path(sys.argv[1])
            if not path.is_absolute():
                path = repo_root / path
            errors = validate_path(path)
    else:
        # Validate all
        errors = validate_all(repo_root)

    # Print results
    error_count = 0
    warning_count = 0

    for error in errors:
        print(error)
        if error.severity == "error":
            error_count += 1
        else:
            warning_count += 1

    print()
    print(f"Validation complete: {error_count} error(s), {warning_count} warning(s)")

    if error_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Claude Code Community Extensions - Interactive TUI Installer

Usage:
    ./scripts/install.py                    # Interactive mode
    ./scripts/install.py --list             # List all components
    ./scripts/install.py --preset NAME      # Install preset
    ./scripts/install.py --restore          # Restore from backup
    ./scripts/install.py --help             # Show help
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def color(text: str, color_code: str) -> str:
    """Apply color to text."""
    return f"{color_code}{text}{Colors.ENDC}"


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


class Installer:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.repo_dir = self.script_dir.parent
        self.catalog = self._load_catalog()

        # Target directories
        self.claude_code_global = Path.home() / ".claude"
        self.claude_desktop_macos = Path.home() / "Library" / "Application Support" / "Claude"
        self.claude_desktop_linux = Path.home() / ".config" / "Claude"

        # Selected components
        self.selected_skills: Set[str] = set()
        self.selected_agents: Set[str] = set()
        self.selected_hooks: Set[str] = set()
        self.selected_commands: Set[str] = set()
        self.selected_mcp: Set[str] = set()

        # Backup tracking
        self.backup_dir: Optional[Path] = None
        self.no_backup = False

    def _load_catalog(self) -> Dict:
        """Load the catalog.json file."""
        catalog_path = self.repo_dir / "catalog.json"
        if catalog_path.exists():
            with open(catalog_path) as f:
                return json.load(f)
        return {"components": {}, "presets": []}

    def get_claude_desktop_path(self) -> Optional[Path]:
        """Get the Claude Desktop config path for current platform."""
        if sys.platform == "darwin":
            return self.claude_desktop_macos
        elif sys.platform == "linux":
            return self.claude_desktop_linux
        return None

    def create_backup(self, target_dir: Path) -> Optional[Path]:
        """Create a backup of existing configuration."""
        if self.no_backup:
            return None

        # Check if there's anything to backup
        has_content = False
        subdirs = ['skills', 'agents', 'commands', 'hooks']

        for subdir in subdirs:
            subdir_path = target_dir / subdir
            if subdir_path.exists() and any(subdir_path.iterdir()):
                has_content = True
                break

        config_files = [
            target_dir / 'settings.json',
            target_dir.parent / '.mcp.json',
            target_dir / 'claude_desktop_config.json'
        ]

        for config_file in config_files:
            if config_file.exists():
                has_content = True
                break

        if not has_content:
            return None

        # Create backup directory
        backup_name = f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        backup_dir = target_dir / '.backups' / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)

        print(color(f"\nCreating backup at: {backup_dir}", Colors.BLUE))

        # Backup directories
        for subdir in subdirs:
            subdir_path = target_dir / subdir
            if subdir_path.exists() and any(subdir_path.iterdir()):
                # Use copytree with follow_symlinks=True to dereference symlinks
                shutil.copytree(subdir_path, backup_dir / subdir, symlinks=False, dirs_exist_ok=True)
                print(color(f"  Backed up {subdir}/", Colors.DIM))

        # Backup config files
        if (target_dir / 'settings.json').exists():
            shutil.copy2(target_dir / 'settings.json', backup_dir / 'settings.json')
            print(color("  Backed up settings.json", Colors.DIM))

        if (target_dir.parent / '.mcp.json').exists():
            shutil.copy2(target_dir.parent / '.mcp.json', backup_dir / '.mcp.json')
            print(color("  Backed up .mcp.json", Colors.DIM))

        if (target_dir / 'claude_desktop_config.json').exists():
            shutil.copy2(target_dir / 'claude_desktop_config.json', backup_dir / 'claude_desktop_config.json')
            print(color("  Backed up claude_desktop_config.json", Colors.DIM))

        print(color("Backup created successfully", Colors.GREEN))
        print()

        # Keep only last 5 backups
        backups_dir = target_dir / '.backups'
        if backups_dir.exists():
            backups = sorted(backups_dir.glob('backup-*'), key=lambda p: p.name, reverse=True)
            for old_backup in backups[5:]:
                shutil.rmtree(old_backup)

        self.backup_dir = backup_dir
        return backup_dir

    def list_backups(self, target_dir: Path) -> List[Path]:
        """List available backups."""
        backups_dir = target_dir / '.backups'
        if not backups_dir.exists():
            return []
        return sorted(backups_dir.glob('backup-*'), key=lambda p: p.name, reverse=True)

    def restore_backup(self, target_dir: Path) -> bool:
        """Restore from a previous backup."""
        backups = self.list_backups(target_dir)

        if not backups:
            print(color("No backups found", Colors.YELLOW))
            return False

        print(color("\nAvailable backups:", Colors.BLUE))
        for i, backup in enumerate(backups, 1):
            print(f"  {i}. {backup.name}")

        try:
            choice = input(f"\nSelect backup to restore (1-{len(backups)}): ").strip()
            idx = int(choice) - 1

            if 0 <= idx < len(backups):
                selected_backup = backups[idx]
                print(color(f"\nRestoring from: {selected_backup}", Colors.BLUE))

                # Restore directories
                for subdir in ['skills', 'agents', 'commands', 'hooks']:
                    backup_subdir = selected_backup / subdir
                    if backup_subdir.exists():
                        target_subdir = target_dir / subdir
                        if target_subdir.exists():
                            shutil.rmtree(target_subdir)
                        shutil.copytree(backup_subdir, target_subdir)
                        print(color(f"  Restored {subdir}/", Colors.GREEN))

                # Restore config files
                if (selected_backup / 'settings.json').exists():
                    shutil.copy2(selected_backup / 'settings.json', target_dir / 'settings.json')
                    print(color("  Restored settings.json", Colors.GREEN))

                if (selected_backup / '.mcp.json').exists():
                    shutil.copy2(selected_backup / '.mcp.json', target_dir.parent / '.mcp.json')
                    print(color("  Restored .mcp.json", Colors.GREEN))

                if (selected_backup / 'claude_desktop_config.json').exists():
                    shutil.copy2(selected_backup / 'claude_desktop_config.json', target_dir / 'claude_desktop_config.json')
                    print(color("  Restored claude_desktop_config.json", Colors.GREEN))

                print(color("\nRestore complete!", Colors.GREEN + Colors.BOLD))
                return True
            else:
                print(color("Invalid selection", Colors.RED))
                return False

        except (ValueError, KeyboardInterrupt):
            print(color("Restore cancelled", Colors.YELLOW))
            return False

    def print_banner(self):
        """Print the installer banner."""
        print()
        print(color("=" * 60, Colors.CYAN))
        print(color("   Claude Code Community Extensions Installer", Colors.CYAN + Colors.BOLD))
        print(color("=" * 60, Colors.CYAN))
        print()

    def print_menu(self, title: str, options: List[tuple], selected: Set[str] = None):
        """Print a menu with options."""
        print(color(f"\n{title}", Colors.BLUE + Colors.BOLD))
        print("-" * 40)

        for i, (key, name, desc) in enumerate(options, 1):
            checkbox = "[x]" if selected and key in selected else "[ ]"
            checkbox_color = Colors.GREEN if selected and key in selected else Colors.DIM
            print(f"  {color(checkbox, checkbox_color)} {i}. {color(name, Colors.CYAN)} - {desc}")

    def get_user_selection(self, prompt: str, max_val: int) -> Optional[str]:
        """Get user input for menu selection."""
        print()
        print(f"  {color('a', Colors.YELLOW)} = select all | {color('n', Colors.YELLOW)} = select none | {color('d', Colors.YELLOW)} = done | {color('q', Colors.YELLOW)} = quit")

        try:
            choice = input(f"\n{prompt}: ").strip().lower()
            return choice
        except (KeyboardInterrupt, EOFError):
            return 'q'

    def select_components(self, title: str, components: List[Dict], selected: Set[str]) -> Set[str]:
        """Interactive component selection."""
        options = [(c['id'], c['name'], c['description']) for c in components]

        while True:
            clear_screen()
            self.print_banner()
            self.print_menu(title, options, selected)

            choice = self.get_user_selection("Toggle selection (number/a/n/d/q)", len(options))

            if choice == 'q':
                sys.exit(0)
            elif choice == 'd':
                return selected
            elif choice == 'a':
                selected = {c['id'] for c in components}
            elif choice == 'n':
                selected = set()
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(components):
                    comp_id = components[idx]['id']
                    if comp_id in selected:
                        selected.remove(comp_id)
                    else:
                        selected.add(comp_id)

        return selected

    def select_hooks_with_security(self) -> Set[str]:
        """Select hooks with security warnings."""
        hooks = self.catalog['components'].get('hooks', [])
        selected = set()

        for hook in hooks:
            clear_screen()
            self.print_banner()

            print(color(f"\nHook: {hook['name']}", Colors.BLUE + Colors.BOLD))
            print("-" * 40)
            print(f"Description: {hook['description']}")
            print(f"Security Level: {color(hook['securityLevel'], Colors.YELLOW if hook['securityLevel'] == 'LOW' else Colors.RED)}")

            # Read hook README for security details
            hook_readme = self.repo_dir / hook['path'] / "README.md"
            if hook_readme.exists():
                content = hook_readme.read_text()
                # Extract commands section
                if "Commands executed:" in content:
                    start = content.find("Commands executed:")
                    end = content.find("```", content.find("```", start) + 3)
                    if start != -1 and end != -1:
                        commands_section = content[start:end + 3]
                        print(f"\n{color('Commands that will be executed:', Colors.YELLOW)}")
                        # Print just the code block
                        code_start = commands_section.find("```")
                        code_end = commands_section.find("```", code_start + 3)
                        if code_start != -1:
                            code = commands_section[code_start+3:code_end].strip()
                            if code.startswith("bash\n"):
                                code = code[5:]
                            for line in code.split("\n"):
                                print(f"  {color(line, Colors.DIM)}")

            print()
            choice = input(f"Install {hook['name']}? (y/N/q to quit): ").strip().lower()

            if choice == 'q':
                sys.exit(0)
            elif choice == 'y':
                selected.add(hook['id'])

        return selected

    def select_target(self) -> tuple:
        """Select installation target."""
        clear_screen()
        self.print_banner()

        print(color("\nInstallation Target", Colors.BLUE + Colors.BOLD))
        print("-" * 40)
        print(f"  1. {color('Claude Code (Global)', Colors.CYAN)} - ~/.claude/")
        print(f"  2. {color('Claude Desktop', Colors.CYAN)} - Application config")
        print(f"  3. {color('Both', Colors.CYAN)} - Install to both")
        print(f"  4. {color('Project', Colors.CYAN)} - Current directory .claude/")

        choice = input("\nSelect target (1-4): ").strip()

        if choice == '1':
            return ('claude-code', self.claude_code_global)
        elif choice == '2':
            return ('claude-desktop', self.get_claude_desktop_path())
        elif choice == '3':
            return ('both', (self.claude_code_global, self.get_claude_desktop_path()))
        elif choice == '4':
            return ('project', Path.cwd() / '.claude')
        else:
            return ('claude-code', self.claude_code_global)

    def select_mode(self) -> str:
        """Select installation mode."""
        clear_screen()
        self.print_banner()

        print(color("\nInstallation Mode", Colors.BLUE + Colors.BOLD))
        print("-" * 40)
        print(f"  1. {color('Symlink', Colors.CYAN)} - Link to repo (easy updates via git pull)")
        print(f"  2. {color('Copy', Colors.CYAN)} - Copy files (standalone, no repo dependency)")

        choice = input("\nSelect mode (1-2, default=1): ").strip()

        return 'copy' if choice == '2' else 'symlink'

    def install_skill(self, skill_id: str, target_dir: Path, mode: str):
        """Install a skill."""
        source = self.repo_dir / "skills" / skill_id
        dest = target_dir / "skills" / skill_id

        if not source.exists():
            print(color(f"  Skill not found: {skill_id}", Colors.YELLOW))
            return

        dest.parent.mkdir(parents=True, exist_ok=True)

        if dest.exists():
            if dest.is_symlink():
                dest.unlink()
            else:
                shutil.rmtree(dest)

        if mode == 'symlink':
            dest.symlink_to(source)
        else:
            shutil.copytree(source, dest)

        print(color(f"  Installed skill: {skill_id}", Colors.GREEN))

    def install_agent(self, agent_id: str, target_dir: Path, mode: str):
        """Install an agent."""
        source = self.repo_dir / "agents" / f"{agent_id}.md"
        dest = target_dir / "agents" / f"{agent_id}.md"

        if not source.exists():
            print(color(f"  Agent not found: {agent_id}", Colors.YELLOW))
            return

        dest.parent.mkdir(parents=True, exist_ok=True)

        if dest.exists():
            dest.unlink()

        if mode == 'symlink':
            dest.symlink_to(source)
        else:
            shutil.copy2(source, dest)

        print(color(f"  Installed agent: {agent_id}", Colors.GREEN))

    def install_hook(self, hook_id: str, target_dir: Path):
        """Install a hook by merging settings.json."""
        source_settings = self.repo_dir / "hooks" / hook_id / "settings.json"
        target_settings = target_dir / "settings.json"

        if not source_settings.exists():
            print(color(f"  Hook not found: {hook_id}", Colors.YELLOW))
            return

        target_dir.mkdir(parents=True, exist_ok=True)

        # Load existing settings
        existing = {}
        if target_settings.exists():
            with open(target_settings) as f:
                existing = json.load(f)

        # Load hook settings
        with open(source_settings) as f:
            hook_settings = json.load(f)

        # Merge hooks
        existing.setdefault('hooks', {})
        for event, handlers in hook_settings.get('hooks', {}).items():
            existing['hooks'].setdefault(event, []).extend(handlers)

        # Write merged settings
        with open(target_settings, 'w') as f:
            json.dump(existing, f, indent=2)

        print(color(f"  Installed hook: {hook_id}", Colors.GREEN))

    def install_command(self, command_id: str, target_dir: Path, mode: str):
        """Install a command."""
        source = self.repo_dir / "commands" / f"{command_id}.md"
        dest = target_dir / "commands" / f"{command_id}.md"

        if not source.exists():
            print(color(f"  Command not found: {command_id}", Colors.YELLOW))
            return

        dest.parent.mkdir(parents=True, exist_ok=True)

        if dest.exists():
            dest.unlink()

        if mode == 'symlink':
            dest.symlink_to(source)
        else:
            shutil.copy2(source, dest)

        print(color(f"  Installed command: {command_id}", Colors.GREEN))

    def install_mcp(self, preset_id: str, target_dir: Path, target_type: str):
        """Install an MCP preset."""
        if target_type == 'claude-code':
            source = self.repo_dir / "mcp" / "claude-code" / f"{preset_id}.json"
            target = target_dir.parent / ".mcp.json"
        else:
            source = self.repo_dir / "mcp" / "claude-desktop" / f"{preset_id}.json"
            target = target_dir / "claude_desktop_config.json"

        if not source.exists():
            print(color(f"  MCP preset not found: {preset_id}", Colors.YELLOW))
            return

        target.parent.mkdir(parents=True, exist_ok=True)

        # Load existing config
        existing = {}
        if target.exists():
            with open(target) as f:
                existing = json.load(f)

        # Load preset
        with open(source) as f:
            preset = json.load(f)

        # Merge mcpServers
        existing.setdefault('mcpServers', {})
        existing['mcpServers'].update(preset.get('mcpServers', {}))

        # Write merged config
        with open(target, 'w') as f:
            json.dump(existing, f, indent=2)

        print(color(f"  Installed MCP preset: {preset_id}", Colors.GREEN))

    def do_install(self, target_dir: Path, target_type: str, mode: str):
        """Perform the installation."""
        print(color(f"\nInstalling to: {target_dir}", Colors.CYAN))
        print("-" * 40)

        # Create backup before installing
        self.create_backup(target_dir)

        if target_type in ('claude-code', 'project'):
            # Skills
            for skill_id in self.selected_skills:
                self.install_skill(skill_id, target_dir, mode)

            # Agents
            for agent_id in self.selected_agents:
                self.install_agent(agent_id, target_dir, mode)

            # Commands
            for command_id in self.selected_commands:
                self.install_command(command_id, target_dir, mode)

            # Hooks
            for hook_id in self.selected_hooks:
                self.install_hook(hook_id, target_dir)

            # MCP
            for mcp_id in self.selected_mcp:
                self.install_mcp(mcp_id, target_dir, 'claude-code')

        elif target_type == 'claude-desktop':
            # Desktop only supports MCP
            for mcp_id in self.selected_mcp:
                self.install_mcp(mcp_id, target_dir, 'claude-desktop')

    def load_preset(self, preset_name: str):
        """Load a preset configuration."""
        for preset in self.catalog.get('presets', []):
            if preset['id'] == preset_name:
                self.selected_skills = set(preset.get('skills', []))
                self.selected_agents = set(preset.get('agents', []))
                self.selected_hooks = set(preset.get('hooks', []))
                self.selected_commands = set(preset.get('commands', []))
                self.selected_mcp = set(preset.get('mcp', []))
                return True
        return False

    def list_components(self):
        """List all available components."""
        self.print_banner()

        components = self.catalog.get('components', {})

        print(color("\nSkills:", Colors.BLUE + Colors.BOLD))
        for skill in components.get('skills', []):
            print(f"  - {color(skill['id'], Colors.CYAN)}: {skill['description']}")

        print(color("\nAgents:", Colors.BLUE + Colors.BOLD))
        for agent in components.get('agents', []):
            print(f"  - {color(agent['id'], Colors.CYAN)}: {agent['description']}")

        print(color("\nHooks:", Colors.BLUE + Colors.BOLD))
        for hook in components.get('hooks', []):
            level_color = Colors.GREEN if hook['securityLevel'] == 'LOW' else Colors.YELLOW
            print(f"  - {color(hook['id'], Colors.CYAN)} [{color(hook['securityLevel'], level_color)}]: {hook['description']}")

        print(color("\nCommands:", Colors.BLUE + Colors.BOLD))
        for cmd in components.get('commands', []):
            print(f"  - {color(cmd['id'], Colors.CYAN)}: {cmd['description']}")

        print(color("\nMCP Presets (Claude Code):", Colors.BLUE + Colors.BOLD))
        for mcp in components.get('mcp', {}).get('claude-code', []):
            print(f"  - {color(mcp['id'], Colors.CYAN)}: {mcp['description']}")

        print(color("\nMCP Presets (Claude Desktop):", Colors.BLUE + Colors.BOLD))
        for mcp in components.get('mcp', {}).get('claude-desktop', []):
            print(f"  - {color(mcp['id'], Colors.CYAN)}: {mcp['description']}")

        print(color("\nPresets:", Colors.BLUE + Colors.BOLD))
        for preset in self.catalog.get('presets', []):
            print(f"  - {color(preset['id'], Colors.CYAN)}: {preset['description']}")

    def run_interactive(self):
        """Run the interactive installer."""
        # Select components
        components = self.catalog.get('components', {})

        # Skills
        self.selected_skills = self.select_components(
            "Select Skills",
            components.get('skills', []),
            self.selected_skills
        )

        # Agents
        self.selected_agents = self.select_components(
            "Select Agents",
            components.get('agents', []),
            self.selected_agents
        )

        # Hooks (with security review)
        self.selected_hooks = self.select_hooks_with_security()

        # Commands
        self.selected_commands = self.select_components(
            "Select Commands",
            components.get('commands', []),
            self.selected_commands
        )

        # MCP Presets
        mcp_options = components.get('mcp', {}).get('claude-code', [])
        self.selected_mcp = self.select_components(
            "Select MCP Presets",
            mcp_options,
            self.selected_mcp
        )

        # Select target
        target_type, target_path = self.select_target()

        # Select mode
        mode = self.select_mode()

        # Confirm
        clear_screen()
        self.print_banner()

        print(color("\nInstallation Summary", Colors.BLUE + Colors.BOLD))
        print("-" * 40)
        print(f"Skills: {', '.join(self.selected_skills) or 'none'}")
        print(f"Agents: {', '.join(self.selected_agents) or 'none'}")
        print(f"Hooks: {', '.join(self.selected_hooks) or 'none'}")
        print(f"Commands: {', '.join(self.selected_commands) or 'none'}")
        print(f"MCP: {', '.join(self.selected_mcp) or 'none'}")
        print(f"Target: {target_type}")
        print(f"Mode: {mode}")

        confirm = input("\nProceed with installation? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("Installation cancelled.")
            return

        # Install
        if target_type == 'both':
            code_target, desktop_target = target_path
            if code_target:
                self.do_install(code_target, 'claude-code', mode)
            if desktop_target:
                self.do_install(desktop_target, 'claude-desktop', mode)
        else:
            self.do_install(target_path, target_type, mode)

        print(color("\nInstallation complete!", Colors.GREEN + Colors.BOLD))

        if mode == 'symlink':
            print(f"\nTo update: cd {self.repo_dir} && git pull")
        else:
            print(f"\nTo update: cd {self.repo_dir} && git pull && ./scripts/install.py")


def main():
    parser = argparse.ArgumentParser(description='Claude Code Community Extensions Installer')
    parser.add_argument('--list', action='store_true', help='List all components')
    parser.add_argument('--preset', type=str, help='Install a preset')
    parser.add_argument('--target', choices=['claude-code', 'claude-desktop', 'both', 'project'],
                        default='claude-code', help='Installation target')
    parser.add_argument('--mode', choices=['symlink', 'copy'], default='symlink',
                        help='Installation mode')
    parser.add_argument('--restore', action='store_true', help='Restore from a previous backup')
    parser.add_argument('--no-backup', action='store_true', dest='no_backup',
                        help='Skip backing up existing configuration')

    args = parser.parse_args()

    installer = Installer()
    installer.no_backup = args.no_backup

    if args.list:
        installer.list_components()
        return

    if args.restore:
        installer.print_banner()
        print(color("Restore Mode", Colors.CYAN + Colors.BOLD))
        print()

        # Determine target directory for restore
        if args.target == 'claude-code':
            target_path = installer.claude_code_global
        elif args.target == 'claude-desktop':
            target_path = installer.get_claude_desktop_path()
        elif args.target == 'project':
            target_path = Path.cwd() / '.claude'
        else:
            target_path = installer.claude_code_global

        if target_path is None:
            print(color("Error: Claude Desktop not supported on this platform", Colors.RED))
            return

        if installer.restore_backup(target_path):
            print(color("\nRestore complete!", Colors.GREEN + Colors.BOLD))
        else:
            print(color("\nRestore cancelled or failed.", Colors.YELLOW))
        return

    if args.preset:
        if not installer.load_preset(args.preset):
            print(color(f"Preset not found: {args.preset}", Colors.RED))
            print("Available presets:")
            for preset in installer.catalog.get('presets', []):
                print(f"  - {preset['id']}")
            return

        # Determine target
        if args.target == 'claude-code':
            target_path = installer.claude_code_global
        elif args.target == 'claude-desktop':
            target_path = installer.get_claude_desktop_path()
        elif args.target == 'both':
            target_path = (installer.claude_code_global, installer.get_claude_desktop_path())
        else:
            target_path = Path.cwd() / '.claude'

        installer.print_banner()
        print(f"Installing preset: {args.preset}")

        if args.target == 'both':
            code_target, desktop_target = target_path
            if code_target:
                installer.do_install(code_target, 'claude-code', args.mode)
            if desktop_target:
                installer.do_install(desktop_target, 'claude-desktop', args.mode)
        else:
            installer.do_install(target_path, args.target, args.mode)

        print(color("\nInstallation complete!", Colors.GREEN + Colors.BOLD))
        return

    # Interactive mode
    installer.run_interactive()


if __name__ == '__main__':
    main()

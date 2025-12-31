# Notification Hook

## Overview

Sends desktop notifications when Claude completes tasks or encounters errors. Useful for long-running operations so you can work on other things.

## Security Disclosure

**Security Level:** LOW

**Commands executed:**
```bash
# macOS:
osascript -e 'display notification "Task completed" with title "Claude Code"'

# Linux (requires libnotify):
notify-send "Claude Code" "Task completed"
```

**Trigger conditions:** When Claude's task stops (Stop event)

**File access:** None

**Network access:** None

**Risk assessment:**
This hook is classified as LOW risk because:
- Only sends local desktop notifications
- No file access
- No network access
- Uses built-in OS notification systems

## Configuration

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$OSTYPE\" == \"darwin\"* ]]; then osascript -e 'display notification \"Claude has completed the task\" with title \"Claude Code\" sound name \"Glass\"'; elif command -v notify-send &> /dev/null; then notify-send 'Claude Code' 'Claude has completed the task'; fi"
          }
        ]
      }
    ]
  }
}
```

### With Custom Sound (macOS)

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Task completed\" with title \"Claude Code\" sound name \"Ping\"'"
          }
        ]
      }
    ]
  }
}
```

### Error Notifications

To also notify on errors:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$STOP_REASON\" == \"error\" ]]; then osascript -e 'display notification \"Error occurred\" with title \"Claude Code\" sound name \"Basso\"'; else osascript -e 'display notification \"Task completed\" with title \"Claude Code\" sound name \"Glass\"'; fi"
          }
        ]
      }
    ]
  }
}
```

## Requirements

### macOS
Built-in - uses `osascript` which is pre-installed.

### Linux
Install libnotify:
```bash
# Debian/Ubuntu
sudo apt install libnotify-bin

# Fedora
sudo dnf install libnotify

# Arch
sudo pacman -S libnotify
```

### Windows
Use PowerShell toast notifications (modify command accordingly).

## Customization

### Available macOS Sounds
- Basso
- Blow
- Bottle
- Frog
- Funk
- Glass
- Hero
- Morse
- Ping
- Pop
- Purr
- Sosumi
- Submarine
- Tink

### Custom Notification Content

You can include task context in the notification:

```bash
osascript -e 'display notification "Finished processing $FILE_COUNT files" with title "Claude Code"'
```

## Troubleshooting

### Notifications not appearing (macOS)

1. Check System Preferences > Notifications > Script Editor
2. Ensure notifications are enabled
3. Check Do Not Disturb is off

### Notifications not appearing (Linux)

1. Verify `notify-send` is installed: `which notify-send`
2. Check notification daemon is running
3. Try running `notify-send "test"` manually

## Author

Claude Code Community

## Version History

- 1.0.0: Initial release with macOS and Linux support

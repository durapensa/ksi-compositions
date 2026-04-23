---
component_type: behavior
name: claude_code_sandbox
version: 1.0.0
description: Claude Code-specific sandbox conventions - tool preferences, session behavior, permission handling
author: ksi_system
---

# Claude Code Sandbox Conventions

These are specific to your Claude Code execution environment.

## Tool Preferences

Claude Code provides dedicated tools that are more effective than their shell equivalents:

- **Read files** with the Read tool rather than `cat`, `head`, or `tail`
- **Edit files** with the Edit tool rather than `sed` or `awk`
- **Create files** with the Write tool rather than `echo` or heredocs
- **Search files** with Glob (by name) or Grep (by content) rather than `find` or `grep`
- **Use Bash** for actual shell operations — running KSI commands, git, scripts, etc.

## Your Sandbox

Your working directory is an ephemeral sandbox created for this session. You have full read/write access within it. Files you create here will not persist beyond your session unless you explicitly store them through KSI's state or component systems.

## KSI Commands

KSI CLI commands are run through Bash:
```bash
ksi discover
ksi send agent:list
ksi send completion:async --agent-id <id> --prompt "message"
```

These are your primary interface to the broader KSI environment.

---
name: hook-manager
description: |
  Manage Claude Code hooks: create, modify, delete, enable/disable.
  Trigger: "hook 만들어줘", "hook 추가", "hook 삭제", "hook 켜줘/꺼줘",
  "hook 목록", "hooks 관리", "hook enable/disable", "create a hook",
  "add hook", "remove hook", "toggle hook", "list hooks"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Hook Manager

Manage Claude Code hooks with registry-based toggle control.

## Intent Routing

1. **Q&A** (질문, 설명 요청, 탐색): Refer to [references/hook-guide.md](references/hook-guide.md) and answer
2. **Task** (생성, 수정, 삭제, 토글): Execute the matching action below

## Actions

Determine the user's intent and execute one of the 7 actions below.
When invoked via slash command without clear intent, use `AskUserQuestion` to ask which action.

Default settings target: `.claude/settings.local.json` (project-local, not tracked by git).
See [hook-guide.md §5](references/hook-guide.md) for all settings file locations.

### 1. list

Display all hooks (managed + unmanaged) with their status.

**Steps:**

1. Read `.claude/hooks/registry.json` if exists — this is the source of truth for managed hooks
2. Read settings files (local → project → user) using `Read` tool — extract all active hooks
3. Cross-reference registry vs settings:
   - `status: "enabled"` but hook missing in settings → mark as **orphaned** and warn user
   - `status: "disabled"` and hook absent in settings → normal (expected)
4. Identify unmanaged hooks: hooks in settings that have no matching registry entry
5. Output a table:

```markdown
| # | Event | Matcher | Type | Name | Status |
|---|-------|---------|------|------|--------|
| 1 | PostToolUse | Edit|Write | command | FORMAT | enabled |
| 2 | PreToolUse | Bash | command | BLOCKDANGER | disabled |
| 3 | Stop | (all) | agent | TESTGATE | enabled |
| 4 | Notification | (all) | command | — | unmanaged |
```

- **enabled**: registry `status: "enabled"` and hook exists in settings
- **disabled**: registry `status: "disabled"` and hook removed from settings
- **orphaned**: registry `status: "enabled"` but hook missing in settings — suggest `enable` to restore or `delete` to clean up
- **unmanaged**: hook exists in settings but not tracked in registry

### 2. create

Create a new hook and register it.

**Steps:**

1. Ask user via `AskUserQuestion` (batch into 1-2 questions):
   - **Event**: which lifecycle event (e.g., PostToolUse, PreToolUse, Stop)
   - **Matcher**: regex pattern (e.g., `Edit|Write`, `Bash`, empty for all)
   - **Handler type**: command, prompt, or agent
   - **Command/prompt**: the actual handler content
   - **Name**: short uppercase identifier (e.g., `FORMAT`, `BLOCKDANGER`) — must be unique in registry
   - **Description**: one-line summary of what this hook does (e.g., "Auto-format files after editing", "Block dangerous shell commands")
   - **Use recipe?**: offer to pick from [hook-recipes.md](references/hook-recipes.md)

2. Validate name: read registry and check for duplicate name (case-insensitive). If duplicate, ask user for a different name.
3. Insert hook into target settings file (`hooks` section):
   - Always include `description` field in the matcher group
   - If the same `event` + `matcher` group already exists → append to its `hooks` array
   - If the `event` key exists but matcher differs → add a new matcher group (with `description`)
   - If the `event` key doesn't exist → create the event key with a new matcher group (with `description`)
4. Add entry to `.claude/hooks/registry.json` (create file if absent):
   ```json
   {
     "NAME": {
       "event": "PostToolUse",
       "matcher": "Edit|Write",
       "status": "enabled",
       "settingsFile": ".claude/settings.local.json",
       "hookEntry": { ... }
     }
   }
   ```
5. If command handler requires multi-line logic (see "Inline vs Shell Script" criteria):
   - Create `.claude/hooks/handlers/{name}.sh` (lowercase of NAME)
   - Add `#!/bin/bash` shebang, write the script content
   - Run `chmod +x` on the file
   - Set the hook's `command` field to `.claude/hooks/handlers/{name}.sh`
6. Show the created hook summary

### 3. modify

Edit an existing hook's configuration. Only managed hooks (tracked in registry) can be modified.

**Steps:**

1. Run the **list** action to show current hooks
2. Ask which hook to modify (by number or name) — if user picks an **unmanaged** hook, offer to register it first via `create` flow, then modify
3. Ask what to change: command, matcher, timeout, handler type, etc.
4. If **event or matcher** is changed and hook is enabled:
   - Remove hook from old location in settings (clean up empty containers)
   - Insert hook at new location (follow same insertion logic as `create` step 3)
   - Update registry's `event`, `matcher`, and `hookEntry`
5. If only **hookEntry fields** change (command, timeout, etc.):
   - If hook is **enabled**: update both settings file and registry `hookEntry` using `Edit` tool
   - If hook is **disabled**: update only registry `hookEntry` (settings has no entry to update)
6. Show the modified hook summary

### 4. delete

Remove a hook completely.

**Steps:**

1. Run the **list** action to show current hooks
2. Ask which hook to delete (by number or name)
3. If hook is **enabled**: remove the hook entry from settings `hooks` section, clean up empty event array or matcher group
4. If hook is **disabled**: skip settings removal (hook is already absent from settings)
5. If `.claude/hooks/handlers/{name}.sh` exists, delete it
6. Remove the entry from `.claude/hooks/registry.json`
7. Delete registry file if empty after removal
8. Show confirmation

### 5. enable

Activate a disabled hook. All handler types use the same flow.

**Steps:**

1. Read `.claude/hooks/registry.json` — if file not found, report "no managed hooks" and stop
2. Find the entry by name — if not found or already `enabled`, report and stop
3. Re-insert `hookEntry` into the settings file `hooks` section:
   - If the same `event` + `matcher` group exists → append to its `hooks` array
   - If the `event` key exists but matcher differs → add a new matcher group
   - If the `event` key doesn't exist → create the event key with a new matcher group
   - If the settings file doesn't exist → report error and stop
4. Update registry: change `status` from `"disabled"` to `"enabled"`
5. Confirm with the restored hook summary

### 6. disable

Deactivate a hook. All handler types use the same flow.

**Steps:**

1. Read `.claude/hooks/registry.json` — if not found or entry not found, report and stop
2. Check registry entry status — if already `"disabled"`, report "already disabled" and stop
3. Find the hook entry in the settings file `hooks` section using registry's `event` and `matcher`
4. Remove the hook entry from the settings file
5. If event array or matcher group becomes empty, clean up empty containers
6. Update registry: change `status` from `"enabled"` to `"disabled"`
7. Confirm: `NAME disabled (entry preserved in registry)`

## File Layout

```
.claude/hooks/
├── registry.json          # Hook registry (source of truth)
└── handlers/              # Shell scripts for multi-line hooks
    ├── format.sh
    └── blockdanger.sh
```

- **Registry**: `.claude/hooks/registry.json`
- **Shell scripts**: `.claude/hooks/handlers/{name}.sh` (lowercase of registry NAME)

### Inline vs Shell Script

| Condition | Use inline | Use .sh file |
|-----------|-----------|-------------|
| Single command | `afplay /System/Library/Sounds/Glass.aiff` | — |
| Simple pipe | `jq -r '.file' \| xargs prettier --write` | — |
| Conditionals / loops | — | `if`, `for`, `while` |
| Multi-line logic (2+ lines) | — | Always |
| Complex stdin parsing | — | Multiple `jq` extractions |

**Rule: if it fits naturally in one line, inline. Otherwise, create a .sh file.**

When creating a .sh file:
1. Save to `.claude/hooks/handlers/{name}.sh`
2. Add shebang `#!/bin/bash` as first line
3. Run `chmod +x` on the file
4. Reference in settings as `.claude/hooks/handlers/{name}.sh`

## Hook JSON Structure Reference

```json
{
  "hooks": {
    "<Event>": [
      {
        "description": "One-line summary of what this hook does",
        "matcher": "<regex>",
        "hooks": [
          {
            "type": "command",
            "command": "<shell command>",
            "timeout": 600,
            "async": false
          }
        ]
      }
    ]
  }
}
```

**Required fields:**

| Field | Description |
|-------|-------------|
| `description` | One-line summary of the hook's purpose. Not an official field, but always include it for maintainability. |

**Optional fields** (set only when user requests):

| Field | Default | Description |
|-------|---------|-------------|
| `timeout` | 600 (cmd), 30 (prompt), 60 (agent) | Seconds before timeout |
| `async` | false | Run in background (command only) |
| `statusMessage` | - | Spinner text during execution |
| `once` | false | Run once per session (skill hooks only) |

## Registry File

All managed hooks are tracked in `.claude/hooks/registry.json`.
Shell scripts are stored in `.claude/hooks/handlers/`.
This file is the single source of truth for hook status and metadata.

**Structure:**

```json
{
  "FORMAT": {
    "event": "PostToolUse",
    "matcher": "Edit|Write",
    "status": "enabled",
    "settingsFile": ".claude/settings.local.json",
    "hookEntry": {
      "type": "command",
      "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true",
      "timeout": 30
    }
  },
  "TESTGATE": {
    "event": "Stop",
    "matcher": "",
    "status": "disabled",
    "settingsFile": ".claude/settings.local.json",
    "hookEntry": {
      "type": "agent",
      "prompt": "Run tests and verify all tests pass. $ARGUMENTS",
      "timeout": 120
    }
  }
}
```

**Fields:**

| Field | Description |
|-------|-------------|
| `key` (top-level) | User-chosen NAME in uppercase. Must be unique. |
| `event` | Hook lifecycle event (e.g., PostToolUse, PreToolUse, Stop) |
| `matcher` | Regex pattern for filtering. Empty string = match all. |
| `status` | `"enabled"` (active in settings) or `"disabled"` (removed from settings) |
| `settingsFile` | Path to the settings file this hook belongs to |
| `hookEntry` | The exact hook handler object (always preserved for restore/reference) |

**Lifecycle:**

```
hook 없음
  │
  ├─ create → settings에 hook 삽입 + registry에 {status: "enabled"} 추가
  │
  ├─ disable → settings에서 hook 제거 + registry status → "disabled"
  │
  ├─ enable → settings에 hook 복원 + registry status → "enabled"
  │
  └─ delete → settings에서 hook 제거 + registry 엔트리 삭제
```

This file is gitignored (project-local state). It is created on first `create` or `disable` and deleted when the last entry is removed.

## Recipes

When the user wants a common hook pattern, offer recipes from
[references/hook-recipes.md](references/hook-recipes.md).

Present the recipe list and let the user pick. Then create the hook
using the recipe's pre-configured values through the standard create flow.

## Important Rules

1. **Read before edit**: Always read the target settings file before modifying
2. **Preserve structure**: Use `Edit` tool for surgical changes, never rewrite the entire file
3. **Valid JSON**: Ensure the output is valid JSON after every edit
4. **No migration**: Do not touch pre-existing hooks not tracked in the registry
5. **One settings file**: Each operation targets a single settings file (default: `settings.local.json`)
6. **Confirm destructive actions**: Ask before delete operations
7. **Registry hygiene**: When deleting a hook, always remove its registry entry. Delete registry file if empty.
8. **Unified toggle**: All types (command, prompt, agent) use the same enable/disable flow — remove/restore entry + registry status update
9. **Name uniqueness**: Reject duplicate names on create. Names are case-insensitive for comparison but stored uppercase.
10. **Handler scripts**: When deleting a hook, also delete its `.claude/hooks/handlers/{name}.sh` if it exists.

# Hook Recipes

Pre-configured hook patterns ready to deploy. Each recipe includes the event,
matcher, handler type, registry name, and command.

---

## 1. auto-format — Auto-format on file edit

| Field | Value |
|-------|-------|
| Event | `PostToolUse` |
| Matcher | `Edit\|Write` |
| Handler | command |
| Name | `FORMAT` |

**Command:**

```bash
jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true
```

**Variants:**

- Python (Black): `jq -r '.tool_input.file_path' | xargs black 2>/dev/null || true`
- Ruff: `jq -r '.tool_input.file_path' | xargs ruff format 2>/dev/null || true`

**Generated JSON:**

```json
{
  "matcher": "Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true",
    "timeout": 30
  }]
}
```

---

## 2. block-danger — Block destructive commands

| Field | Value |
|-------|-------|
| Event | `PreToolUse` |
| Matcher | `Bash` |
| Handler | command |
| Name | `BLOCKDANGER` |

**Command:**

```bash
CMD=$(jq -r '.tool_input.command'); if echo "$CMD" | grep -qE 'rm\s+-rf|DROP\s+TABLE|TRUNCATE\s+TABLE|git\s+push\s+.*--force'; then echo "Blocked: destructive command" >&2; exit 2; fi
```

**Generated JSON:**

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "CMD=$(jq -r '.tool_input.command'); if echo \"$CMD\" | grep -qE 'rm\\s+-rf|DROP\\s+TABLE|TRUNCATE\\s+TABLE|git\\s+push\\s+.*--force'; then echo 'Blocked: destructive command' >&2; exit 2; fi"
  }]
}
```

---

## 3. protect-files — Prevent editing protected files

| Field | Value |
|-------|-------|
| Event | `PreToolUse` |
| Matcher | `Edit\|Write` |
| Handler | command |
| Name | `PROTECTFILES` |

**Command:**

```bash
FILE=$(jq -r '.tool_input.file_path'); for p in .env .env.local package-lock.json .git/; do case "$FILE" in *"$p"*) echo "Protected: $FILE" >&2; exit 2;; esac; done
```

**Generated JSON:**

```json
{
  "matcher": "Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "FILE=$(jq -r '.tool_input.file_path'); for p in .env .env.local package-lock.json .git/; do case \"$FILE\" in *\"$p\"*) echo \"Protected: $FILE\" >&2; exit 2;; esac; done"
  }]
}
```

---

## 4. desktop-notify — OS desktop notifications

| Field | Value |
|-------|-------|
| Event | `Notification` |
| Matcher | (empty — all notifications) |
| Handler | command |
| Name | `DESKTOP` |

**Command (macOS):**

```bash
osascript -e 'display notification "Claude Code needs attention" with title "Claude Code"'
```

**Command (Linux):**

```bash
notify-send 'Claude Code' 'Needs attention'
```

**Generated JSON (cross-platform):**

```json
{
  "matcher": "",
  "hooks": [{
    "type": "command",
    "command": "if [ \"$(uname)\" = \"Darwin\" ]; then osascript -e 'display notification \"Claude Code needs attention\" with title \"Claude Code\"'; else notify-send 'Claude Code' 'Needs attention'; fi"
  }]
}
```

---

## 5. test-gate — Enforce tests before stop

| Field | Value |
|-------|-------|
| Event | `Stop` |
| Matcher | (empty — always fires) |
| Handler | agent |
| Name | `TESTGATE` |

**Generated JSON:**

```json
{
  "hooks": [{
    "type": "agent",
    "prompt": "Check if the stop is appropriate. Context: $ARGUMENTS\n\n1. Look at the conversation to understand what was requested\n2. Run the test suite to verify all tests pass\n3. If tests fail, respond with {\"ok\": false, \"reason\": \"Tests failing: ...\"}\n4. If all good, respond with {\"ok\": true}",
    "timeout": 120
  }]
}
```

---

## 6. env-loader — Load .env on session start

| Field | Value |
|-------|-------|
| Event | `SessionStart` |
| Matcher | `startup` |
| Handler | command |
| Name | `ENVLOADER` |

**Command:**

```bash
if [ -f .env ] && [ -n "$CLAUDE_ENV_FILE" ]; then grep -v '^#' .env | grep '=' >> "$CLAUDE_ENV_FILE"; fi
```

**Generated JSON:**

```json
{
  "matcher": "startup",
  "hooks": [{
    "type": "command",
    "command": "if [ -f .env ] && [ -n \"$CLAUDE_ENV_FILE\" ]; then grep -v '^#' .env | grep '=' >> \"$CLAUDE_ENV_FILE\"; fi"
  }]
}
```

---

## 7. compact-restore — Restore context after compact

| Field | Value |
|-------|-------|
| Event | `SessionStart` |
| Matcher | `compact` |
| Handler | command |
| Name | `COMPACTRESTORE` |

**Command:**

```bash
echo "[Context restored] <custom message here>"
```

**Dynamic variant (with git info):**

```bash
BRANCH=$(git branch --show-current 2>/dev/null); RECENT=$(git log --oneline -3 2>/dev/null); echo "Branch: $BRANCH | Recent: $RECENT"
```

**Generated JSON:**

```json
{
  "matcher": "compact",
  "hooks": [{
    "type": "command",
    "command": "echo '[Context restored] Use bun (not npm). Run tests before commits.'"
  }]
}
```

---

## 8. bash-audit — Log all Bash commands

| Field | Value |
|-------|-------|
| Event | `PostToolUse` |
| Matcher | `Bash` |
| Handler | command |
| Name | `BASHAUDIT` |

**Command:**

```bash
jq -r '[.session_id, (.tool_input.command // "N/A")] | @tsv' >> /tmp/claude-bash-audit.log
```

**Generated JSON:**

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "jq -r '[.session_id, (.tool_input.command // \"N/A\")] | @tsv' >> /tmp/claude-bash-audit.log",
    "async": true
  }]
}
```

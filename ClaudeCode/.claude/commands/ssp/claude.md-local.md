---
allowed-tools: Read, Write, Glob, Grep, Bash(git:*), Bash(ls:*), Bash(wc:*)
description: "Create CLAUDE.local.md as a session context manager for the project"
argument-hint: "<session goal description> or 'rolling <project description>'"
---

# Create CLAUDE.local.md — Session Context Manager

## Input

- **Target**: `CLAUDE.local.md` at the project root.
- **Mode**: Determined by `$ARGUMENTS`:
  - Starts with `rolling` → **Rolling mode** (remaining text = operational description)
  - Otherwise → **Session mode** (entire text = session goal)

> Examples:
>
> - `/ssp:claude.md-local implement user authentication` → Session mode
> - `/ssp:claude.md-local migrate REST API to GraphQL` → Session mode
> - `/ssp:claude.md-local rolling continuous improvement project` → Rolling mode
> - `/ssp:claude.md-local rolling multi-project maintenance` → Rolling mode

---

## Step 1: Assess the Environment

1. Locate the project root (`git rev-parse --show-toplevel` or nearest `CLAUDE.md`)
2. Check if `CLAUDE.local.md` already exists
   - **Exists**: Read its contents and ask the user — overwrite or abort
   - **Does not exist**: Proceed
3. Read the root `CLAUDE.md` — extract project name, key structure, and context
4. Check current git branch and recent 3 commits (working context)

---

## Step 2: Determine Mode and Gather Information

**Mode determination:**

- `$ARGUMENTS` starts with `rolling` → **Rolling mode**
- All other cases → **Session mode**

**Information to gather** from `CLAUDE.md` and project structure:

- Project name (from CLAUDE.md heading or directory name)
- Key modules and directory structure
- For Session mode: infer directories/files relevant to the goal

---

## Step 3: Generate CLAUDE.local.md

Create the file using the appropriate template based on the determined mode.
Replace all `{placeholder}` values with actual information gathered in Steps 1–2.

### Session Mode Template

Use this template when the user has a specific goal (feature, migration, refactoring, etc.).

```markdown
# {Project Name} — {Session Goal Summary}

> Last updated: {YYYY-MM-DD}

---

## Session Goal

- **Goal**: {extracted from $ARGUMENTS}
- **Scope**: {relevant directories/modules — inferred from CLAUDE.md}
- **Success criteria**: {completion conditions — inferred or "TBD"}

---

## Recent Changes

> Keep only the latest 3–5 entries. Remove older items.

_(Session started — no changes yet)_

---

## Progress

### Completed

_(None yet)_

### In Progress

_(Awaiting session start)_

### Next Steps

1. {Suggest first concrete step based on CLAUDE.md analysis}

---

## Decisions

> Record architectural/implementation decisions made during the session and their rationale.

_(None yet)_

---

## Blockers & Dependencies

_(None yet)_

---

## Lessons Learned

> Record failed approaches, corrected strategies, and discovered gotchas.

_(None yet)_
```

### Rolling Mode Template

Use this template for long-running projects that accumulate context continuously without resetting.

```markdown
# {Project Name} — Operational Context

> Last updated: {YYYY-MM-DD}

{Operational policy description — from text after "rolling" in $ARGUMENTS, or inferred from project nature. 1–2 sentences.}

---

## Recent Changes

> Keep only the latest 3–5 entries. Remove older items.

_(Operations started — no changes yet)_

---

## Backlog

> Record improvements discovered during work.
> Format: `[source] description — target file/module`

_(None currently)_

---

## Known Issues

_(None currently)_

---

## Pending Decisions

_(None currently)_

---

## Design Decisions

> Reference these when the same question arises in future sessions.

_(None yet)_
```

### Template Rules

- All `{placeholder}` values must be replaced with actual information — never leave raw placeholders
- When inference is uncertain, write "TBD (needs confirmation)"
- Keep empty-section placeholders (`_(None yet)_`, etc.) as-is from the template
- Target file size: **≤ 80 lines** (content accumulates later via `claude.md-update`)

---

## Step 4: Verify .gitignore

Check whether the project root `.gitignore` includes `CLAUDE.local.md`.

- **Included**: Confirmed (likely auto-added by Claude Code)
- **Not included**: Note in the report that manual addition is recommended (do not modify `.gitignore` directly)

---

## Step 5: Report

After generation, report the following:

1. Generated file path and line count
2. Applied mode (Session / Rolling)
3. List of sections included
4. `.gitignore` status
5. Next action guidance:
   - Session mode: "Run `/ssp:claude.md-update` after making progress to update session context"
   - Rolling mode: "Run `/ssp:claude.md-update` when changes occur to accumulate records"

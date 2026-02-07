---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Bash(wc:*)
description: Consolidate session learnings into auto memory with intelligent file management
argument-hint: '[optional: topic, "full", "cleanup", or "stats"]'
---

# Update Auto Memory

## Overview

You, Claude Code, have a **persistent auto memory directory** that survives across conversations.
This command triggers a structured review of the current session and consolidates learnings into your auto memory files.

**Auto Memory Location**: `~/.claude/projects/{project-path-encoded}/memory/`

To find YOUR auto memory path for this project, look for the line in your system prompt:
> "You have a persistent auto memory directory at `/Users/.../.claude/projects/.../memory/`"

Use that exact path. Do NOT guess or construct the path yourself.

---

## User-Specified Focus

`$ARGUMENTS`

| Argument | Behavior |
|----------|----------|
| (empty) | Full session review — extract, prune, deduplicate, and write |
| `full` | Same as empty |
| `{topic}` | Focus extraction and pruning on the specified topic only |
| `cleanup` | Skip extraction — only prune stale entries and reorganize |
| `stats` | Report current memory state only — no modifications |

---

## Step 1: Discover Current Memory State

1. Read `MEMORY.md` in your auto memory directory (it may not exist yet).
2. List all existing `.md` files in the memory directory.
3. Count the lines in `MEMORY.md` (if it exists).

If the memory directory does not exist, create it before proceeding.

Report what you found before proceeding.

If the argument is `stats`, report and **stop here**.

---

## Step 2: Extract Session Learnings

If the argument is `cleanup`, skip this step and proceed directly to Step 3.

Review the **entire current conversation** and identify items worth persisting. Categorize each item:

### Category A — Mistakes & Corrections

- Errors you made that were corrected (by user or by yourself)
- Wrong assumptions that led to failed attempts
- Tools or approaches that didn't work and why

### Category B — Discovered Patterns

- Project-specific patterns, conventions, or idioms
- Configuration quirks or environment-specific behavior
- Workarounds for known limitations

### Category C — Key Facts

- Important file paths, versions, or architecture decisions
- API behaviors, schema constraints, or runtime requirements
- Dependencies between components

### Category D — Operational Knowledge

- Commands that work (or don't) in this environment
- Build/deploy/test procedures learned
- Troubleshooting steps that resolved issues

### Exclusions — Do NOT Record

- Rules or conventions already stated in `CLAUDE.md` or `CLAUDE.local.md`
- One-off debugging commands unlikely to be reused
- Simple typo fixes or other low-recurrence corrections

For each item, write a **one-line summary** (max 120 chars) and note its category.

If no learnings are found, report "No new learnings to record" and continue to Step 3 (pruning may still apply).

---

## Step 3: Prune Stale Entries

Review all existing entries in `MEMORY.md` and topic files against the current session context:

1. **Contradicted**: Entry was disproven or corrected during this session → delete or update.
2. **Obsolete**: Entry references code, patterns, or tools that no longer exist → delete.
3. **Superseded**: A newer, more accurate entry covers the same ground → merge or delete the older one.

For each pruned item, note what was removed and why.

If no stale entries are found, report "No stale entries found" and proceed.

---

## Step 4: Deduplicate Against Existing Memory

For each extracted learning:

1. Check if `MEMORY.md` or any topic file already covers it.
2. If already covered → skip (or update if the new info is more accurate).
3. If new → mark for insertion.

Report the dedup results: how many new, how many skipped, how many updated.

---

## Step 5: Decide File Placement

Apply these rules:

### Rule 1: MEMORY.md is the Index (max 200 lines)

- Contains **concise summaries only** (1-2 lines per item)
- Organized by **topic sections** (not chronologically)
- Links to detail files when a topic exceeds 5 items

### Rule 2: Topic Files for Depth

- Create a topic file when a section in MEMORY.md accumulates **more than 5 items**
- File naming: `{topic-slug}.md` (e.g., `settings-quirks.md`, `gateway-ops.md`, `build-debug.md`)
- Move detailed notes to the topic file, keep only a summary + link in MEMORY.md

### Rule 3: Topic File Merge-Back

- If a topic file shrinks to **3 items or fewer** (due to pruning), merge its contents back into MEMORY.md and delete the topic file

### Rule 4: MEMORY.md Section Format

```markdown
## {Topic Name}
- Key point one (concise)
- Key point two (concise)
- See [detailed notes](./{topic-slug}.md) for more
```

### Rule 5: Topic File Format

```markdown
# {Topic Name} — Detailed Notes

## {Subtopic}
- **Context**: What happened
- **Learning**: What to remember
- **Action**: What to do differently

## {Subtopic}
...
```

### Rule 6: Line Budget Management

- Before writing, count current MEMORY.md lines
- If adding new items would exceed 180 lines → extract the largest section into a topic file first
- Always leave ~20 lines of buffer (target: 180 lines max)

---

## Step 6: Write Changes

1. If `MEMORY.md` doesn't exist → create it with a header and the new items.
2. If it exists → use Edit to insert/update items in the correct section.
3. If a topic file is needed → create it with Write, then update the MEMORY.md link.

### MEMORY.md Header Template (for new files only)

```markdown
# Auto Memory — {Project Name}

> Last updated: {YYYY-MM-DD}
> This file is auto-loaded into the system prompt every session. Keep it concise.

---

{sections go here}
```

---

## Step 7: Validate & Report

After writing:

1. Count the final line count of MEMORY.md.
2. List all memory files with their line counts.
3. Report a summary:

```markdown
## Auto Memory Update Complete

| Metric | Value |
|--------|-------|
| New items added | N |
| Items updated | N |
| Items pruned | N |
| Items skipped (duplicate) | N |
| MEMORY.md lines | N / 200 |
| Topic files | N |

### What was recorded:
- (brief list of recorded items)

### What was pruned:
- (brief list of pruned items, or "None")
```

---

## Important Principles

- **Semantic organization**: Group by topic, NOT by date or session.
- **Conciseness over completeness**: One clear sentence beats a detailed paragraph.
- **Actionable over descriptive**: "Use Write tool to bypass settings validation" beats "The Edit tool validates settings".
- **Correct over persistent**: If a previous memory entry is wrong, update or delete it.
- **No sensitive data**: Never store API keys, tokens, passwords, or personal identifiers.

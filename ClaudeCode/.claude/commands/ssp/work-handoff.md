---
allowed-tools: Read, Grep, Glob, Bash, Task, Write
argument-hint: "[focus area] [save: to save file]"
description: Generate a focused handoff document for the next session to continue work seamlessly
---


## User-Specified Focus Area

`$ARGUMENTS`

---

## Generation Instructions

Analyze the above context along with the **entire current conversation** to produce a handoff document in the format below.

## Handoff Document Template

Write the handoff document in **markdown format** following the structure below.
Include only sections that have relevant content from this session.

---

```markdown

# 📋 Session Handoff Document

- **Date**: YYYY-MM-DD HH:MM
- **Topic**: [Main topic of this session (1-2 sentences)]

# 📌 Executive Summary
[Summarize the key accomplishments and outcomes of this session in 2-3 sentences]

# ⏭️ Immediate Next Steps
[The specific task in progress and exact next actions to take]

# 🔑 Key Decisions & Rationale
- [Decision made] — **Why**: [reason, tradeoff, or constraint that led to this choice]
- [User preferences or requirements discovered]

# 🚫 Dead Ends & Lessons
- [What was tried and failed] — **Cause**: [why it didn't work]
- [Workarounds discovered during troubleshooting]
(Omit this section if nothing failed)

# 📁 Changed Files
- `path/to/file` — [what changed and why]
- `path/to/file` — [what changed and why]

# 🌐 Environment State
- **Branch**: [current git branch]
- **Uncommitted changes**: [yes/no, brief summary]
- **Active subscription/venv/config**: [relevant env context]
(Omit this section if no notable env state)

# 📊 Current State
- Completed: [what's done]
- In Progress: [what's partially done]
- Remaining: [what's left to do]

# ⚠️ Critical Notes
- [Blockers, dependencies, or known issues]
- [Warnings the next session must know about]
- **Memory updated**: [yes/no — topic files updated during this session, if any]

**⏸️ Do NOT start implementation. Wait for explicit instruction.**

```

## Writing Principles

1. **Immediately Actionable**: The next agent should be able to resume work after reading this
2. **Specific Over Abstract**: Use actual file paths, function names, and shell commands
3. **Why Over What**: For decisions and file changes, always include the reason — not just what happened
4. **Failures Are Valuable**: Dead ends prevent repeated mistakes — always record them
5. **No Duplication With Memory**: If something was already saved to auto memory, reference it instead of restating
6. **900 Words Max**: Compress to essentials, omit unnecessary background
7. **Priority First**: Place the most urgent items at the top
8. **Copy-Paste Ready**: The output should be directly usable as input for the next session

## Output Instructions

- **Default**: Output the handoff document to the conversation only (no file saved)
- **Save option**: If `$ARGUMENTS` contains `save`, output to conversation AND save to file
  - Path: `.handoff/HANDOFF-{TITLE}-{YYYY-MM-DD-HHMM}.md`
  - `{TITLE}`: Session topic summarized in UPPERCASE, hyphen-separated (e.g., `API-REFACTOR`, `AUTH-BUGFIX`)
  - `{YYYY-MM-DD-HHMM}`: Current date/time
  - Create `.handoff/` directory if it does not exist

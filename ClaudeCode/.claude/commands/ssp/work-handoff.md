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
- **Topic**: [Main topic of this session(1~2 stentences)]

# 📌 Executive Summary
[Summarize the key accomplishments and outcomes of this session in 2-3 sentences]

# ⏭️ Immediate Next Steps
[The specific task in progress and exact next actions to take]

# 🔑 Key Context
- [Major decisions made in this session]
- [Established patterns, conventions, or constraints]
- [User preferences or requirements discovered]

# 📁 Relevant Files
- [File paths that matter for continuing the work]

# 📊 Current State
- Completed: [what's done]
- In Progress: [what's partially done]
- Remaining: [what's left to do]

# ⚠️ Critical Notes
- [Blockers, dependencies, or known issues]
- [Warnings the next session must know about]
```

## Writing Principles

1. **Immediately Actionable**: The next agent should be able to resume work after reading this
2. **Specific Over Abstract**: Use actual file paths, function names, and shell commands
3. **600 Words Max**: Compress to essentials, omit unnecessary background
4. **Priority First**: Place the most urgent items at the top
5. **Copy-Paste Ready**: The output should be directly usable as input for the next session

## Output Instructions

- **Default**: Output the handoff document to the conversation only (no file saved)
- **Save option**: If `$ARGUMENTS` contains `save`, output to conversation AND save to file
  - Path: `.handoff/HANDOFF-{TITLE}-{YYYY-MM-DD-HHMM}.md`
  - `{TITLE}`: Session topic summarized in UPPERCASE, hyphen-separated (e.g., `API-REFACTOR`, `AUTH-BUGFIX`)
  - `{YYYY-MM-DD-HHMM}`: Current date/time
  - Create `.handoff/` directory if it does not exist

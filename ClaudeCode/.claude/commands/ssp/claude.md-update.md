---
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git:*), Bash(ls:*), Bash(wc:*)
description: Update CLAUDE Files with Relevant Knowledge from This Session
argument-hint: "[project-name]"
---

# Update CLAUDE Files with Relevant Knowledge from This Session

## Memory File System Overview

You, Claude Code, manage persistent memory using two main file types: `CLAUDE.md` for shared project structure and guidelines, and `CLAUDE.local.md` for session-specific context. The system recursively searches upward from the current working directory to load all relevant files, ensuring both project-level documentation and current session state are available.

### File Types & Roles

- **`CLAUDE.md` — "What the project IS"** (relatively static)
  - Located in the repository root or any working directory
  - Checked into version control for team-wide knowledge sharing
  - Contains: directory organization, file roles, architecture patterns, coding standards, shared guidelines
  - Updated when project structure changes or important decisions are made

- **`CLAUDE.local.md` — "What I'm DOING"** (highly dynamic)
  - Placed alongside working files, excluded from version control (`.gitignore`)
  - Functions as a **session context manager** — a "session" is a continuous work stream toward a specific goal (feature, migration, refactoring, etc.) that may span multiple days and Claude Code conversations
  - Persists across multiple conversations until the goal is achieved, then reset for the next session
  - Claude should immediately understand "where we left off", "what was tried", and "what comes next" from this file alone
  - **Contains:**
    - **Goal & Scope**: what this session aims to achieve
    - **Progress Tracking**: completed milestones, in-progress work, remaining tasks
    - **Decisions & Rationale**: architectural choices made during the session and why
    - **Lessons Learned**: what was tried and failed, corrected approaches, gotchas discovered
    - **Blockers & Dependencies**: unresolved issues, waiting-on items, external dependencies
    - **Next Steps**: concrete actions for the next conversation to pick up

- **Subdirectory `CLAUDE.md`** — scoped version of root `CLAUDE.md`
  - Loaded on-demand only when editing files in that subfolder
  - Contains module-specific structure, roles, and conventions

### Placement Decision Table

| This information is... | → Target File |
|------------------------|---------------|
| Project structure, directory roles, architecture patterns | **CLAUDE.md** (root) |
| Coding standards, build/test commands, shared guidelines | **CLAUDE.md** (root) |
| Recurring error patterns, corrected implementation details | **CLAUDE.md** (relevant section) |
| Specific to a single submodule's structure/roles/style | **subdirectory CLAUDE.md** |
| Session goal, scope definition, success criteria | **CLAUDE.local.md** |
| Currently in-progress tasks, active work items | **CLAUDE.local.md** |
| Completed milestones within current session | **CLAUDE.local.md** |
| Recent decisions with rationale, next steps, planned actions | **CLAUDE.local.md** |
| Failed approaches, corrected strategies, lessons learned | **CLAUDE.local.md** |
| Blockers, dependencies, waiting-on items | **CLAUDE.local.md** |

**Core rule**: Information that remains valid beyond the current session → `CLAUDE.md` / Information bound to a specific work stream (goal → completion) → `CLAUDE.local.md`

---

## Instructions

### Step 1: Discover Existing Files

1. Find all `CLAUDE.md` and `CLAUDE.local.md` files from the current directory up to the project root.
2. Read their contents and note the current line counts.
3. Report what you found before proceeding.

### Step 2: Identify Items to Record

Review the current session and identify items worth persisting. Triggers include:

- You learned something new about the project structure or conventions
- The user corrected you on an implementation detail or source code
- You struggled to find information and had to infer or look up details
- You lost track of the project structure during the session
- You identified a mistake in your own work
- The user made decisions about architecture, approach, or next steps
- Work was left incomplete and needs to be resumed

...that is relevant, was not known initially, and should be persisted.

### Step 3: Classify & Place Each Item

For each identified item, use the **Placement Decision Table** above to determine the correct file. When specific information belongs to a particular subcomponent, place it in the `CLAUDE.md` within that subdirectory.

For example:

- Information exclusively about a UI component → `apps/{component}-ui/CLAUDE.md`
- Information exclusively about an API component → `apps/{component}-api/CLAUDE.md`
- Information about infrastructure-as-code → `infrastructure/CLAUDE.md` or `cdk/CLAUDE.md`

### Step 4: Write Changes

**For `CLAUDE.md`** (project knowledge):

- Check for duplicates or contradictions with existing content before adding
- If existing content is outdated, update it rather than appending
- Group related information under logical sections

**For `CLAUDE.local.md`** (session context):

- **Accumulate, then prune** — build up context as the session progresses; when a milestone completes, move it to a brief "completed" summary and expand the next phase
- Completed items stay as concise summaries (proof of progress, not detailed logs)
- In-progress and upcoming items get full detail (enough for the next Claude to continue without asking)
- Structure so the next conversation's Claude can immediately resume work:
  - Session goal and current phase
  - What has been completed (brief summaries with key outcomes)
  - What is currently in progress (detailed context)
  - What comes next (concrete actionable steps)
  - What was tried and didn't work (avoid repeating mistakes)
  - Any pending decisions or blockers

### Step 5: Validate & Report

1. Verify final line counts:
   - `CLAUDE.md` (root): target **≤ 180 lines**. If exceeded, consider distributing to subdirectory files or compressing content.
   - `CLAUDE.local.md`: target **≤ 150 lines**. If exceeded, prune completed items.
   - Subdirectory `CLAUDE.md`: target **≤ 150 lines** each.
2. Report what was added, updated, or removed.

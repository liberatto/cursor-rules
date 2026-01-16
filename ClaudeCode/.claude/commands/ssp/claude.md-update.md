---
allowed-tools: Bash(git:*), Bash(ls:*), Bash(find:*)
description: Update CLAUDE Files with Relevant Knowledge from This Session
argument-hint: [project-name]
---

# Update CLAUDE Files with Relevant Knowledge from This Session

FYI: You, Claude Code, manage persistent memory using two main file types: `CLAUDE.md` for shared project structure and guidelines, and `CLAUDE.local.md` for session-specific context and personal notes. The system recursively searches upward from the current working directory to load all relevant `CLAUDE.md` and `CLAUDE.local.md` files, ensuring both project-level architecture documentation and current session state are available. Subdirectory `CLAUDE.md` and `CLAUDE.local.md` files are only loaded when working within those subfolders, keeping the active context focused and efficient.
Additionally, placing a `CLAUDE.md` in your home directory (e.g., `~/.claude/CLAUDE.md`) provides a global, cross-project memory that is merged into every session under your home directory.

**Summary of Memory File Behavior:**

- **Shared Project Structure (`CLAUDE.md`):**
  - Located in the repository root or any working directory
  - Checked into version control for team-wide knowledge sharing
  - Contains fixed, structural information: directory organization, file roles, architecture patterns, coding standards, shared guidelines
  - Manages documentation of new files/folders as they're added to the project
  - Updated when project structure changes or important team-wide decisions are made
  - Loaded recursively from the current directory up to the root

- **Session-Specific Context (`CLAUDE.local.md`):**
  - Placed alongside or above working files, excluded from version control
  - Stores dynamic, session-oriented information: current work status, active tasks, recent decisions, next steps, running processes
  - Functions as a "session checkpoint" - allowing seamless work resumption across sessions
  - Contains personal developer notes, temporary TODOs, and context-specific reminders
  - Maintains temporal project state (what was just completed, what's in progress, what's planned next)
  - Captures ADR (Architecture Decision Records) for the current work stream
  - Updated frequently during active development sessions
  - Enables Claude to immediately understand "where we left off" and "what comes next"
  - Loaded recursively like `CLAUDE.md`

- **On-Demand Subdirectory Loading:**
  - `CLAUDE.md` files in child folders are loaded only when editing files in those subfolders
  - Prevents unnecessary context bloat
  
- **Global User Memory (`~/.claude/CLAUDE.md`):**
  - Acts as a personal, cross-project memory
  - Automatically merged into sessions under your home directory

**Key Distinction:**

- `CLAUDE.md` = "What the project IS" (structure, roles, standards) - relatively static
- `CLAUDE.local.md` = "What I'm DOING" (current state, active work, next actions) - highly dynamic

---
**Instructions:**  
If during your session:

- You learned something new about the project
- I corrected you on a specific implementation detail
- I corrected source code you generated
- You struggled to find specific information and had to infer details about the project
- You lost track of the project structure and had to look up information in the source code
- You identified a mistake or error in your own work during the process
...that is relevant, was not known initially, and should be persisted, add it to the appropriate `CLAUDE.md` (for shared context) or `CLAUDE.local.md` (for private notes or project's session context) file. If the information is relevant for a subdirectory only, place or update it in the `CLAUDE.md` file within that subdirectory.
When specific information belongs to a particular subcomponent, ensure you place it in the CLAUDE file for that component.
For example:
- Information A belongs exclusively to the `heatsense-ui` component → put it in `apps/heatsense-ui/CLAUDE.md`
- Information B belongs exclusively to the `heatsense-api` component → put it in `apps/heatsense-api/CLAUDE.md`  
- Information C is infrastructure-as-code related → put it in `cdk/CLAUDE.md`
This ensures important knowledge is retained and available in future sessions.

---
allowed-tools: Bash(git:*), Bash(ls:*), Bash(find:*)
description: Review and update CLAUDE memory files across the project hierarchy
---

# Review and Update CLAUDE Memory Files

## Step 1: Discover Memory Files

List all `CLAUDE.md` and `CLAUDE.local.md` files from the current directory up to the project root.  
Include subdirectory files only when working inside those folders.

## Step 2: Review Each File

For every memory file:

- Load its content
- Compare documented details with the actual codebase
- Identify outdated, incorrect, missing, or duplicated information

## Step 3: Update and Reorganize

Apply corrections:

- Remove obsolete or incorrect statements  
- Add missing architectural or component-specific details  
- Consolidate duplicates  
- Ensure the information is stored in the correct file type and location  

### Placement Rules

- **Project-level knowledge → `CLAUDE.md`**  
  (architecture, module roles, standards)

- **Session-specific context → `CLAUDE.local.md`**  
  (current tasks, recent decisions, TODOs)

- **Component-specific details → subdirectory `CLAUDE.md`**  
  e.g.,  
  - UI → `apps/myproject-ui/CLAUDE.md`  
  - API → `apps/myproject-api/CLAUDE.md`  
  - IaC → `cdk/CLAUDE.md` or `infrastructure/CLAUDE.md`

Focus on clarity, accuracy, and relevance. Remove any information that no longer serves the project.

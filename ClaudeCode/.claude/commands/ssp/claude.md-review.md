---
allowed-tools: Read, Edit, Glob, Grep, Bash(git:*), Bash(ls:*), Bash(tree:*), Bash(wc:*)
description: Review and update CLAUDE.md files against the actual codebase
---

# Review and Update CLAUDE.md Files

## Step 1: Discover CLAUDE.md Files

Find all `CLAUDE.md` files from the current directory up to the project root, including subdirectory files.
Report found files with their line counts before proceeding.

> **Scope**: This command targets `CLAUDE.md` files only. `CLAUDE.local.md` (session checkpoint) is not subject to review.

---

## Step 2: Review Each File Against the Codebase

For every `CLAUDE.md` file found, verify its content against reality:

**What to compare:**

- Directory structure described vs actual directory tree
- Referenced files/modules — do they still exist?
- Documented patterns/conventions — are they still in use?
- Build/test commands — are they still valid?
- Dependencies listed — are they current?
- Architecture descriptions — do they match the current implementation?

**Identify issues:**

- **Outdated**: References to files, modules, or patterns that no longer exist
- **Incorrect**: Descriptions that contradict the actual implementation
- **Missing**: Important structure, components, or conventions not documented
- **Duplicated**: Same information repeated across multiple CLAUDE.md files

---

## Step 3: Apply Corrections

For each issue found:

- Remove obsolete or incorrect statements
- Update descriptions to match current reality
- Add missing architectural or component-specific details
- Consolidate duplicates — keep information in the most specific applicable file

### Placement Rules

- **Project-wide knowledge** → root `CLAUDE.md`
  (overall architecture, shared standards, build commands)

- **Component-specific details** → subdirectory `CLAUDE.md`
  (e.g., `apps/{component}-ui/CLAUDE.md`, `infrastructure/CLAUDE.md`)

### Size Guidelines

- Root CLAUDE.md: **≤ 180 lines**. If exceeded, distribute to subdirectory files.
- Subdirectory CLAUDE.md: **≤ 150 lines** each.

---

## Step 4: Report

After corrections, report the following:

1. Files reviewed (with before/after line counts)
2. Issues found and actions taken:
   - Items removed (outdated/incorrect)
   - Items updated (corrected to match reality)
   - Items added (previously missing)
   - Items relocated (moved to correct file)
3. Any areas that could not be verified and why

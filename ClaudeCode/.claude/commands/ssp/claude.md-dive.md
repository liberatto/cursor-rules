---
allowed-tools: Read, Write, Glob, Grep, Bash(git:*), Bash(ls:*), Bash(tree:*), Bash(wc:*)
description: Investigate directory architecture and generate CLAUDE.md documentation
argument-hint: "[directory-path] [optional: focus area or instructions]"
---

# Investigate and Document the Directory Architecture

## Input

- **Target**: First path in `$ARGUMENTS`, or current working directory if not specified.
- **Focus**: If `$ARGUMENTS` contains additional text beyond the path, use it as the focus direction for deeper analysis and documentation emphasis.

> Examples:
> - `/ssp:claude.md-dive src/api` → Full analysis of `src/api` directory
> - `/ssp:claude.md-dive src/api focus on API endpoints and middleware` → Deeper focus on API/middleware
> - `/ssp:claude.md-dive . test structure and build pipeline` → Current directory, test/build focus

---

## Step 1: Explore the Target Directory

Deeply explore the target directory and its subdirectories.

**What to examine:**

- Directory tree structure
- Key source files, config files, entry points
- Internal and external dependencies and their roles
- Design patterns, core abstractions, component interactions
- Naming conventions, file organization, overall code layout

**Exclude from exploration:**

- Generated/dependency directories: `node_modules/`, `.git/`, `dist/`, `build/`, `__pycache__/`, `.venv/`, `vendor/`
- Binary files, media files

**When Focus is specified:** Explore all items above, but analyze the user-specified direction more deeply and give it greater weight in the documentation.

---

## Step 2: Generate CLAUDE.md

Create a **new** `CLAUDE.md` file in the target directory.
If a `CLAUDE.md` already exists, **overwrite it** — this command is for initial documentation generation.

### Document Structure

Include only sections that are **relevant**. Omit sections with no applicable content.

```markdown
# {Directory/Module Name}

## Overview
Module purpose and core responsibilities (1-3 sentences)

## Directory Structure
Tree structure of key directories/files with role descriptions

## Architecture & Design Patterns
Key design choices, rationale, and applied patterns

## Key Components
Major files/classes/modules, their roles, and interactions

## Dependencies
Internal/external dependencies and their purposes

## Build & Run
Build, test, and run commands (if applicable)

## Conventions & Style
Coding conventions, naming rules, project-specific practices

## Caveats & Pitfalls
Non-obvious behaviors, gotchas, and developer warnings
```

### Size Guidelines

- Project root CLAUDE.md: **≤ 180 lines**
- Subdirectory CLAUDE.md: **≤ 150 lines**
- If exceeded, keep only essentials and distribute details to subdirectory CLAUDE.md files

---

## Step 3: Report

After generation, report the following:

1. Generated file path and line count
2. List of included sections
3. If Focus was specified, key insights discovered in that area

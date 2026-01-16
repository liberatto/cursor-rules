---
name: skill-creator
description: Guide for creating Claude Code skills. Triggers on "create a skill", "make a new skill", "build a skill for...", "package my skill", "help me design a skill".
---

# Skill Creator

## Core Principles

### Concise is Key

Context window is shared with codebase, conversation, and other skills. Only include what Claude doesn't already know. Prefer concise examples over verbose explanations.

### Match Freedom to Task Fragility

- **High freedom**: Multiple valid approaches, context-dependent decisions
- **Medium freedom**: Preferred patterns with acceptable variation
- **Low freedom**: Fragile operations, critical consistency requirements

## Skill Anatomy

```text
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/       - Executable automation (Python/Bash)
    ├── references/    - Docs loaded into context when needed
    └── assets/        - Templates, configs for output
```

### SKILL.md Structure

**Frontmatter (YAML):**

- `name`: kebab-case identifier (max 64 chars)
- `description`: What it does AND when to use it (max 1024 chars). Include triggers since body loads only after triggering.

**Body (Markdown):** Instructions loaded when skill triggers.

### Resource Types

| Type | Purpose | Example |
|------|---------|---------|
| `scripts/` | Executable automation | `scripts/init_project.py` |
| `references/` | Context docs (loaded on demand) | `references/api-patterns.md` |
| `assets/` | Templates, configs (not loaded) | `assets/template/main.py` |

## Skill Creation Process

### Step 1: Gather Examples

Ask:

- "What specific tasks should this skill handle?"
- "What would a user type to trigger this skill?"
- "What tools/frameworks are involved?"

### Step 2: Plan Reusable Contents

| Pattern | Resource Type |
|---------|---------------|
| Same boilerplate repeatedly | `assets/` template |
| Same commands executed | `scripts/` automation |
| Same decisions made | `references/` guide |
| Same patterns applied | `SKILL.md` workflow |

### Step 3: Initialize

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

### Step 4: Edit SKILL.md

**Frontmatter:**

```yaml
---
name: my-skill-name
description: What it does. When to use it (triggers, file types). Example: "Python API with FastAPI. Use when creating REST APIs or adding endpoints."
---
```

**Body Guidelines:**

- Use imperative form ("Run", "Create", not "Running", "Creates")
- Keep under 500 lines; split into references/ if larger
- Reference bundled resources with clear usage
- Include decision trees for complex workflows

### Step 5: Validate & Package

```bash
# Validate first
python scripts/validate_skill.py <path/to/skill-folder>

# Package if valid
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

### Step 6: Iterate

1. Test on real tasks
2. Note struggles or missing info
3. Update and re-package

## Output Patterns

→ See [references/output-patterns.md](references/output-patterns.md) for:

- Template patterns (strict vs flexible)
- Code generation style rules
- Project structure scaffolding
- Diff/modification format

## Progressive Disclosure

Keep SKILL.md lean by using references:

```markdown
## Quick Start
- New project: `python scripts/init.py`
- Add feature: Follow "Development" below

## Advanced
→ See [references/workflows.md](references/workflows.md)
```

## Example Structure

```text
python-fastapi/
├── SKILL.md
├── scripts/
│   ├── init_api.py
│   └── add_endpoint.py
├── references/
│   ├── api-patterns.md
│   └── testing-guide.md
└── assets/
    └── template/
        ├── main.py
        └── requirements.txt
```

## What NOT to Include

- README.md, CHANGELOG.md (SKILL.md is the docs)
- User-facing documentation
- Setup/testing procedures

Only include what Claude needs to execute tasks.

## Claude Code Best Practices

→ See [references/claude-code-specifics.md](references/claude-code-specifics.md) for:

- Project detection patterns
- Style preservation
- Safety guidelines
- Git integration

## Workflow Patterns

→ See [references/workflows.md](references/workflows.md) for:

- Sequential workflows
- Conditional workflows
- Error recovery patterns

## Validation Checklist

Before packaging:

- [ ] `name`: kebab-case, ≤64 chars
- [ ] `description`: includes what AND when, ≤1024 chars, no angle brackets
- [ ] Body: <500 lines
- [ ] All referenced files exist
- [ ] Scripts tested and executable
- [ ] No unnecessary documentation files

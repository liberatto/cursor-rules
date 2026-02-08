---
name: codex
description: Use when the user asks to run Codex CLI (codex exec, codex resume, codex review, codex fork) or references OpenAI Codex for code analysis, refactoring, planning, validation, testing, or automated editing
---

# Codex Skill Guide

> **CLI Version**: 0.98.0+ | **Config**: `~/.codex/config.toml`

## Execution Workflow

### Step 1: Gather Parameters

Use `AskUserQuestion` with **two questions in a single prompt**:

1. **Model**: `gpt-5.3-codex` (recommended), `gpt-5.2-codex`, or `gpt-5.2`
2. **Reasoning effort**: `xhigh`, `high`, `medium`, or `low`

### Step 2: Determine Sandbox Mode

| Task type | Sandbox | Flag |
| --- | --- | --- |
| Read-only analysis | `read-only` (default) | `-s read-only` |
| Local file edits | `workspace-write` | `--full-auto` |
| Network or broad access | `danger-full-access` | `-s danger-full-access --full-auto` |

### Step 3: Build and Run Command

```bash
codex exec --skip-git-repo-check \
  -m <MODEL> \
  -c model_reasoning_effort="<EFFORT>" \
  <SANDBOX_FLAGS> \
  "prompt here" 2>/dev/null
```

**Rules:**

- Always use `--skip-git-repo-check` with `exec`.
- Always append `2>/dev/null` to suppress thinking tokens (stderr). Only show stderr when user requests thinking tokens or debugging.
- Use `-C <DIR>` to set working directory.

**Optional flags:**

| Flag | Purpose |
| --- | --- |
| `-i <FILE>...` | Attach image(s) to the prompt |
| `--search` | Enable web search tool |
| `--add-dir <DIR>` | Allow writes to additional directories |
| `--output-schema <FILE>` | Constrain response to JSON Schema |
| `--json` | Output events as JSONL stream |
| `-p <PROFILE>` | Select a config.toml profile |

### Step 4: Report and Follow Up

After completion, inform the user: *"You can resume this Codex session at any time by saying 'codex resume' or asking me to continue."*

Then use `AskUserQuestion` to confirm next steps.

## Resume and Fork

### Resume (continue previous session)

```bash
echo "follow-up prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null
```

- Inherits model, reasoning effort, and sandbox from original session.
- Only add config flags if the user explicitly requests changes.

### Fork (branch from previous session)

```bash
codex fork --last "explore a different approach"
```

- Creates a new session branching from the previous one.

## Code Review

Non-interactive code review via `codex review`:

```bash
# Uncommitted changes (staged + unstaged + untracked)
codex review --uncommitted 2>/dev/null

# Changes against a base branch
codex review --base main 2>/dev/null

# Specific commit
codex review --commit <SHA> 2>/dev/null

# Custom review instructions
codex review --uncommitted "focus on security vulnerabilities" 2>/dev/null
```

## Apply Diff

Apply the latest diff produced by a Codex agent to the local working tree:

```bash
codex apply <TASK_ID>
```

## Codex Cloud (Experimental)

Run tasks remotely and apply results locally:

```bash
codex cloud exec "refactor the auth module"   # Submit task
codex cloud list                                # List tasks
codex cloud status <TASK_ID>                    # Check status
codex cloud diff <TASK_ID>                      # View diff
codex cloud apply <TASK_ID>                     # Apply locally
```

## Approval Policy Reference

The `-a, --ask-for-approval` flag controls when user approval is required:

| Policy | Behavior |
| --- | --- |
| `untrusted` | Auto-run trusted commands (ls, cat, etc.); prompt for others |
| `on-failure` | Auto-run all; prompt only on execution failure |
| `on-request` | Model decides when to ask (default with `--full-auto`) |
| `never` | Never prompt; failures go straight back to the model |

## Config Override Syntax

```bash
# Override config values with -c (parsed as TOML)
codex exec -c model="o3" -c model_reasoning_effort="high" ...

# Dotted path for nested values
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' ...
```

## Error Handling

- Stop and report failures when `codex` exits non-zero; request user direction before retrying.
- Before using high-impact flags (`--full-auto`, `-s danger-full-access`, `--skip-git-repo-check`), ask user permission via `AskUserQuestion` unless already granted.
- Summarize warnings or partial results and ask how to proceed.

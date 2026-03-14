---
name: codex
description: "Use when the user asks to run Codex CLI (codex exec, codex review, codex resume, codex fork) or references OpenAI Codex. Triggers: 코드 리뷰, codex 실행, codex로 분석, 리뷰해줘, 코드 검토, codex review, codex exec, run codex, code review with codex"
---

# Codex CLI Skill Guide

> **CLI**: 0.111.0+ | **Tier**: Plus | **Config**: `~/.codex/config.toml`

## Defaults

Before asking the user for model or reasoning effort, check if `~/.codex/config.toml` already defines them.

```toml
# ~/.codex/config.toml
model = "gpt-5.4"
model_reasoning_effort = "high"
```

**Rule**: If config.toml has `model` and `model_reasoning_effort`, skip `AskUserQuestion` and use those defaults. Only ask when the user explicitly wants to override.

### Available Models (Plus)

| Model | Notes |
|-------|-------|
| `gpt-5.4` | Latest, best performance |
| `gpt-5.3-codex` | Stable, proven |
| `gpt-5.2-codex` | Good for API key workflows |
| `gpt-5.1-codex-mini` | Lightweight, low cost |

## Command Router

Match user intent to the right subcommand. **Default to `review` unless the user explicitly wants code generation or modification.**

| User Intent | Subcommand | Key Signals |
|-------------|------------|-------------|
| Review code / plan / find improvements | `review` | "리뷰", "review", "개선점", "검토", "코드 품질", "확인해줘" |
| Run a task (generate, refactor, fix) | `exec` | "수정해", "고쳐", "만들어", "리팩토링", "분석해줘" |
| Continue previous session | `resume` | "이어서", "continue", "resume" |
| Branch from previous session | `fork` | "다른 방향", "fork", "분기" |
| Apply a generated diff | `apply` | "적용", "apply", "diff 반영" |

---

## Review Workflow (Primary)

Non-interactive code review. No sandbox needed. **가장 자주 사용하는 워크플로우.**

### Step 1: Determine Review Scope

| Scope | Flag | When to Use |
|-------|------|-------------|
| Uncommitted changes | `--uncommitted` | Default — staged + unstaged + untracked |
| Branch comparison | `--base <BRANCH>` | Reviewing a feature branch against main |
| Specific commit | `--commit <SHA>` | Reviewing a single commit |

If the user doesn't specify scope, use `--uncommitted`.

### Step 2: Build and Run

```bash
codex review <SCOPE_FLAG> \
  [--title "<CONTEXT>"] \
  ["<CUSTOM_INSTRUCTIONS>"] \
  2>/dev/null
```

Examples:

```bash
# Review all uncommitted changes
codex review --uncommitted 2>/dev/null

# Review against main branch
codex review --base main 2>/dev/null

# Review specific commit
codex review --commit abc1234 2>/dev/null

# With context and custom focus
codex review --uncommitted --title "Auth module" "Focus on security vulnerabilities" 2>/dev/null

# Claude Code가 작성한 코드를 리뷰
codex review --uncommitted "Claude Code가 생성한 코드의 품질, 엣지케이스, 개선점을 검토해줘" 2>/dev/null
```

### Step 3: Report Results

Summarize the review output. If the user wants to act on findings, switch to direct code editing (Claude Code) or `exec` for Codex-driven fixes.

---

## Exec Workflow

Non-interactive task execution. 코드 수정이 필요할 때 사용.

### Step 1: Gather Parameters (only if no config.toml defaults)

Use `AskUserQuestion` to collect **in a single prompt**:

1. **Model** — `gpt-5.4` (recommended), `gpt-5.3-codex`, `gpt-5.1-codex-mini`
2. **Reasoning effort** — `xhigh`, `high`, `medium`, `low`

### Step 2: Determine Sandbox

| Task Type | Sandbox | Flags |
|-----------|---------|-------|
| Read-only analysis | `read-only` (default) | `-s read-only` |
| Local file edits | `workspace-write` | `--full-auto` |
| Network / broad access | `danger-full-access` | `-s danger-full-access --full-auto` |

### Step 3: Build and Run

```bash
codex exec --skip-git-repo-check \
  -m <MODEL> \
  -c model_reasoning_effort="<EFFORT>" \
  <SANDBOX_FLAGS> \
  "prompt here" 2>/dev/null
```

**Rules:**

- Always use `--skip-git-repo-check` with `exec`.
- Always append `2>/dev/null` to suppress stderr (thinking tokens). Show stderr only when user requests debugging.
- Use `-C <DIR>` to set working directory.
- Pipe prompt via stdin: `echo "prompt" | codex exec ...` or use `-` as prompt arg.

**Optional flags:**

| Flag | Purpose |
|------|---------|
| `-i <FILE>...` | Attach images (PNG, JPG, GIF, WebP) |
| `--add-dir <DIR>` | Additional writable directory |
| `--output-schema <FILE>` | Constrain response shape with JSON Schema |
| `--json` | JSONL stream output |
| `-o <FILE>` | Save last message to file |
| `-p <PROFILE>` | Select config.toml profile |
| `--ephemeral` | Don't persist session files |
| `--enable <FEATURE>` | Enable a feature flag for this run |
| `--disable <FEATURE>` | Disable a feature flag for this run |

### Step 4: Report and Follow Up

After completion, inform the user: *"You can continue this session with `codex resume --last`."*

---

## Resume & Fork

### Resume (continue previous session)

```bash
# Non-interactive: continue last session
echo "follow-up prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null

# Interactive: session picker
codex resume

# Interactive: continue last session directly
codex resume --last

# Interactive: specific session
codex resume <SESSION_ID>

# Show all sessions (ignore cwd filter)
codex resume --all
```

- Inherits model, reasoning effort, and sandbox from the original session.
- Only add override flags when the user explicitly requests them.

### Fork (branch from previous session)

```bash
codex fork --last "try a different approach"
codex fork <SESSION_ID> "new direction"
codex fork --all  # show all sessions picker
```

- Creates a new session branching from a previous one.

---

## Apply

Apply a Codex-generated diff to the local working tree:

```bash
codex apply <TASK_ID>
```

---

## MCP Server Management

외부 MCP 서버를 Codex에 연결하여 도구 확장.

```bash
codex mcp list              # 등록된 MCP 서버 목록
codex mcp get <NAME>        # 특정 서버 정보 조회
codex mcp add <NAME> ...    # MCP 서버 추가
codex mcp remove <NAME>     # MCP 서버 제거
codex mcp login <NAME>      # MCP 서버 인증
codex mcp logout <NAME>     # MCP 서버 인증 해제
```

Codex를 MCP 서버로 노출: `codex mcp-server` (stdio 모드)

---

## Feature Flags

```bash
codex features list             # 전체 플래그 목록 (상태 포함)
codex features enable <NAME>    # config.toml에 활성화 저장
codex features disable <NAME>   # config.toml에 비활성화 저장
```

주요 stable 플래그: `fast_mode`, `personality`, `shell_tool`, `shell_snapshot`, `sqlite`, `unified_exec`, `skill_mcp_dependency_install`

---

## Config Override

```bash
# Override config values with -c (TOML parsing)
codex exec -c model="gpt-5.4" -c model_reasoning_effort="high" ...

# Nested values use dot paths
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' ...
codex exec -c shell_environment_policy.inherit=all ...
```

Key config keys:

```toml
model = "gpt-5.4"
model_reasoning_effort = "high"     # xhigh | high | medium | low
personality = "pragmatic"            # none | friendly | pragmatic
model_instructions_file = "path"     # custom instruction file
sandbox_mode = "read-only"           # read-only | workspace-write | danger-full-access
```

## Error Handling

- On abnormal `codex` exit: stop and report. Confirm with user before retrying.
- Before using high-risk flags (`--full-auto`, `-s danger-full-access`, `--skip-git-repo-check`), get user permission via `AskUserQuestion` (skip if already granted).
- On warnings or partial results: summarize and ask how to proceed.

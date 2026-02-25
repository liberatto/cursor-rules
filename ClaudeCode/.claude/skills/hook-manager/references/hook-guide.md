# Hook Guide

Hook을 만들기 전에 알아야 할 개념, 이벤트, 핸들러, 옵션, 구조를 정리한 레퍼런스.
사용자가 hook에 대해 질문하면 이 문서를 참조하여 답변한다.

---

## 1. Hooks란

Claude Code lifecycle의 특정 시점에서 자동 실행되는 사용자 정의 핸들러.
LLM 재량이 아닌 **결정론적(deterministic) 실행**을 보장한다.

| 구분 | CLAUDE.md | Hooks |
|------|-----------|-------|
| 성격 | 지시 (LLM 재량) | 강제 (결정적 실행) |
| 실행 보장 | LLM이 무시할 수 있음 | 반드시 실행됨 |
| 적합 대상 | 코딩 스타일, 아키텍처 가이드 | 포맷팅 강제, 명령 차단, 알림 |

Hook 생성 방법: (1) `/hooks` 내장 메뉴, (2) Claude Code에 자연어 요청, (3) settings JSON 수동 편집

---

## 1.1 이벤트 흐름 다이어그램

### Session Lifecycle

```
 ① SessionStart [command만]
 │  matcher: startup | resume | clear | compact
 │
 │  ┌─────────────────── TURN (반복) ──────────────────┐
 │  │                                                   │
 │  │  ② UserPromptSubmit [all]                         │
 │  │  │  사용자 프롬프트 제출                            │
 │  │  │                                                │
 │  │  │  ┌──────── AGENTIC LOOP (반복) ───────┐        │
 │  │  │  │                                     │        │
 │  │  │  │  ③ PreToolUse [all]                 │        │
 │  │  │  │  │  matcher: Bash, Edit|Write, ...  │        │
 │  │  │  │  │                                  │        │
 │  │  │  │  │  ┌─ ④ PermissionRequest [all]    │        │
 │  │  │  │  │  │  (권한 필요 시에만)             │        │
 │  │  │  │  │  └──────────────────────┐        │        │
 │  │  │  │  │                         │        │        │
 │  │  │  │  ▼                         │        │        │
 │  │  │  │  도구 실행                  │        │        │
 │  │  │  │  │                         │        │        │
 │  │  │  │  ├─ 성공 → ⑤ PostToolUse [all]      │        │
 │  │  │  │  └─ 실패 → ⑥ PostToolUseFailure [all]       │
 │  │  │  │                                     │        │
 │  │  │  │  ── 서브에이전트 사용 시 ──          │        │
 │  │  │  │  │                                  │        │
 │  │  │  │  ⑦ SubagentStart [command만]        │        │
 │  │  │  │  │  서브에이전트 작업 중...           │        │
 │  │  │  │  ⑧ SubagentStop [all]               │        │
 │  │  │  │                                     │        │
 │  │  │  └──────── (다음 도구 호출) ──────────┘        │
 │  │  │                                                │
 │  │  ⑨ Stop [all]                                     │
 │  │     │                                             │
 │  │     ├─ 허용 → 사용자 입력 대기 (다음 턴)           │
 │  │     └─ 차단 → Claude 계속 작업 (agentic loop 복귀) │
 │  │                                                   │
 │  └───────────────── (다음 턴) ──────────────────────┘
 │
 ⑩ SessionEnd [command만]
    matcher: clear | logout | prompt_input_exit | ...
```

### Standalone Events

```
 ⑪ Notification [command만]        ─ 알림 발송 시
    matcher: permission_prompt | idle_prompt | ...

 ⑫ PreCompact [command만]          ─ 컨텍스트 압축 전
    matcher: manual | auto

 ⑬ ConfigChange [command만]        ─ 설정 파일 변경 시
    matcher: user_settings | project_settings | ...

 ⑭ WorktreeCreate [command만]      ─ worktree 생성 시
 ⑮ WorktreeRemove [command만]      ─ worktree 제거 시
```

### Agent Team Events

```
 ⑯ TeammateIdle [command만]        ─ 팀원이 idle 전환 시
 ⑰ TaskCompleted [command만]       ─ 태스크 완료 표시 시
```

### 이벤트 쌍

| 시작 | 종료 | 단위 |
|------|------|------|
| `SessionStart` | `SessionEnd` | 세션 |
| `UserPromptSubmit` | `Stop` | 턴 |
| `PreToolUse` | `PostToolUse` / `PostToolUseFailure` | 도구 호출 |
| `SubagentStart` | `SubagentStop` | 서브에이전트 |
| `WorktreeCreate` | `WorktreeRemove` | worktree |

### 차단 가능 여부

**차단 가능** (exit 2 또는 `decision: "block"`):
`UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `Stop`, `SubagentStop`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`, `WorktreeCreate`

**차단 불가** (부수 효과만):
`SessionStart`, `SessionEnd`, `PostToolUse`, `PostToolUseFailure`, `Notification`, `SubagentStart`, `PreCompact`, `WorktreeRemove`

---

## 2. Hook Events (17종)

| Event | Timing | Block | Matcher Target | Handlers |
|-------|--------|:-----:|---------------|----------|
| `SessionStart` | 세션 시작/재개 | - | `startup`, `resume`, `clear`, `compact` | command |
| `SessionEnd` | 세션 종료 | - | `clear`, `logout`, `prompt_input_exit` 등 | command |
| `UserPromptSubmit` | 프롬프트 제출 (Claude 처리 전) | O | — (항상 발동) | all |
| `PreToolUse` | 도구 실행 전 | O | tool name (`Bash`, `Edit\|Write`, `mcp__.*`) | all |
| `PostToolUse` | 도구 실행 성공 후 | - | tool name | all |
| `PostToolUseFailure` | 도구 실행 실패 후 | - | tool name | all |
| `PermissionRequest` | 권한 대화상자 표시 시 | O | tool name | all |
| `Stop` | Claude 응답 완료 | O | — (항상 발동) | all |
| `Notification` | 알림 전송 | - | `permission_prompt`, `idle_prompt` 등 | command |
| `SubagentStart` | 서브에이전트 생성 | - | agent type | command |
| `SubagentStop` | 서브에이전트 완료 | O | agent type | all |
| `TeammateIdle` | 팀원 idle 전환 | O | — | command |
| `TaskCompleted` | 작업 완료 표시 | O | — | command |
| `ConfigChange` | 설정 파일 변경 | O | `user_settings`, `project_settings` 등 | command |
| `WorktreeCreate` | worktree 생성 | O | — | command |
| `WorktreeRemove` | worktree 제거 | - | — | command |
| `PreCompact` | 컨텍스트 압축 전 | - | `manual`, `auto` | command |

- **Block(O)**: exit code 2 또는 `decision: "block"` 출력 시 해당 동작 차단
- **Handlers "all"**: command, prompt, agent 3종 모두 가능. "command"만 표기된 이벤트는 command만 지원

---

## 3. Handler Types

### 비교표

| | command | prompt | agent |
|--|---------|--------|-------|
| 실행 방식 | 셸 커맨드 | Haiku 1회 평가 | 서브에이전트 다회전 |
| 입력 방식 | stdin JSON | `$ARGUMENTS` 치환 | `$ARGUMENTS` 치환 |
| 도구 접근 | 없음 (외부 CLI만) | 없음 | Read, Grep, Glob 등 |
| 기본 timeout | 600초 | 30초 | 60초 |
| 비동기 | O (`async: true`) | X | X |
| 지원 이벤트 | 17종 전부 | 8종 (차단 가능 이벤트) | 8종 (차단 가능 이벤트) |
| 비용 | 0 | Haiku 1회 토큰 | Haiku × N턴 토큰 |

### 선택 가이드

```
셸 스크립트로 충분한가? ── YES ──→ command (결정적, 무료)
         │
         NO
         │
코드/파일 탐색이 필요한가? ── NO ──→ prompt (Haiku 1회 판단)
         │
         YES ──→ agent (서브에이전트 다회전, 도구 사용)
```

### command — stdin JSON

이벤트 컨텍스트가 stdin으로 JSON 전달:

```json
{ "session_id": "abc-123", "tool_name": "Bash", "tool_input": { "command": "ls -la" } }
```

```bash
# 필드 1개
COMMAND=$(jq -r '.tool_input.command')

# 여러 필드 (jq는 stdin 1회만 읽음 — 변수에 먼저 저장)
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')
```

### prompt / agent — $ARGUMENTS 치환

프롬프트의 `$ARGUMENTS`가 이벤트 컨텍스트 텍스트로 치환:

```json
{ "type": "prompt", "prompt": "이 명령이 안전한지 판단하세요: $ARGUMENTS" }
```

---

## 4. Matcher Patterns

정규식(regex) 기반. 이벤트에 따라 매칭 대상이 다르다.

| Pattern | Meaning | Example |
|---------|---------|---------|
| `Bash` | Exact | Bash tool only |
| `Edit\|Write` | OR | Edit or Write |
| `mcp__.*` | Wildcard | All MCP tools |
| `mcp__github__.*` | Server filter | GitHub MCP server tools |
| `""` or omitted | Match all | Fires on everything |

**Matcher target by event:**

| Event | Matches against |
|-------|----------------|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` | tool name |
| `SessionStart` | start method (`startup`, `resume`, `clear`, `compact`) |
| `SessionEnd` | exit reason (`clear`, `logout`, `prompt_input_exit` etc.) |
| `Notification` | notification type (`permission_prompt`, `idle_prompt` etc.) |
| `SubagentStart`, `SubagentStop` | agent type |
| `PreCompact` | trigger type (`manual`, `auto`) |
| `ConfigChange` | config source (`user_settings`, `project_settings`, `skills`) |
| Others (`UserPromptSubmit`, `Stop` etc.) | No matcher — always fires |

---

## 5. Settings Files

| File | Scope | Shared | Use case |
|------|-------|:------:|----------|
| `~/.claude/settings.json` | All projects (user) | X | Desktop notifications, personal security |
| `.claude/settings.json` | Single project (shared) | O (Git) | Team formatting, project security |
| `.claude/settings.local.json` | Single project (private) | X | Personal/experimental hooks |

---

## 6. Hook JSON Structure

3-level nesting:

```json
{
  "hooks": {
    "<Event>": [                      // Level 1: Event
      {
        "matcher": "<regex>",         // Level 2: Filter (regex)
        "hooks": [                    // Level 3: Handler array
          {
            "type": "command",
            "command": "<shell command>"
          }
        ]
      }
    ]
  }
}
```

### Handler fields

**Required:**

| Field | Values | Description |
|-------|--------|-------------|
| `type` | `command`, `prompt`, `agent` | Handler type |
| `command` | shell string | Shell command (command type) |
| `prompt` | text string | LLM prompt (prompt/agent type) |

**Optional** (set only when needed):

| Field | Default | Applies to | Description |
|-------|---------|------------|-------------|
| `timeout` | 600 / 30 / 60 | all | Seconds before timeout |
| `async` | `false` | command only | Run in background |
| `statusMessage` | — | all | Spinner text during execution |
| `once` | `false` | skill hooks only | Run once per session |

---

## 7. Exit Codes & Output

### Exit codes

| Code | Meaning | Behavior |
|------|---------|----------|
| **0** | Success | Parse stdout JSON |
| **2** | Block | stderr → Claude error. JSON ignored |
| **Other** | Non-blocking error | stderr in verbose mode only |

### JSON output fields (exit 0)

| Field | Default | Description |
|-------|---------|-------------|
| `continue` | `true` | `false` stops Claude completely |
| `stopReason` | — | Shown to user when `continue: false` |
| `suppressOutput` | `false` | Hide verbose output |
| `systemMessage` | — | Warning message to user |

### Decision control by event

| Event group | Key fields |
|-------------|------------|
| `UserPromptSubmit`, `PostToolUse`, `Stop` etc. | `decision: "block"`, `reason` |
| `PreToolUse` | `hookSpecificOutput.permissionDecision` (allow/deny/ask), `updatedInput`, `additionalContext` |
| `PermissionRequest` | `hookSpecificOutput.decision.behavior` (allow/deny) |
| `TeammateIdle`, `TaskCompleted` | exit code 2 + stderr only |

**PreToolUse `updatedInput`** — 도구 호출 전 파라미터 수정:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": { "command": "npm run lint -- --fix" }
  }
}
```

---

## 8. Debugging

| Method | Description |
|--------|-------------|
| `claude --debug` | Hook matching/execution logs |
| `Ctrl+O` | Toggle verbose mode |
| `/hooks` | View registered hooks with source labels |

**Common issues:**

| Issue | Solution |
|-------|----------|
| Hook not firing | Check `/hooks`, verify matcher regex, confirm event type |
| Stop hook infinite loop | Check `stop_hook_active` in stdin — if `true`, `exit 0` |
| JSON parse failure | Shell profile `echo` polluting stdout — wrap with `[[ $- == *i* ]]` |
| Script not executing | Check `chmod +x` and shebang `#!/bin/bash` |
| Manual edit not applied | `/hooks` menu review or restart session |
| Path issues | Use `$CLAUDE_PROJECT_DIR` for reliable paths |

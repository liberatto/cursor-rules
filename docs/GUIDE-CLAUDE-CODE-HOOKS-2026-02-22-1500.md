# Claude Code Hooks 가이드

> 작성일: 2026-02-22
> 대상: Claude Code 사용자 (초급~중급)
> 대상 버전: Claude Code 2026-02 기준 (v2.1.0+)

---

## 1. 개요 — Hooks란 무엇인가

Hooks는 Claude Code lifecycle의 특정 시점에서 **자동으로 실행되는 사용자 정의 명령**이다. 셸 커맨드, LLM 프롬프트, 서브에이전트 중 하나의 형태로 동작하며, LLM의 판단에 의존하지 않는 **결정론적(deterministic) 제어**를 제공한다.

**CLAUDE.md vs Hooks:**

| 구분 | CLAUDE.md | Hooks |
|------|-----------|-------|
| 성격 | 지시 (LLM 재량) | 강제 (결정적 실행) |
| 실행 보장 | LLM이 무시할 수 있음 | 반드시 실행됨 |
| 적합 대상 | 코딩 스타일, 아키텍처 가이드 | 포맷팅 강제, 명령 차단, 알림 |

**Hook 생성 방법 3가지:**

1. **`/hooks` 메뉴** — CLI 내장 인터랙티브 메뉴 (가장 쉬움)
2. **Claude Code에게 자연어 요청** — 복잡한 로직도 대화로 생성
3. **수동 JSON 편집** — settings.json 직접 편집 (세밀한 제어)

---

## 2. 핵심 개념 Quick Reference

### 2.1 Hook 이벤트 전체 요약표 (17종)

| 이벤트 | 시점 | 차단 | Matcher 대상 | Handler |
|--------|------|:----:|-------------|---------|
| `SessionStart` | 세션 시작/재개 | - | `startup`, `resume`, `clear`, `compact` | command |
| `SessionEnd` | 세션 종료 | - | `clear`, `logout`, `prompt_input_exit` 등 | command |
| `UserPromptSubmit` | 프롬프트 제출 (Claude 처리 전) | O | 미지원 (항상 발동) | 모두 |
| `PreToolUse` | 도구 실행 전 | O | tool명 (`Bash`, `Edit\|Write`, `mcp__.*`) | 모두 |
| `PostToolUse` | 도구 실행 성공 후 | - | tool명 | 모두 |
| `PostToolUseFailure` | 도구 실행 실패 후 | - | tool명 | 모두 |
| `PermissionRequest` | 권한 대화상자 표시 시 | O | tool명 | 모두 |
| `Stop` | Claude 응답 완료 | O | 미지원 (항상 발동) | 모두 |
| `Notification` | 알림 전송 | - | `permission_prompt`, `idle_prompt` 등 | command |
| `SubagentStart` | 서브에이전트 생성 | - | agent type | command |
| `SubagentStop` | 서브에이전트 완료 | O | agent type | 모두 |
| `TeammateIdle` | 팀원 idle 전환 | O | 미지원 | command |
| `TaskCompleted` | 작업 완료 표시 | O | 미지원 | command |
| `ConfigChange` | 설정 파일 변경 | O | `user_settings`, `project_settings` 등 | command |
| `WorktreeCreate` | worktree 생성 | O | 미지원 | command |
| `WorktreeRemove` | worktree 제거 | - | 미지원 | command |
| `PreCompact` | 컨텍스트 압축 전 | - | `manual`, `auto` | command |

> **차단(O)**: hook이 exit code 2를 반환하거나 `decision: "block"`을 출력하면 해당 동작을 막을 수 있다.
> **Handler "모두"**: command, prompt, agent 3종 모두 사용 가능. "command"만 표기된 이벤트는 command type만 지원.

### 2.2 Handler Type 비교표

| 항목 | command | prompt | agent |
|------|---------|--------|-------|
| 실행 방식 | 셸 커맨드 | Haiku 1회 평가 | 서브에이전트 다회전 |
| 입력 | stdin JSON | `$ARGUMENTS` 치환 | `$ARGUMENTS` 치환 |
| 도구 접근 | 없음 (외부 CLI만) | 없음 | Read, Grep, Glob 등 |
| 기본 timeout | 600초 | 30초 | 60초 |
| 비동기 지원 | O (`async: true`) | X | X |
| 적합 상황 | 스크립트, 결정적 규칙 | 간단한 판단/검증 | 코드 검사, 복잡한 검증 |
| 지원 이벤트 | 17종 전부 | 8종 (차단 가능 이벤트) | 8종 (차단 가능 이벤트) |

### 2.3 Handler Type 상세 동작 방식

#### (1) `command` — 셸 커맨드 실행

가장 기본적이고 범용적인 타입. 셸 스크립트나 CLI 도구를 직접 실행한다.

**동작 흐름:**

```
이벤트 발생
  → Claude Code가 이벤트 컨텍스트를 JSON으로 직렬화
    → hook 셸 프로세스 spawn
      → stdin 파이프로 JSON 전달
        → 스크립트가 JSON 파싱 → 로직 실행
          → exit code + stdout/stderr 반환
```

**stdin 입력**: Claude Code가 hook 프로세스를 실행하면서 **표준 입력(stdin) 파이프로 이벤트 컨텍스트 JSON을 전달**한다. 터미널의 `echo '{}' | jq`와 동일한 원리다.

stdin에 들어오는 JSON 예시 (`PreToolUse` + Bash):

```json
{
  "session_id": "abc-123",
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la"
  }
}
```

스크립트에서 stdin 읽는 법:

```bash
#!/bin/bash
# 방법 1: jq로 직접 파싱 (필드 1개만 필요할 때)
COMMAND=$(jq -r '.tool_input.command')

# 방법 2: 변수에 저장 후 파싱 (여러 필드 필요할 때)
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
```

> **주의**: `jq`는 stdin을 한 번만 읽을 수 있다. 여러 필드가 필요하면 `cat`으로 먼저 변수에 담아야 한다.

**특징:**

- **결정론적(deterministic)** — LLM 판단 없이 지정한 로직대로 정확히 동작
- 17종 이벤트 **전부** 지원 (유일하게 모든 이벤트에서 사용 가능)
- `async: true`로 비동기 실행 가능

**적합한 상황:** 포맷터/린터 자동 실행, 위험 명령어 패턴 차단, 로그 기록, 데스크톱 알림, 환경변수 로딩

---

#### (2) `prompt` — Haiku LLM 1회 판단

**Haiku 모델을 1회 호출**해서 판단을 위임하는 방식. 셸 스크립트의 패턴 매칭으로는 어려운 **"의미 기반" 검증**이 필요할 때 사용한다.

**동작 흐름:**

```
이벤트 발생
  → 이벤트 컨텍스트를 텍스트로 직렬화
    → 프롬프트의 $ARGUMENTS를 컨텍스트 텍스트로 치환
      → Haiku 모델에 1회 API 호출
        → Haiku가 JSON 응답 반환 (decision, reason 등)
```

**`$ARGUMENTS` 치환**: `command` 타입이 raw JSON을 stdin으로 받는 것과 달리, `prompt`는 프롬프트 문자열 안의 `$ARGUMENTS`를 **읽기 쉬운 텍스트로 치환**한다. LLM이 자연어로 바로 이해할 수 있다.

```json
{
  "type": "prompt",
  "prompt": "이 명령이 프로덕션에 안전한지 판단하세요: $ARGUMENTS"
}
```

실제 Haiku에 전달되는 프롬프트:

```
이 명령이 프로덕션에 안전한지 판단하세요:
Tool: Bash
Input: {"command": "docker rm -f $(docker ps -aq)"}
Session: abc-123
```

**`command`로는 어렵지만 `prompt`가 해결하는 경우:**

```bash
# command 타입 — "rm -rf" 패턴 매칭은 가능하지만...
echo "$COMMAND" | grep -qE 'rm\s+-rf'

# 이런 의미 판단은 불가능:
# "find / -delete"         ← 위험하지만 패턴이 다름
# "rm -rf ./build"         ← 빌드 디렉토리라 안전할 수도
# "docker system prune -a" ← 문맥에 따라 위험도가 다름
```

`prompt` 타입은 Haiku가 명령의 **의미를 이해**하고 `find / -delete` 같은 변형도 차단할 수 있다.

**Haiku 응답 형식:**

```json
// 허용
{"decision": "allow"}

// 차단
{"decision": "block", "reason": "루트 디렉토리 전체 삭제 명령입니다"}
```

**특징:**

- 도구 접근 없음 — 텍스트 기반 판단만 수행
- 빠르고 가벼움 (timeout 30초)
- 차단 가능 이벤트 8종에서만 사용 가능

**적합한 상황:** 서브에이전트 결과 품질 평가, 프롬프트 적절성 판단, 패턴 매칭으론 부족하지만 코드 탐색까지는 불필요한 중간 수준의 판단

---

#### (3) `agent` — 서브에이전트 다회전 실행

가장 강력하지만 비용이 큰 타입. **독립 서브에이전트가 여러 턴에 걸쳐 도구를 사용하며 작업을 수행**한다. `prompt`가 "1회 판단"이라면, `agent`는 "스스로 탐색하고 실행하는 미니 Claude"다.

**동작 흐름:**

```
이벤트 발생
  → 이벤트 컨텍스트를 텍스트로 직렬화
    → 프롬프트의 $ARGUMENTS를 컨텍스트로 치환 (prompt 타입과 동일)
      → Hook 전용 서브에이전트 spawn (Haiku 모델)
        → 에이전트가 도구를 사용하며 다회전 실행
          ├─ Turn 1: 프롬프트 분석, 탐색 전략 수립
          ├─ Turn 2: Glob으로 관련 파일 탐색
          ├─ Turn 3: Read로 파일 내용 확인
          ├─ Turn 4: Bash로 테스트 실행
          └─ Turn 5: 결과 판단 → JSON 응답 반환
```

**서브에이전트 사양:**

| 항목 | 내용 |
|------|------|
| 모델 | Haiku (경량, 빠름) |
| 사용 가능 도구 | Read, Grep, Glob, Bash 등 (읽기 + 실행) |
| 사용 불가 도구 | Edit, Write, Task 등 (파일 수정, 하위 에이전트 spawn 불가) |
| 컨텍스트 | 프롬프트 + `$ARGUMENTS`만 (메인 대화 기록 접근 불가) |
| 수명 | hook 실행 → 응답 반환 → 즉시 종료 |

> `.claude/agents/`에 정의한 커스텀 에이전트와는 무관한, **hook 전용 경량 에이전트**다. 메인 Claude(Opus/Sonnet)의 대화와 완전히 격리되어 있고, 읽기 + 실행만 가능하며, 응답 후 즉시 소멸한다.

**구체적 동작 예시 — Stop hook 테스트 게이트:**

```json
{
  "type": "agent",
  "prompt": "테스트를 실행하고 통과 여부를 확인하세요. $ARGUMENTS",
  "timeout": 120
}
```

서브에이전트의 실제 턴별 동작:

```
Turn 1: $ARGUMENTS 분석 → "src/auth.ts가 수정된 것 같다"
Turn 2: Glob("**/auth*.test.*") → src/auth.test.ts 발견
Turn 3: Read("src/auth.test.ts") → 테스트 코드 확인
Turn 4: Bash("npm test -- src/auth.test.ts") → 2 passed, 1 failed
Turn 5: 결과 반환 → {"ok": false, "reason": "auth.test.ts: 'should reject expired token' 실패"}
```

**적합한 상황:** 작업 완료 전 테스트 실행 + 결과 검증, 코드 변경 후 영향도 분석, 단순 스크립트로는 불가능한 코드 이해가 필요한 검증

---

#### Handler Type 선택 가이드

```
셸 스크립트로 충분한가? ── YES ──→ command (결정적, 무료)
         │
         NO
         │
코드/파일 탐색이 필요한가? ── NO ──→ prompt (Haiku 1회 판단)
         │
         YES ──→ agent (서브에이전트 다회전, 도구 사용)
```

> **비용 순서**: `command` (0) < `prompt` (Haiku 1회 토큰) < `agent` (Haiku × N턴 토큰). 가능하면 `command`로 해결하고, LLM 판단이 필요할 때만 `prompt`/`agent`를 사용하는 것이 권장된다.

### 2.5 설정 파일 위치와 스코프

| 위치 | 스코프 | 공유 | 용도 예시 |
|------|--------|:----:|----------|
| `~/.claude/settings.json` | 전체 프로젝트 | X | 데스크톱 알림, 개인 보안 규칙 |
| `.claude/settings.json` | 단일 프로젝트 | O (Git) | 팀 코드 포맷팅, 프로젝트 보안 |
| `.claude/settings.local.json` | 단일 프로젝트 | X | 개인 실험용 hook |
| Managed policy | 조직 전체 | O (관리자) | 기업 보안 정책 |
| Plugin `hooks/hooks.json` | 플러그인 활성 시 | O | 플러그인 번들 hook |
| Skill/Agent frontmatter | 컴포넌트 활성 시 | O | 스킬별 검증 |

### 2.6 설정 구조 (3-level nesting)

```json
{
  "hooks": {
    "PostToolUse": [                    // 1단계: 이벤트 선택
      {
        "matcher": "Edit|Write",        // 2단계: 필터링 (정규식)
        "hooks": [                      // 3단계: 핸들러 배열
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

---

## 3. Hook 생성 방법

### 3.1 `/hooks` 메뉴로 생성하기

Claude Code CLI에서 `/hooks`를 입력하면 인터랙티브 메뉴가 열린다.

**워크플로우:**

```
/hooks 입력
  → Step 1: 이벤트 목록에서 선택 (예: PostToolUse)
    → Step 2: Matcher 설정 (예: Edit|Write 또는 * 전체)
      → Step 3: "+ Add new hook..." → 커맨드 입력
        → Step 4: 저장 위치 선택
          ├─ User settings    (~/.claude/settings.json)
          ├─ Project settings  (.claude/settings.json)
          └─ Local settings    (.claude/settings.local.json)
  → Esc: CLI 복귀, 즉시 활성화
```

**메뉴 기능:**

| 기능 | 설명 |
|------|------|
| 조회 | 이벤트별 등록된 hooks 표시. 소스 레이블(`[User]`, `[Project]`, `[Local]`, `[Plugin]`) 포함 |
| 추가 | 이벤트 → matcher → handler type → 커맨드/프롬프트 입력 → 저장 위치 |
| 삭제 | 해당 hook 선택 후 삭제 |
| 전체 비활성화 | "Disable all hooks" 토글 (`disableAllHooks: true` 설정) |

**장점과 한계:**

- 장점: 이벤트/matcher를 목록에서 선택하므로 오류 최소화, 추가 즉시 반영
- 한계: `async`, `timeout`, `once`, `statusMessage` 등 **고급 필드는 설정 불가** → 수동 편집 필요

---

### 3.2 Claude Code에게 자연어로 요청하기

Claude Code에게 hook 생성을 요청할 때는 다음 구조가 효과적이다:

```
[상황/문제] + [원하는 동작] + [이벤트/handler 힌트(선택)] + [저장 위치(선택)]
```

**시나리오별 요청 예시:**

#### (1) 파일 편집 후 자동 포맷팅

> "파일 수정 후 자동으로 prettier를 실행하는 PostToolUse hook을 만들어줘. `.claude/settings.json`에 저장해."

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true"
      }]
    }]
  }
}
```

#### (2) 위험 명령어 차단

> "rm -rf, DROP TABLE 같은 위험한 명령이 실행되지 않도록 PreToolUse hook으로 차단해줘."

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "if echo $(jq -r '.tool_input.command') | grep -qE 'rm\\s+-rf|DROP\\s+TABLE|truncate'; then echo 'Destructive command blocked' >&2; exit 2; fi"
      }]
    }]
  }
}
```

#### (3) 데스크톱 알림 (macOS)

> "Claude가 알림을 보낼 때 macOS 데스크톱 알림이 뜨게 해줘. 모든 프로젝트에 적용."

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude Code needs attention\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

#### (4) 작업 완료 전 테스트 게이트

> "Claude가 작업을 끝내기 전에 테스트가 통과하는지 확인하는 Stop hook을 만들어줘. agent type으로."

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "agent",
        "prompt": "Run the test suite and verify all tests pass before allowing Claude to stop. $ARGUMENTS",
        "timeout": 120
      }]
    }]
  }
}
```

#### (5) 환경변수 로딩

> "세션 시작 시 .env 파일의 환경변수를 자동으로 로딩하는 hook을 만들어줘."

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "if [ -f .env ] && [ -n \"$CLAUDE_ENV_FILE\" ]; then grep -v '^#' .env | grep '=' >> \"$CLAUDE_ENV_FILE\"; fi"
      }]
    }]
  }
}
```

#### (6) 보호 파일 수정 차단

> ".env, package-lock.json, .git/ 하위 파일을 수정 못하게 하는 hook을 만들어줘."

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "FILE=$(jq -r '.tool_input.file_path'); for p in .env package-lock.json .git/; do case \"$FILE\" in *\"$p\"*) echo \"Protected: $FILE\" >&2; exit 2;; esac; done"
      }]
    }]
  }
}
```

#### (7) Compact 후 컨텍스트 복원

> "컨텍스트 compact 후 프로젝트 핵심 정보를 다시 주입하는 hook을 만들어줘."

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo 'Reminder: use bun (not npm). Run bun test before committing. Current sprint: auth refactoring.'"
      }]
    }]
  }
}
```

#### (8) Bash 명령 로깅

> "실행되는 모든 Bash 명령을 로그 파일에 기록하는 hook을 설정해줘."

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r '[.session_id, (.tool_input.command // \"N/A\")] | @tsv' >> /tmp/claude-bash-audit.log"
      }]
    }]
  }
}
```

**효과적인 요청 팁:**

- **이벤트명을 명시**하면 정확도가 높아진다 ("PostToolUse hook으로..." vs "파일 수정 후...")
- **handler type을 지정**하면 의도에 맞는 결과를 얻는다 ("agent type으로", "command hook으로")
- **저장 위치를 지정**한다 (`settings.json`, `settings.local.json`, `~/.claude/settings.json`)
- **matcher 패턴을 알려주면** 더 정밀하다 ("Edit|Write에 대해서만")
- 구체적 시나리오 설명이 "hook 만들어줘"보다 효과적이다

---

### 3.3 수동 JSON 편집

settings.json을 직접 편집할 때 주의사항:

- **세션 중 편집 시**: Claude Code는 시작 시 hooks 스냅샷을 캡처한다. 세션 도중 외부 편집하면 `/hooks` 메뉴에서 리뷰해야 변경이 적용된다.
- **고급 필드**: `/hooks` 메뉴에서 설정할 수 없는 필드는 수동 편집이 필요하다.

```json
{
  "type": "command",
  "command": "./scripts/lint.sh",
  "timeout": 30,              // 초 단위 (기본 600)
  "async": true,              // 백그라운드 실행 (Claude는 즉시 다음 작업 진행)
  "statusMessage": "Linting...",  // 실행 중 스피너에 표시할 메시지
  "once": true                // 세션당 1회만 실행 (스킬 전용)
}
```

> `async: true`인 hook은 `decision`, `permissionDecision`, `continue` 등 제어 필드를 사용할 수 없다. `systemMessage`와 `additionalContext`만 다음 턴에 전달된다.

---

### 3.4 방법별 비교

| 항목 | `/hooks` 메뉴 | Claude Code에게 요청 | 수동 JSON 편집 |
|------|:-------------:|:-------------------:|:-------------:|
| 난이도 | 쉬움 | 쉬움 | 중간 |
| 고급 필드 설정 | X | O | O |
| 즉시 반영 | O | O | 리뷰 필요 |
| 복잡한 로직 | 제한적 | O | O |
| 별도 스크립트 파일 | X | O (생성 가능) | 수동 작성 |
| 추천 상황 | 단순 hook 빠르게 추가 | 복잡한 hook, 스크립트 포함 | 기존 hook 세부 조정 |

---

## 4. 개발 시나리오별 Use Case

### 4.1 코드 품질 & 포맷팅

| 시나리오 | 이벤트 | Matcher | Handler | 설명 |
|----------|--------|---------|---------|------|
| 자동 포맷팅 | `PostToolUse` | `Edit\|Write` | command | Prettier, Black 등 포맷터 자동 실행 |
| 린트 피드백 | `PostToolUse` | `Edit\|Write` | command | ESLint/Ruff 결과를 Claude에 전달 |
| 타입 체크 | `PostToolUse` | `Edit\|Write` | command (async) | TypeScript tsc 백그라운드 실행 |

### 4.2 보안 & 접근 제어

| 시나리오 | 이벤트 | Matcher | Handler | 설명 |
|----------|--------|---------|---------|------|
| 위험 명령어 차단 | `PreToolUse` | `Bash` | command | `rm -rf`, `DROP TABLE` 등 차단 |
| 보호 파일 편집 차단 | `PreToolUse` | `Edit\|Write` | command | `.env`, secrets 등 보호 |
| MCP 쓰기 작업 검증 | `PreToolUse` | `mcp__.*` | command | MCP 도구 호출 전 검증 |
| 설정 변경 감사 | `ConfigChange` | (전체) | command | 설정 변경 로그 기록 |
| 권한 자동 처리 | `PermissionRequest` | (tool명) | command | 특정 도구 자동 허용/거부 |

### 4.3 테스트 & 검증

| 시나리오 | 이벤트 | Matcher | Handler | 설명 |
|----------|--------|---------|---------|------|
| 작업 완료 전 테스트 게이트 | `Stop` | - | agent | 테스트 통과 여부 확인 후 중단 허용 |
| 파일 편집 후 관련 테스트 | `PostToolUse` | `Edit\|Write` | command (async) | 변경 파일 관련 테스트 비동기 실행 |
| Task 완료 검증 | `TaskCompleted` | - | command | 빌드 아티팩트 존재 확인 |
| 서브에이전트 결과 검증 | `SubagentStop` | (agent명) | prompt | 결과 품질 평가 |

### 4.4 알림 & 모니터링

| 시나리오 | 이벤트 | Matcher | Handler | 설명 |
|----------|--------|---------|---------|------|
| 데스크톱 알림 | `Notification` | (전체) | command | 권한 요청/유휴 시 OS 알림 |
| Bash 명령 로깅 | `PostToolUse` | `Bash` | command | 실행 명령 감사 로그 |
| 도구 실패 알림 | `PostToolUseFailure` | (전체) | command | 실패 시 Slack/이메일 알림 |

### 4.5 세션 관리 & 컨텍스트

| 시나리오 | 이벤트 | Matcher | Handler | 설명 |
|----------|--------|---------|---------|------|
| 환경변수 로딩 | `SessionStart` | `startup` | command | `CLAUDE_ENV_FILE`로 영속 설정 |
| Compact 후 컨텍스트 복원 | `SessionStart` | `compact` | command | 핵심 정보 재주입 |
| 프롬프트 필터링 | `UserPromptSubmit` | - | command | 부적절한 프롬프트 차단/변환 |
| 세션 종료 정리 | `SessionEnd` | (전체) | command | 임시 파일 삭제, 로그 저장 |
| Compact 전 메모 저장 | `PreCompact` | `auto` | command | 중요 정보를 파일에 기록 |

### 4.6 팀 협업 & 서브에이전트

| 시나리오 | 이벤트 | Matcher | Handler | 설명 |
|----------|--------|---------|---------|------|
| Teammate idle 시 품질 게이트 | `TeammateIdle` | - | command | 린트 통과 확인 후 idle 허용 |
| Task 완료 검증 | `TaskCompleted` | - | command | 테스트 통과 확인 |
| 서브에이전트 컨텍스트 주입 | `SubagentStart` | (agent명) | command | 보안 가이드라인 주입 |

---

## 5. 실전 구현 예시

### 5.1 파일 편집 후 자동 포맷팅

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true",
        "timeout": 30
      }]
    }]
  }
}
```

### 5.2 위험 명령어 차단 (별도 스크립트)

**settings.json:**

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/scripts/block-dangerous.sh"
      }]
    }]
  }
}
```

**scripts/block-dangerous.sh:**

```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command')
BLOCKED_PATTERNS='rm\s+-rf|DROP\s+TABLE|TRUNCATE\s+TABLE|git\s+push\s+.*--force'

if echo "$COMMAND" | grep -qE "$BLOCKED_PATTERNS"; then
  echo "Blocked: destructive command detected" >&2
  exit 2
fi
exit 0
```

### 5.3 보호 파일 편집 방지

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
PROTECTED=(".env" ".env.local" "package-lock.json" ".git/")

for pattern in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Protected file: $FILE_PATH" >&2
    exit 2
  fi
done
exit 0
```

### 5.4 데스크톱 알림 (macOS / Linux)

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "if [ \"$(uname)\" = \"Darwin\" ]; then osascript -e 'display notification \"Claude Code needs attention\" with title \"Claude Code\"'; else notify-send 'Claude Code' 'Needs attention'; fi"
      }]
    }]
  }
}
```

### 5.5 Compact 후 컨텍스트 복원

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo \"[Context restored] Use bun (not npm). Current sprint: auth refactoring. Run bun test before commits.\""
      }]
    }]
  }
}
```

동적 컨텍스트가 필요하면 git 정보를 포함할 수 있다:

```bash
#!/bin/bash
BRANCH=$(git branch --show-current 2>/dev/null)
RECENT=$(git log --oneline -3 2>/dev/null)
echo "Branch: $BRANCH | Recent commits: $RECENT"
```

### 5.6 작업 완료 전 테스트 강제 (Agent Hook)

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "agent",
        "prompt": "Check if the stop is appropriate. Context: $ARGUMENTS\n\n1. Look at the conversation to understand what was requested\n2. Run the test suite to verify all tests pass\n3. If tests fail, respond with {\"ok\": false, \"reason\": \"Tests failing: ...\"}\n4. If all good, respond with {\"ok\": true}",
        "timeout": 120
      }]
    }]
  }
}
```

> **무한루프 방지**: Stop hook의 stdin에는 `stop_hook_active` 필드가 포함된다. 이미 Stop hook에 의해 재시작된 경우 이 값이 `true`이므로, 필요시 이 필드를 확인하여 즉시 `exit 0`으로 빠져나와야 한다.

---

## 6. Matcher 패턴 가이드

Matcher는 정규식(regex) 기반이며, 이벤트에 따라 매칭 대상이 다르다.

**패턴 문법:**

| 패턴 | 의미 | 예시 |
|------|------|------|
| `Bash` | 정확 매칭 | Bash 도구만 |
| `Edit\|Write` | OR 매칭 | Edit 또는 Write |
| `mcp__.*` | 와일드카드 | 모든 MCP 도구 |
| `mcp__github__.*` | 서버 필터 | GitHub MCP 서버의 모든 도구 |
| `""` 또는 생략 | 전체 매칭 | 모든 대상에 발동 |

**이벤트별 Matcher 대상:**

| 이벤트 | 매칭 대상 |
|--------|----------|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` | tool 이름 |
| `SessionStart` | 시작 방식 (`startup`, `resume`, `clear`, `compact`) |
| `SessionEnd` | 종료 사유 (`clear`, `logout`, `prompt_input_exit` 등) |
| `Notification` | 알림 유형 (`permission_prompt`, `idle_prompt` 등) |
| `SubagentStart`, `SubagentStop` | agent type |
| `PreCompact` | 트리거 유형 (`manual`, `auto`) |
| `ConfigChange` | 설정 소스 (`user_settings`, `project_settings`, `skills`) |
| 나머지 (`UserPromptSubmit`, `Stop` 등) | matcher 미지원 — 항상 발동 |

---

## 7. Exit Code와 JSON 출력

### 7.1 Exit Code 동작 규칙

| Exit Code | 의미 | 동작 |
|-----------|------|------|
| **0** | 성공 | stdout의 JSON 파싱. `UserPromptSubmit`/`SessionStart`는 Claude 컨텍스트에 추가 |
| **2** | 차단 | stderr를 Claude에 에러로 전달. JSON 무시 |
| **기타** | 비차단 에러 | stderr는 verbose 모드에서만 표시. 실행 계속 |

### 7.2 JSON 출력 구조 (exit 0 시)

공통 필드:

| 필드 | 기본값 | 설명 |
|------|--------|------|
| `continue` | `true` | `false`이면 Claude 완전 중단 |
| `stopReason` | - | `continue: false` 시 사용자에게 표시 |
| `suppressOutput` | `false` | `true`이면 verbose 출력 숨김 |
| `systemMessage` | - | 사용자에게 경고 메시지 표시 |

### 7.3 이벤트별 Decision Control

| 이벤트 그룹 | 패턴 | 핵심 필드 |
|-------------|------|----------|
| `UserPromptSubmit`, `PostToolUse`, `Stop` 등 | 최상위 `decision` | `decision: "block"`, `reason` |
| `PreToolUse` | `hookSpecificOutput` | `permissionDecision` (allow/deny/ask), `updatedInput`, `additionalContext` |
| `PermissionRequest` | `hookSpecificOutput` | `decision.behavior` (allow/deny), `updatedInput` |
| `TeammateIdle`, `TaskCompleted` | exit code만 | exit 2 + stderr 메시지 |

**PreToolUse의 `updatedInput` (v2.0.10+):**

도구 호출 전 파라미터를 수정할 수 있다:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "npm run lint -- --fix"
    },
    "additionalContext": "Production environment. Proceed with caution."
  }
}
```

---

## 8. 디버깅 & 트러블슈팅

**디버깅 도구:**

| 방법 | 설명 |
|------|------|
| `claude --debug` | hook 매칭/실행 상세 로그 |
| `Ctrl+O` | verbose 모드 토글 (hook 출력 표시) |
| `/hooks` | 등록된 hooks 확인, 소스 레이블 포함 |

**트러블슈팅 체크리스트:**

| 문제 | 원인/해결 |
|------|----------|
| Hook이 실행되지 않음 | `/hooks`에서 해당 hook 존재 확인. matcher 대소문자/정규식 검증. 이벤트 타입 확인 |
| Stop hook 무한루프 | stdin의 `stop_hook_active` 필드 확인. `true`이면 즉시 `exit 0` |
| JSON 파싱 실패 | 쉘 프로필(`~/.zshrc`)의 `echo` 문이 stdout 오염. `[[ $- == *i* ]]` 조건으로 감싸기 |
| 스크립트 실행 안됨 | `chmod +x` 확인. shebang (`#!/bin/bash`) 확인 |
| 수동 편집 미반영 | 세션 중 외부 편집 시 `/hooks` 메뉴에서 리뷰 필요. 또는 세션 재시작 |
| 경로 문제 | `$CLAUDE_PROJECT_DIR` 사용 권장. 상대 경로보다 절대 경로가 안전 |

---

## 9. 참고 자료

- [Hooks Reference (공식)](https://code.claude.com/docs/en/hooks) — 전체 이벤트 스키마, JSON 입출력 포맷
- [Automate workflows with hooks (공식 가이드)](https://code.claude.com/docs/en/hooks-guide) — 첫 hook 설정 워크스루, 자동화 예제
- [Claude Code Hooks Mastery (GitHub)](https://github.com/disler/claude-code-hooks-mastery) — 커뮤니티 예제 모음
- 이 저장소: `docs/RESEARCH-CLAUDE-CODE-SETTINGS-REFERENCE-2026-02-20-1200.md` — settings.json 전체 설정 참조

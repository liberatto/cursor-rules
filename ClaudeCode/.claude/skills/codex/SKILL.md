---
name: codex
description: Use when the user asks to run Codex CLI (codex exec, codex resume, codex review, codex fork) or references OpenAI Codex for code analysis, refactoring, planning, validation, testing, or automated editing
---

# Codex Skill Guide

> **CLI**: 0.104.0+ | **Tier**: Plus | **Config**: `~/.codex/config.toml`

## Available Models (Plus)

| Model | 특징 | Credit/msg |
| --- | --- | --- |
| `gpt-5.3-codex` | 최고 성능, 권장 | 5 |
| `gpt-5.2-codex` | 안정적, API 키 워크플로우 권장 | 5 |
| `gpt-5.1-codex-mini` | 경량, 비용 1/5 | 1 |

> `gpt-5.3-codex-spark`는 Pro 전용 — Plus에서 사용 불가.

## Execution Workflow

### Step 1: Gather Parameters

`AskUserQuestion`으로 **두 질문을 한 번에** 수집:

1. **Model**: `gpt-5.3-codex` (recommended), `gpt-5.2-codex`, `gpt-5.1-codex-mini`
2. **Reasoning effort**: `xhigh`, `high`, `medium`, `low`

### Step 2: Determine Sandbox Mode

| 작업 유형 | Sandbox | 플래그 |
| --- | --- | --- |
| 읽기 전용 분석 | `read-only` (기본) | `-s read-only` |
| 로컬 파일 편집 | `workspace-write` | `--full-auto` |
| 네트워크/광범위 접근 | `danger-full-access` | `-s danger-full-access --full-auto` |

### Step 3: Build and Run Command

```bash
codex exec --skip-git-repo-check \
  -m <MODEL> \
  -c model_reasoning_effort="<EFFORT>" \
  <SANDBOX_FLAGS> \
  "prompt here" 2>/dev/null
```

**필수 규칙:**

- `exec`에는 항상 `--skip-git-repo-check` 사용.
- 항상 `2>/dev/null`로 stderr(thinking tokens) 억제. 사용자가 디버깅 요청 시에만 stderr 표시.
- `-C <DIR>`로 작업 디렉토리 지정.
- stdin으로 프롬프트 전달 가능: `echo "prompt" | codex exec ...` 또는 프롬프트 인자에 `-` 사용.

**exec 선택 플래그:**

| Flag | 용도 |
| --- | --- |
| `-i <FILE>...` | 이미지 첨부 (PNG, JPG, GIF, WebP) |
| `--add-dir <DIR>` | 추가 쓰기 허용 디렉토리 |
| `--output-schema <FILE>` | JSON Schema로 응답 형태 제한 |
| `--json` | JSONL 스트림 출력 |
| `-o, --output-last-message <FILE>` | 마지막 메시지를 파일로 저장 |
| `-p <PROFILE>` | config.toml 프로파일 선택 |
| `--ephemeral` | 세션 파일 저장 안 함 |
| `--enable <FEATURE>` | 피처 플래그 활성화 |
| `--disable <FEATURE>` | 피처 플래그 비활성화 |
| `--color <COLOR>` | 색상 설정 (`always`, `never`, `auto`) |

### Step 4: Report and Follow Up

완료 후 사용자에게: *"codex resume으로 이 세션을 이어서 진행할 수 있습니다."*

`AskUserQuestion`으로 다음 단계 확인.

## Interactive Mode

```bash
# 대화형 세션 시작
codex "prompt here"
codex -m gpt-5.3-codex --full-auto "prompt here"
```

**인터랙티브 전용 추가 플래그:**

| Flag | 용도 |
| --- | --- |
| `-a <POLICY>` | 승인 정책 설정 (`untrusted`, `on-request`, `never`) |
| `--search` | 웹 검색 도구 활성화 |
| `--no-alt-screen` | 인라인 TUI 모드 (스크롤백 유지) |

## Resume and Fork

### Resume (이전 세션 이어서)

```bash
# 비대화형: 마지막 세션 이어서
echo "follow-up prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null

# 대화형: 세션 선택 picker
codex resume

# 마지막 세션 바로 이어서
codex resume --last

# 특정 세션 ID로 이어서
codex resume <SESSION_ID>

# 모든 세션 표시 (cwd 필터 무시)
codex resume --all
```

- 원본 세션의 model, reasoning effort, sandbox 설정을 상속.
- 사용자가 명시 요청 시에만 설정 플래그 추가.

### Fork (이전 세션에서 분기)

```bash
codex fork --last "다른 접근 시도"
codex fork <SESSION_ID> "새로운 방향"
codex fork --all  # 모든 세션 picker 표시
```

- 이전 세션에서 분기한 새 세션 생성.

## Code Review

비대화형 코드 리뷰:

```bash
# 커밋 안 된 변경사항 (staged + unstaged + untracked)
codex review --uncommitted 2>/dev/null

# 베이스 브랜치 대비 변경사항
codex review --base main 2>/dev/null

# 특정 커밋
codex review --commit <SHA> 2>/dev/null

# 타이틀 컨텍스트 포함
codex review --uncommitted --title "Add auth module" 2>/dev/null

# 커스텀 리뷰 지침
codex review --uncommitted "보안 취약점에 집중" 2>/dev/null
```

> Plus 기준 주간 10-25건 리뷰 가능.

## Apply Diff

Codex 에이전트가 생성한 diff를 로컬 working tree에 적용:

```bash
codex apply <TASK_ID>
```

## Codex Cloud (Experimental)

원격으로 태스크를 실행하고 결과를 로컬에 적용:

```bash
codex cloud exec --env <ENV_ID> "refactor the auth module"  # 태스크 제출
codex cloud exec --env <ENV_ID> --attempts 3 "fix the bug"  # best-of-N 시도
codex cloud list                                             # 태스크 목록
codex cloud status <TASK_ID>                                 # 상태 확인
codex cloud diff <TASK_ID>                                   # diff 보기
codex cloud apply <TASK_ID>                                  # 로컬 적용
```

> `--env <ENV_ID>`는 필수. Plus 기준 5시간당 10-60건 제한.

## MCP Integration

```bash
codex mcp list              # 등록된 MCP 서버 목록
codex mcp get <NAME>        # 특정 서버 정보
codex mcp add <NAME>        # 서버 추가
codex mcp remove <NAME>     # 서버 제거
codex mcp login <NAME>      # 서버 로그인
codex mcp logout <NAME>     # 서버 로그아웃
codex mcp-server             # Codex를 MCP 서버로 시작 (stdio)
```

## Feature Flags

피처 확인 및 관리:

```bash
codex features list              # 전체 피처 목록 (stage, 상태)
codex features enable <NAME>     # config.toml에서 활성화
codex features disable <NAME>    # config.toml에서 비활성화
```

주요 stable 피처:

| Feature | 기본값 | 용도 |
| --- | --- | --- |
| `shell_tool` | true | 셸 도구 사용 |
| `unified_exec` | true | PTY 기반 명령 실행 |
| `shell_snapshot` | true | 셸 환경/rc 파일 스냅샷 |
| `steer` | true | Steer 모드 (Enter=전송, Tab=큐잉) |
| `collaboration_modes` | true | 협업 모드 |
| `personality` | true | Personality 설정 |
| `enable_request_compression` | true | 요청 압축 |

주요 experimental/dev 피처:

| Feature | 용도 |
| --- | --- |
| `js_repl` | JavaScript REPL 런타임 (상태 유지) |
| `multi_agent` | 멀티 에이전트 |
| `apps` | Apps SDK 앱 지원 |
| `prevent_idle_sleep` | 유휴 시 슬립 방지 |

> `--enable`/`--disable` 플래그로 실행 시 일회성 토글 가능.

## Interactive Slash Commands

대화형 세션에서 사용 가능:

| Command | 용도 |
| --- | --- |
| `/m_update` | 세션 메모리 업데이트 |
| `/m_drop` | 세션 메모리 삭제 |
| `/statusline` | TUI 푸터 메타데이터 커스터마이징 |
| `/model` | 세션 중 모델 전환 |

## Approval Policy Reference

`-a, --ask-for-approval` 플래그 (인터랙티브/resume/fork 전용):

| Policy | 동작 |
| --- | --- |
| `untrusted` | 신뢰 명령(ls, cat 등) 자동 실행; 나머지 프롬프트 |
| `on-request` | 모델이 승인 필요 시점 결정 (`--full-auto` 기본값) |
| `never` | 프롬프트 없음; 실패 시 모델에 직접 전달 |

## Config Override Syntax

```bash
# -c로 config 값 오버라이드 (TOML 파싱)
codex exec -c model="gpt-5.3-codex" -c model_reasoning_effort="high" ...

# 중첩 값은 점 경로
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' ...
codex exec -c shell_environment_policy.inherit=all ...
```

주요 config 키:

```toml
model = "gpt-5.3-codex"
model_reasoning_effort = "high"           # xhigh | high | medium | low
personality = "pragmatic"                  # none | friendly | pragmatic
command_attribution = "default"            # default | custom | disabled
model_instructions_file = "path"           # 커스텀 instruction 파일
web_search = "cached"                      # disabled | cached | live
```

## Environment Variables

| Variable | 용도 |
| --- | --- |
| `WS_PROXY` / `WSS_PROXY` | WebSocket 프록시 (소문자 변형도 지원) |

## Error Handling

- `codex` 비정상 종료 시 중단하고 보고; 재시도 전 사용자 확인.
- 고위험 플래그(`--full-auto`, `-s danger-full-access`, `--skip-git-repo-check`) 사용 전 `AskUserQuestion`으로 사용자 허가 (이미 부여된 경우 제외).
- 경고나 부분 결과는 요약 후 진행 방법 확인.

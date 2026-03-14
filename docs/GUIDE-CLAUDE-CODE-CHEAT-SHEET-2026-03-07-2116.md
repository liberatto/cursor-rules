# Claude Code Cheat Sheet

> Everything you need in one place — Commands, Shortcuts, Features & Tips
>
> Original: [Claude Code Cheat Sheet](https://www.reddit.com/r/ClaudeAI/comments/1lkfd3h/claude_code_cheat_sheet/) (Reddit)
>
> Cross-checked: v2.1.71 CLI + [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code) 공식 문서 기준 검증 완료.

---

## 1. Keyboard Shortcuts

> Source: [Interactive mode - Keyboard shortcuts](https://docs.anthropic.com/en/docs/claude-code/interactive-mode)

### General Controls

| 단축키 | 기능 |
|--------|------|
| `Enter` | 메시지 전송 / 확인 |
| `Ctrl+C` | 현재 입력 또는 생성 취소 |
| `Ctrl+D` | Claude Code 세션 종료 (EOF) |
| `Ctrl+G` | 기본 텍스트 에디터에서 프롬프트 편집 |
| `Ctrl+L` | 터미널 화면 클리어 (대화 히스토리 유지) |
| `Ctrl+O` | Verbose 출력 토글 (상세 도구 사용 표시) |
| `Ctrl+R` | 명령 히스토리 역방향 검색 |
| `Ctrl+F` | 백그라운드 에이전트 전체 종료 (3초 내 2회 누름) |
| `Ctrl+V` / `Cmd+V` | 클립보드 이미지 붙여넣기 |

### Text Editing

| 단축키 | 기능 |
|--------|------|
| `Ctrl+K` | 커서부터 줄 끝까지 삭제 |
| `Ctrl+U` | 현재 줄 전체 삭제 |
| `Ctrl+Y` | 삭제한 텍스트 붙여넣기 (`Ctrl+K/U`로 삭제한 것) |
| `Alt+Y` | 붙여넣기 히스토리 순환 (`Ctrl+Y` 이후) |
| `Alt+B` | 커서를 한 단어 뒤로 이동 |
| `Alt+F` | 커서를 한 단어 앞으로 이동 |

### Quick Commands

| 단축키 | 기능 |
|--------|------|
| `/` (입력 시작) | 슬래시 커맨드 또는 스킬 |
| `!` (입력 시작) | Bash 모드 — 셸 명령 직접 실행 |
| `@` | 파일/폴더 경로 멘션 (자동완성) |

### Line Break 입력

| 방법 | 설명 |
|------|------|
| `\` + `Enter` | 줄바꿈 입력 (빠른 방법) |
| `Shift+Enter` | iTerm2, WezTerm, Ghostty, Kitty에서 기본 지원 |

---

## 2. Slash Commands

> Source: [Interactive mode - Built-in commands](https://docs.anthropic.com/en/docs/claude-code/interactive-mode)

### Session Control

| 명령어 | 기능 |
|--------|------|
| `/clear` | 대화 히스토리 초기화. Alias: `/reset`, `/new` |
| `/compact [focus]` | 컨텍스트 압축 (토큰 절약). 선택적 집중 지시 |
| `/review` | 코드 변경사항 되돌아가기 (`gh` 연동) |
| `/rewind` | 체크포인트로 되돌리기. Alias: `/checkpoint` |
| `/export [file]` | 대화를 파일 또는 클립보드로 내보내기 |
| `/cost` | 세션 토큰 사용량 통계 표시 |
| `/context` | 현재 컨텍스트 사용량을 컬러 그리드로 시각화 |

### Configuration

| 명령어 | 기능 |
|--------|------|
| `/config` | 설정 인터페이스 열기. Alias: `/settings` |
| `/model [model]` | 모델 전환: sonnet / opus / haiku |
| `/permissions` | 권한 설정 보기 & 수정. Alias: `/allowed-tools` |
| `/terminal-setup` | 터미널 줄바꿈 설정 |
| `/keybindings` | 키보드 단축키 커스터마이즈 |
| `/output-style [style]` | 출력 스타일 변경 |
| `/fast [on\|off]` | Fast 모드 토글 |

### Tools & Extensions

| 명령어 | 기능 |
|--------|------|
| `/doctor` | 환경 진단 & 헬스 체크 |
| `/agents` | 에이전트 설정 관리 |
| `/mcp` | MCP 서버 관리 |
| `/hooks` | Hooks 설정 관리 |
| `/plugin` | 플러그인 관리 |
| `/ide` | IDE 연결 |

### Session & Navigation

| 명령어 | 기능 |
|--------|------|
| `/resume [session]` | 세션 복원. Alias: `/continue` |
| `/fork [name]` | 현재 세션 포크 |
| `/rename [name]` | 세션 이름 변경 |
| `/copy` | 마지막 응답을 클립보드에 복사 |
| `/diff` | 변경 사항 diff 표시 |

### Account & GitHub

| 명령어 | 기능 |
|--------|------|
| `/login` | 계정 인증 |
| `/logout` | 로그아웃 |
| `/install-github-app` | GitHub 자동 PR 리뷰 설정 |
| `/install-slack-app` | Slack 앱 설치 |
| `/pr-comments [PR]` | GitHub PR 피드백 보기 |

### Others

| 명령어 | 기능 |
|--------|------|
| `/init` | CLAUDE.md 초기 생성 |
| `/memory` | CLAUDE.md 편집 |
| `/help` | 사용 가능한 커맨드 표시 |
| `/plan` | Plan 모드 |
| `/feedback` | 피드백 보내기. Alias: `/bug` |
| `/release-notes` | 릴리즈 노트 확인 |

---

## 3. CLI Launch Flags

> Source: [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

### Starting Sessions

| 플래그 | 기능 |
|--------|------|
| `claude` | 대화형 세션 시작 |
| `claude "query"` | 초기 프롬프트와 함께 시작 |
| `claude -p "query"` | Print 모드 — 응답 출력 후 종료 (스크립팅용) |
| `claude -c` | 마지막 대화 이어서 시작 (`--continue`) |
| `claude -r "name"` | 특정 세션을 이름 또는 ID로 복원 (`--resume`) |
| `claude -w [name]` | 새 git worktree에서 세션 시작 (`--worktree`) |

### Model & Budget

| 플래그 | 기능 |
|--------|------|
| `--model sonnet` | 모델 지정 (alias 또는 전체 이름) |
| `--model opus` | Opus 모델 사용 |
| `--permission-mode plan` | Plan 모드로 시작 |
| `--max-turns N` | 최대 에이전트 턴 수 제한 (`-p` 모드 전용) |
| `--max-budget-usd N` | 비용 상한 설정 (`-p` 모드 전용) |

### Context & Integration

| 플래그 | 기능 |
|--------|------|
| `--add-dir ./path` | 추가 디렉토리를 컨텍스트에 포함 |
| `--chrome` | Chrome 브라우저 통합 활성화 |
| `--verbose` | 상세 로깅 표시 |
| `--mcp-config ./mcp.json` | MCP 서버 설정 파일 로드 |
| `--from-pr 123` | PR에 연결된 세션 복원 |

### Output Control

| 플래그 | 기능 |
|--------|------|
| `--allowedTools "Bash(git:*) Edit"` | 허용할 도구 지정 |
| `--disallowedTools "Edit"` | 차단할 도구 지정 |
| `--tools "Bash,Edit,Read"` | 사용 가능한 도구 목록 지정 |
| `--output-format text` | 텍스트 출력 (default) |
| `--output-format json` | JSON 출력 |
| `--output-format stream-json` | 실시간 스트리밍 JSON |

> **Tip**: `cat file.py | claude -p "review this" | tee output.log` — 파이프라인으로 연결 가능

---

## 4. The Big 5 — Claude Code Extension System

Claude Code는 5가지 핵심 확장 체계를 가진다:

### 4.1 Agents (Sub-Agents)

| 항목 | 설명 |
|------|------|
| **What** | 독립적인 Claude 인스턴스. 자체 컨텍스트 & 도구 보유 |
| **Where** | `.claude/agents/*.md` (project) |
| **Invoke** | `my agent: <message>` 또는 `@agents: '{json}'` |

### 4.2 Custom Slash Commands

| 항목 | 설명 |
|------|------|
| **What** | 재사용 가능한 Markdown 파일 (프롬프트 템플릿) |
| **Where** | `.claude/commands/{group}/{name}.md` |
| **Use** | `/group/name` → `$ARGUMENTS` 변수로 인자 전달 |

### 4.3 Skills (Auto-Matching Templates)

| 항목 | 설명 |
|------|------|
| **What** | Claude가 자동으로 사용 시점을 결정 — 직접 호출하지 않음 |
| **Where** | `.claude/skills/{name}/SKILL.md` |
| **How** | 프로젝트 작업 시 Claude가 컨텍스트에서 관련 스킬을 자동 선택 |

### 4.4 Hooks (Event Automation)

| 항목 | 설명 |
|------|------|
| **What** | 이벤트 기반 자동 실행 (command, http, prompt, agent 타입) |
| **Where** | `.claude/settings.json` 또는 `.claude/settings.local.json` |
| **Manage** | `/hooks` 슬래시 커맨드로 관리 |

### 4.5 MCP (Model Context Protocol)

| 항목 | 설명 |
|------|------|
| **What** | 외부 시스템 연결 (GitHub, Slack, DB, 브라우저 등) |
| **Setup** | `claude mcp add <name> <command>` |
| **List** | `claude mcp list` |
| **Config** | `--mcp-config ./mcp.json` at launch |

> **How they differ**: Custom Commands → **YOU** invoke them / Skills → **CLAUDE** invokes them / Sub Agents → Separate AI instances / MCP → External tool connections

---

## 5. Permission Modes

> Source: CLI `--permission-mode` choices

| 모드 | CLI 값 | 설명 |
|------|--------|------|
| **Default** | `default` | 모든 도구 사용에 대해 권한 확인 (기본값) |
| **Auto** | `auto` | 권한 요청 없이 자동 수락 |
| **Accept Edits** | `acceptEdits` | 파일 편집만 자동 수락 |
| **Plan** | `plan` | 코드 읽기 & 계획만 수행. 파일 쓰기/실행 불가 |
| **Don't Ask** | `dontAsk` | 모든 권한 요청 자동 수락 (auto보다 강력) |

> **Best workflow**: Plan Mode에서 문제 파악 → Default/Auto로 전환하여 구현

---

## 6. Hooks — Event Automation

> Source: [Hooks reference](https://docs.anthropic.com/en/docs/claude-code/hooks), [Hooks guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)

도구 실행 전후 또는 세션 이벤트에 맞춰 자동으로 실행한다. 4가지 타입: `command`, `http`, `prompt`, `agent`.

### 모든 타입 지원 이벤트

| Hook | 시점 | 용도 |
|------|------|------|
| `PreToolUse` | 도구 실행 **전** | 검증, 차단 (permissionDecision) |
| `PostToolUse` | 도구 실행 **후** (성공) | 결과 체크, 자동 포맷 |
| `PostToolUseFailure` | 도구 실행 **후** (실패) | 실패 로깅, 재시도 |
| `PermissionRequest` | 권한 대화상자 표시 시 | 자동 허용/거부 |
| `UserPromptSubmit` | 사용자 프롬프트 제출 시 | 입력 검증, 컨텍스트 주입 |
| `Stop` | Claude 응답 완료 시 | 후처리 |
| `SubagentStop` | 서브에이전트 완료 시 | 서브에이전트 결과 체크 |
| `TaskCompleted` | 작업 완료 표시 시 | 완료 검증 |

### command 타입만 지원 이벤트

| Hook | 시점 | 용도 |
|------|------|------|
| `SessionStart` | 세션 시작/복원 시 | 환경 초기화 |
| `SessionEnd` | 세션 종료 시 | 정리 |
| `PreCompact` | 컨텍스트 압축 전 | 중요 정보 보존 |
| `Notification` | 알림 전송 시 | 커스텀 알림 |
| `SubagentStart` | 서브에이전트 생성 시 | 로깅 |
| `TeammateIdle` | 팀원 에이전트 idle 시 | 작업 할당 |
| `ConfigChange` | 설정 파일 변경 시 | 설정 반영 |
| `WorktreeCreate` | Worktree 생성 시 | 초기 설정 |
| `WorktreeRemove` | Worktree 삭제 시 | 정리 |
| `InstructionsLoaded` | 지침 로드 시 | 부가 처리 |

---

## 7. Input Superpowers

| 입력 방식 | 설명 |
|-----------|------|
| `@mention` | 파일 & 폴더 참조. `@auth.js`, `@src/components/` |
| `!command` | Bash 모드 — 셸 명령 직접 실행하여 결과를 세션에 추가 |
| `Ctrl+V` | 이미지 붙여넣기 (스크린샷, 다이어그램) |
| Pipe Input | `cat file.py \| claude -p "explain"` — 파이프로 입력 전달 |
| `--add-dir` | `claude --add-dir ./src1 ./src2` — 여러 디렉토리 동시 작업 |
| `-r` | `claude -r feature` → 이름으로 세션 복원 |
| `-p` + `--output-format` | `claude -p --output-format json` — 스크립트 자동화 |

---

## 8. Configuration

> Source: [Settings](https://docs.anthropic.com/en/docs/claude-code/settings)

| 레벨 | 파일 위치 | 설명 |
|------|-----------|------|
| **Enterprise** | `~/.claude/code-manager-settings.json` | 관리자 설정 |
| **Project Shared** | `.claude/settings.json` | 팀 공유 설정 (git committed) |
| **Project Local** | `.claude/settings.local.json` | 개인 프로젝트 설정 (gitignored) |
| **User Global** | `~/.claude/settings.json` | 글로벌 기본값 |

> **Permissions example**: Allow git commands without asking: add `"Bash(git:*)"` to your allowedTools in settings.

---

## 9. File Structure Map

### Project Level (`.claude/`)

| 파일 | 역할 |
|------|------|
| `CLAUDE.md` | 프로젝트 메모리 — 컨벤션, 아키텍처, 지침 |
| `settings.json` | 공유 프로젝트 설정 (git committed) |
| `settings.local.json` | 개인 설정 (gitignored) |
| `commands/` | 프로젝트 슬래시 커맨드 (*.md 파일) |
| `skills/` | 프로젝트 스킬 (SKILL.md 포함 폴더) |
| `agents/` | 프로젝트 서브에이전트 (*.md 파일) |

### Global Level (`~/.claude/`)

| 파일 | 역할 |
|------|------|
| `CLAUDE.md` | 글로벌 메모리 (모든 프로젝트에 적용) |
| `settings.json` | 글로벌 설정 |
| `commands/` | 글로벌 슬래시 커맨드 |
| `skills/` | 글로벌 스킬 |
| `keybindings.json` | 커스텀 키보드 단축키 |

---

## 10. Rewind & Checkpoints

### 되돌리기

| 방법 | 기능 |
|------|------|
| `/rewind` | 체크포인트로 되돌리기. Alias: `/checkpoint` |
| `/review` | 코드 변경사항 리뷰 & 되돌리기 |

### Rewind 옵션

| 옵션 | 범위 |
|------|------|
| `Conversation` | 대화만 되돌리기. 코드는 그대로 유지 |
| `Code` | 파일만 복원. 대화는 유지 |
| `Full Reset` | 대화 AND 코드 모두 되돌리기 |

> **Note**: 도구 실행 부수효과(DB 변경, API 호출, 파일 삭제)는 되돌릴 수 없다. Checkpoints는 Claude의 파일 편집만 추적. Git을 영구 안전망으로 사용할 것.

---

## 11. Pro Workflow

### Starting a New Project

```bash
cd project && claude    # 1. 프로젝트 디렉토리에서 시작
# /init                 # 2. CLAUDE.md 생성
# Edit CLAUDE.md        # 3. 프로젝트 컨벤션 작성
# Code!                 # 4. 작업 시작
```

### Plan → Execute Pattern

```text
1. --permission-mode plan    → 문제 파악, 계획 수립
2. Review Claude's plan      → 접근 방식 확인
3. Switch to default/auto    → 구현 실행
```

### Saving Context

| 전략 | 설명 |
|------|------|
| `/compact` | 컨텍스트가 커지면 압축. 토큰 절약 |
| `/clear` | 새 작업 시작 시. 오래된 컨텍스트 제거 |
| `/export` | 대화 내보내기 |

### Focus Modes

| 모드 | 용도 |
|------|------|
| `Paste errors` | 전체 에러 메시지 붙여넣기. Claude가 원인 분석 |
| `Paste screenshots` | UI 스크린샷 붙여넣기. 시각적 분석 |
| `Pipe logs` | `cat error.log \| claude -p "What's wrong?"` |
| `/doctor` | 환경 진단 실행 |
| `Worktrees` | `claude -w feature-auth` — 격리된 worktree에서 작업 |
| `Multiple dirs` | `--add-dir ./api ./web` — 여러 저장소 동시 작업 |
| `Agent Teams` | 여러 Claude 인스턴스 동시 협업 |

---

## 12. Create Custom Commands

### 생성 단계

```text
1. Create file     → .claude/commands/review.md
2. Write prompt    → Markdown 내용이 곧 Claude에게 전달되는 프롬프트
3. Use it          → /project/review 입력
```

### Frontmatter 옵션

| 필드 | 설명 |
|------|------|
| `description` | 커맨드 설명 |
| `allowed-tools` | 커맨드가 사용할 수 있는 도구 제한 |
| `argument-hint` | 사용자에게 입력 인자 힌트 표시 |

### 유용한 팁

| 항목 | 설명 |
|------|------|
| `$ARGUMENTS` | 마크다운 안의 `$ARGUMENTS`는 사용자가 입력한 값으로 대체 |
| Example | `/project/review src/utils.ts` → `$ARGUMENTS` = `"src/utils.ts"` |

---

## 13. Quick Reference — Most Used Combos

### 기본 동작

| 작업 | 명령어 |
|------|--------|
| Start project | `cd project && claude` |
| Continue where I left off | `claude -c` |
| Quick question, no session | `claude -p "How do I..."` |
| Review my changes | `git diff \| claude -p "review"` |
| Explain error | `cat error.log \| claude -p "explain"` |
| Quick cost | `/cost` |
| Undo mistake | `/rewind` |

### Advanced Combos

| 작업 | 명령어 |
|------|--------|
| Parallel worktrees | `claude -w feature-a` + `claude -w feature-b` |
| Custom reviewer agent | `.claude/agents/reviewer.md` 생성 |
| Auto-format on edit | `PostToolUse` hook → run prettier |
| Resume session | `claude -r "Fix the bug"` |
| Resume from PR | `claude --from-pr 123` |
| Budget limit | `claude -p --max-budget-usd 3` |
| Scripted automation | `claude -p --output-format json` |

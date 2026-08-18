# rules — AI 개발 도구 하네스 원본 저장소

Claude Code · Codex · Claude Desktop 하네스의 **단일 진실 원천(Single Source of Truth)**. 글로벌 지침, 커스텀 커맨드, 서브에이전트, 스킬, 훅, 문서 컨벤션의 원본이 전부 여기 있고, 여기서 글로벌(`~/.claude/`)과 각 프로젝트로 나간다.

경로: `/Users/sspark/Work/rules` (`~/Work/rules`)

---

## 다른 프로젝트에서 이 저장소를 연결하는 법

두 가지가 모두 필요하다.

1. **`/add-dir ~/Work/rules`** — 파일 읽기·쓰기 권한을 연다. 세션마다 실행한다.
2. **그 프로젝트의 `CLAUDE.md`에 포인터 한 줄** — `add-dir`은 권한만 줄 뿐 이 저장소의 지침을 컨텍스트에 넣어주지 않으므로(검증됨: 추가 디렉토리의 `CLAUDE.md`는 자동 주입되지 않는다), 읽으라는 지시가 없으면 아무 일도 일어나지 않는다. 아래 한 줄이면 충분하다.

   ```markdown
   AI 하네스(스킬·커맨드·에이전트·글로벌 지침) 원본 저장소는 `~/Work/rules`다.
   여기 있는 하네스 자산을 가져오거나 개선분을 원본에 반영하는 작업이면, 먼저 `~/Work/rules/README.md`를 읽고 그 절차를 따른다.
   ```

## 이 저장소를 참조하는 Claude에게

아래 세 방향이 성립한다 — **어느 방향인지 먼저 판별하고 움직인다.**

| 방향 | 사용자 표현 | 해야 할 일 |
|---|---|---|
| ⬇️ 가져오기 | "원본 저장소에서 가져와", "rules에 있는 거 복사해" | 이 저장소의 해당 파일을 현재 프로젝트로 복사. 원본은 건드리지 않는다 |
| ⬆️ **역반영** | **"원본 저장소에도 반영해"**, "여기도 업데이트해" | 현재 프로젝트에서 개선한 파일을 이 저장소의 대응 경로에 반영. 아래 절차를 따른다 |
| ✏️ 직접 편집 | "글로벌 CLAUDE.md 고쳐", "이 스킬 수정해" | 이 저장소에서 편집한 뒤 배포까지 수행 |

### 역반영 절차 ("원본 저장소에도 반영해")

1. **대응 경로를 찾는다** — 아래 "디렉토리 지도"로 어디가 원본인지 판별. 배포 템플릿이면 `ClaudeCode/.claude/…`, 이 저장소 자체 설정이면 루트 `.claude/…`이다. 헷갈리면 같은 이름의 파일을 양쪽에서 grep해 확인한다.
2. **덮어쓰기 전에 원본을 읽는다** — 원본이 그새 앞서 있을 수 있다. 단순 복사가 아니라 차이를 확인한 뒤 병합한다.
3. **양쪽 동기화가 필요한지 본다** — 같은 자산이 루트 `.claude/`와 `ClaudeCode/.claude/` 양쪽에 존재하면 어느 쪽을 갱신할지 사용자에게 확인한다 (두 폴더는 현재 내용이 서로 다르다).
4. **글로벌로도 나가는 자산이면 배포까지** — 아래 "글로벌 배포 현황" 표를 보고 심링크면 추가 작업 불필요, 복사본이면 복사 명령까지 실행한다.
5. **커밋** — 변경 사유를 메시지에 남긴다. push가 필요하면 아래 "Git 규칙"을 따른다.

---

## 디렉토리 지도 — 무엇이 어디의 원본인가

| 경로 | 역할 | 나가는 곳 |
|---|---|---|
| `ClaudeCode/CLAUDE.v.*.md` | **글로벌 지침 정본**. 최신 버전 파일이 정본이며, 정적 `ClaudeCode/CLAUDE.md`는 없다 | `~/.claude/CLAUDE.md` (복사) |
| `ClaudeCode/.claude/` | 다른 프로젝트에 배포할 **템플릿** (agents · commands · skills · hooks · output-styles · settings) | 각 프로젝트 `.claude/` (복사) |
| `.claude/` (루트) | **이 저장소 자체**가 쓰는 로컬 설정 | `commands/ssp`만 글로벌 심링크 (원본은 `ClaudeCode/` 쪽) |
| `bootstrap-kit/` | 신규 프로젝트 부트스트랩 키트 (CLAUDE.md·CLAUDE.local.md 템플릿 + 자율 루프용 BACKLOG·PROMPT) | 폴더째 복사 |
| `Codex/` | OpenAI Codex CLI 설정 (`config.toml`, `AGENTS.md`) | `~/.codex/` (복사) |
| `ClaudeDesktop/` | Claude Desktop용 지침 (CHAT-PREFERENCES, COWORK-INSTRUCTIONS) | 수동 반영 |
| `docs/` | 이 저장소의 지식 자산 — 하네스 가이드·리서치·분석 문서 | 참조 전용 |
| `CLAUDE.md` / `CLAUDE.local.md` (루트) | 이 저장소 자체의 프로젝트 지침·운영 컨텍스트 | 배포 대상 아님 |

## 글로벌 배포 현황 — 심링크 vs 복사

**심링크는 이 저장소 파일을 고치는 즉시 글로벌에 반영된다.** 복사본은 복사 명령을 다시 실행해야 반영된다. 이 구분이 편집의 파급 범위를 결정하므로 건드리기 전에 확인한다.

| 대상 | 형태 | 글로벌 경로 |
|---|---|---|
| `.claude/commands/ssp/` | 🔗 **심링크** — 편집 즉시 글로벌 반영 | `~/.claude/commands/ssp` |
| `ClaudeCode/CLAUDE.v.*.md` (최신본) | 📋 복사 — `cp`로 갱신 필요 | `~/.claude/CLAUDE.md` |
| `Codex/config.toml` | 📋 복사 | `~/.codex/config.toml` |

현재 이 저장소에서 글로벌로 나간 심링크는 `commands/ssp` **하나뿐**이다. 스킬은 심링크로 배포된 것이 없다.

**2단 심링크 구조다.** `~/.claude/commands/ssp`는 루트 `.claude/commands/ssp/` 디렉토리를 통째로 가리키고, 그 안의 각 `.md`는 다시 `ClaudeCode/.claude/commands/ssp/`의 원본을 가리키는 상대 심링크다. 커맨드 실체는 `ClaudeCode/` 한 곳에만 있고, 루트 쪽은 **어느 커맨드를 글로벌로 내보낼지의 선택**만 표현한다.

```bash
ln -s ../../../ClaudeCode/.claude/commands/ssp/<name>.md .claude/commands/ssp/<name>.md   # 글로벌 노출 추가
git add -f .claude/commands/ssp/<name>.md                                                  # 선택을 버전 관리 (.gitignore 우회)
rm .claude/commands/ssp/<name>.md                                                          # 글로벌 노출 제거 (원본은 남음)
```

개별 파일 심링크가 커맨드로 인식되는지는 2026-08-02에 실측했다 — 프로브 커맨드를 심링크로 걸고 중립 디렉토리에서 헤드리스로 조회해 인식을 확인했고, 존재하지 않는 토큰으로 음성 대조군을 함께 돌려 판별력을 검증했다.

## 카탈로그는 탐색해서 확인한다

커맨드·에이전트·스킬의 **목록은 이 문서에 두지 않는다** — 복제하면 실제와 어긋나기 때문이다. 필요할 때 직접 조회한다.

```bash
ls ClaudeCode/.claude/{commands/ssp,agents,skills}   # 배포 템플릿 카탈로그
ls .claude/{commands/ssp,agents,skills}              # 이 저장소 로컬 카탈로그
ls -la ~/.claude/{commands,skills}                   # 글로벌 현황 (심링크 여부 포함)
```

각 자산의 목적은 파일 frontmatter의 `description`에 있다. 스킬은 `SKILL.md`, 커맨드·에이전트는 `.md` 본문 상단을 읽는다.

---

## 배포 명령

```bash
# Claude Code 템플릿 → 프로젝트
cp -r ClaudeCode/.claude/* /path/to/project/.claude/

# 글로벌 지침 (최신 버전 파일을 지정)
cp ClaudeCode/CLAUDE.v.5.4.md ~/.claude/CLAUDE.md

# Codex 설정
cp Codex/config.toml ~/.codex/
```

## Git 규칙

- 이 저장소의 remote는 `liberatto/cursor-rules`. push 전 `gh auth switch --user liberatto`, push 후 `gh auth switch --user ss-park_ktdev`로 복원한다.
- 커밋은 기능 개선 / 신규 추가 / 설정 유지보수로 논리 분리한다.
- 커밋 메시지에 변경 사유를 명시한다.

## 주의사항

- **`.gitignore`가 `.claude/*`를 제외한다** — 루트 `.claude/` 하위는 기본적으로 추적되지 않는다. 예외로 `claude-md-audit` 스킬만 negation으로 추적 중이다. 루트 `.claude/`에 파일을 추가하고 커밋이 안 되면 이 때문이다. `ClaudeCode/` 하위는 정상 추적된다.
- **`.mcp.json`은 추적 제외** — `*.mcp.json` 패턴으로 제외되며, 현재 저장소에 커밋된 MCP 설정 파일은 없다. API 키가 평문으로 들어가는 파일이라 공유 시 환경변수 치환이 필요하다.
- **루트 `.claude/`와 `ClaudeCode/.claude/`는 내용이 다르다** — 이름이 같아도 같은 파일이라고 가정하지 말고 양쪽을 확인한다.

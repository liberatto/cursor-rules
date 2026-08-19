# Rules Repository

AI 개발 도구(Claude Code, Codex)의 설정, 커스텀 커맨드, 에이전트, 스킬, MCP 설정의 마스터 템플릿 저장소

## Overview

각 프로젝트에 배포할 AI 도구 설정 파일들의 원본을 중앙 관리한다. Claude Code 생태계와 OpenAI Codex CLI 설정을 포함한다.

> 디렉토리 구조와 커맨드·에이전트·스킬 카탈로그는 저장소를 직접 탐색해 확인한다(`ls`, 각 디렉토리의 frontmatter). 여기에 목록을 복제하면 실제와 어긋나므로 두지 않는다.

> **외부 참조용 진입점은 `README.md`다.** 다른 프로젝트에서 이 저장소를 참조할 때 필요한 것(원본 위치 매핑, 글로벌 배포 현황, 역반영 절차)은 전부 README에 있다. 이 문서는 이 저장소 안에서 작업할 때의 지침이므로, 같은 내용을 여기에 복제하지 않는다.

---

## Key Components

### 프로젝트 부트스트랩 키트 (`bootstrap-kit/`)

신규 프로젝트에서 Claude Code 작업 패턴을 즉시 재현하기 위한 키트 — 기본 3파일에, 자율 루프 모드용 2파일(`BACKLOG.template.json`·`PROMPT.template.md`)이 선택으로 붙는다. `agent_studio` 개발 6주(20회차)에서 실제로 굴러간 패턴을 추출·일반화한 것이다.

핵심 개념은 **기억의 3층 분리**다: `CLAUDE.md`(불변 정본) / `CLAUDE.local.md`(회차 시간축, git 미추적) / auto memory(사용자 개인 선호). 각 층에 무엇을 쓰고 무엇을 쓰지 않을지의 라우팅 규칙과 세션 마감 루프를 `README.md`가 정의한다. README §10(루프 엔지니어링)은 이 위에 HITL 회차 운영을 얹는다 — `BACKLOG.json`(verify 달린 목표 계약)과 `PROMPT.md`(매 회차 동일 주입되는 회차 헌법)로 회차 안은 Claude가 완결 수행하고, 회차마다 사람이 보고를 검토·커밋 승인해 목표 충족(DONE)까지 반복한다. 외부 스킬·플러그인 의존 없이 키트 내 파일과 git만으로 동작한다.

사용법 — 폴더째 새 프로젝트로 복사한 뒤 Claude에게 "이 README 읽고 셋업해줘"라고 지시하면, README §0의 Claude용 셋업 절차(템플릿 복사 → gitignore 등록 → 저장소 탐색 → 노스 스타 질의 → 빈 섹션 삭제 → 스킬 설치 → 루프 모드 확인)가 그대로 실행된다.

---

## Architecture & Design Patterns

### 마스터 템플릿 패턴

이 저장소는 **단일 진실 원천(Single Source of Truth)** 역할을 한다:
1. 모든 설정 원본은 이 저장소에서 관리
2. 각 프로젝트에는 **심링크로 배포** — 사본을 두면 양쪽이 각자 앞서나가 어느 쪽이 정본인지 사라진다
3. 변경은 항상 이 저장소에서 먼저 수행 → 심링크를 통해 자동 전파

### 이중 `.claude/` 구조

- `ClaudeCode/.claude/`: 다른 프로젝트에 배포할 **템플릿** 원본
- `.claude/` (루트): 이 저장소 자체에서 사용하는 **로컬** 설정
- 커맨드 **원본은 `ClaudeCode/.claude/commands/ssp/` 하나뿐이다.** 루트 `.claude/commands/ssp/`는 그중 글로벌로 내보낼 것만 골라 건 **상대 심링크 모음**이고, 이 디렉토리가 통째로 `~/.claude/commands/ssp`로 심링크되어 있다. 따라서 커맨드는 항상 `ClaudeCode/` 쪽 원본을 수정하며, 편집 즉시 글로벌에 반영된다
- **스킬·에이전트도 같은 구조다** — 루트 `.claude/skills/*`·`.claude/agents/ktspace-atlassian-explorer.md`는 전부 `ClaudeCode/` 원본을 가리키는 상대 심링크다. 따라서 원본을 고치면 이 저장소 세션에 즉시 반영되며, `cp`로 동기화할 필요가 없다 (2026-08-14 전환)
- 글로벌 노출을 추가·제거하려면 루트 쪽 심링크만 만들거나 지운다 — `.gitignore`의 `.claude/*` 때문에 `git add -f`로 추적해야 선택 자체가 버전 관리된다

```bash
# 커맨드 글로벌 노출 추가 (파일 단위)
ln -s ../../../ClaudeCode/.claude/commands/ssp/<name>.md .claude/commands/ssp/<name>.md
git add -f .claude/commands/ssp/<name>.md

# 스킬 (디렉토리 단위)
ln -s ../../ClaudeCode/.claude/skills/<name> .claude/skills/<name>
git add -f .claude/skills/<name>
```

### 글로벌 CLAUDE.md 원본

- 글로벌 가이드라인 원본은 `ClaudeCode/CLAUDE.v.*.md` 버전 시리즈로 관리한다 — 최신 버전 파일이 정본이며, 이것을 `~/.claude/CLAUDE.md`로 복사해 배포한다. 정적 `ClaudeCode/CLAUDE.md`는 없다.

---

## Conventions & Style

### 배포 규칙

```bash
# 스킬·에이전트 배포 — 외부 프로젝트는 절대 경로 심링크
ln -s /Users/sspark/Work/rules/ClaudeCode/.claude/skills/<name> /path/to/project/.claude/skills/<name>

# Codex 설정 배포 (심링크 대상 아님)
cp Codex/config.toml ~/.codex/
```

`cp -r`로 배포하지 않는다 — 사본은 프로젝트에서 독자 진화해 원본과 갈라지고, `.claude/*`가 gitignore라 갈라진 사본은 git으로 복구되지 않는다.

### 파일 수정 원칙

1. **이 저장소가 마스터**: 항상 여기서 먼저 수정 후 프로젝트에 배포
2. **배포 전 양방향 대조**: 심링크로 덮기 전에 `diff -rq <원본> <사본>`을 돌린다. **원본이 항상 최신이라는 전제는 틀린다** — 2026-08-14 전환에서 5건(`ktspace`·`report-style`·`svg-slide`·`ktspace-explorer`·`ktspace-atlassian-explorer` 에이전트)이 사본 쪽이 앞서 있었다. 사본에만 있는 내용이 나오면 원본에 역반영한 뒤 배포하고, 구버전 잔재라 버린다면 그 근거를 커밋 메시지에 남긴다
   - 검사 tell: 사본을 지우기 전에 "이 사본에만 있는 문장"을 하나라도 댈 수 있어야 한다. 못 대면 대조를 안 돌린 것이다
3. **커밋 메시지에 변경 사유 명시**
4. **실제 프로젝트에서 동작 확인 후 커밋**

---

## Git Push 규칙

- 이 저장소의 remote(`liberatto/cursor-rules`)에 push 할 때는 반드시 `liberatto` GitHub 계정으로 전환 후 push한다
- 전환: `gh auth switch --user liberatto`
- push 후 원래 계정 복원: `gh auth switch --user ss-park_ktdev`

---

## Caveats & Pitfalls

- **`.gitignore` 주의**: `.claude/*`, `*.mcp.json`이 git 추적에서 제외됨. 단 이 저장소는 솔로라 `CLAUDE.md`·`CLAUDE.local.md`는 **추적한다** — 전역 `~/.config/git/ignore`의 `**/CLAUDE.local.md`를 로컬 `.gitignore`의 `!CLAUDE.local.md` negation으로 이 저장소에서만 무효화했다 (배포 템플릿인 `ClaudeCode/` 하위는 그대로 추적)
- **MCP 설정은 저장소에 없음**: `.gitignore`의 `*.mcp.json`으로 제외되어 현재 커밋된 `.mcp.json`이 없다. 향후 추가하더라도 API 키가 평문으로 들어가므로 환경변수 치환 없이는 추적하지 않는다
- **settings.local.json 중복 항목**: 권한 목록에 중복 엔트리 존재 (예: `Bash(ls:*)`, `Bash(python:*)` 등). 기능상 문제 없으나 정리 가능
- **글로벌 CLAUDE.md vs 루트 CLAUDE.md**: 배포용 글로벌 원본은 `ClaudeCode/CLAUDE.v.*.md` 최신 버전 파일이다(정적 `ClaudeCode/CLAUDE.md`는 없음). 루트 `CLAUDE.md`는 이 저장소 자체 문서

---

## 대화 답변 스타일

> **대화 답변에만** 적용 (문서 산출물은 `doc-writer`·`report-style` 담당).
> 아래 모드는 발동 조건에 걸릴 때만 적용. 발동하지 않으면 평소 응답 규칙을 따름.

### 평이 설명 모드 — "쉽게 설명해" · "회장님 버전으로 설명해"

- **발동 조건** — "쉽게 설명해", "풀어서 설명해", "다시 쉽게", "회장님 버전으로", "임원 보고용으로 쉽게", "explain simply", 또는 이미 답한 내용을 다시 설명해 달라는 모든 요청
- **전역 지침 예외** — 이 모드는 글로벌 `CLAUDE.md`의 `Concise by selection`을 무효화. 평소라면 잘라낼 배경이 곧 요청받은 산출물
- **결론 한 문장을 맨 앞에** — 본론 전에 굵은 한 문장으로 답을 먼저 준다. 그 문장만 읽고 자리를 떠도 손해가 없어야 하고, 배경 복원은 그다음이다
- **전제부터 복원** — 결론을 다시 말하기 전에 이 일이 애초에 무엇을 하는 일인지와 각 수치의 출처·계산 방식을 먼저 세움. 빠진 것은 결론이 아니라 결론에 이르는 연결고리
- **전문용어 치환** — 모든 술어를 일상어로 교체. 원어는 독자가 문서·회의에서 다시 마주칠 때만 괄호 병기
- **수치는 개수로** — "39.22%"가 아니라 "51문제 중 20문제". 비율은 독자가 크기를 다시 상상해야 하고 개수는 바로 잡힌다. 원래 단위가 비율인 것만 비율로 둔다
- **두 번 말하기** — 사실 한 번, 그 사실이 뜻하는 결과 한 번
- **비유는 하나만** — 낯선 구조를 일상 장면 하나로 옮긴다. 둘 이상 쓰면 비유끼리 부딪혀 원래 이야기가 흐려진다
- **양면 제시** — 무엇을 얻고 무엇을 잃는지 각각 한 줄. 특히 **내 결과를 깎는 사실은 묻기 전에 먼저 말한다** — 유리한 해석만 남기면 다음 질문에서 무너진다
- **위험은 반응으로 서술** — 추상적 명칭이 아니라 특정 독자가 보일 반응으로 서술
- **선택지로 닫기** — 사용자가 실제로 내려야 할 결정을 (a)/(b)/(c) 형태로 제시하고 **그중 하나를 근거와 함께 권한다.** 열린 질문으로 끝내지 않음
- **대조·순위는 ASCII 블록** — 같은 대상의 두 판본은 좌우 대조로, 여러 방식의 성적은 한 축으로 세운 순위표로. 코드펜스 안, 폭 60자 이하(터미널 줄바꿈 방지)
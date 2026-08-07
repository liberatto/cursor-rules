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
2. 각 프로젝트에는 `cp -r`로 배포
3. 변경은 항상 이 저장소에서 먼저 수행 → 프로젝트에 전파

### 이중 `.claude/` 구조

- `ClaudeCode/.claude/`: 다른 프로젝트에 배포할 **템플릿** 원본
- `.claude/` (루트): 이 저장소 자체에서 사용하는 **로컬** 설정
- 커맨드 **원본은 `ClaudeCode/.claude/commands/ssp/` 하나뿐이다.** 루트 `.claude/commands/ssp/`는 그중 글로벌로 내보낼 것만 골라 건 **상대 심링크 모음**이고, 이 디렉토리가 통째로 `~/.claude/commands/ssp`로 심링크되어 있다. 따라서 커맨드는 항상 `ClaudeCode/` 쪽 원본을 수정하며, 편집 즉시 글로벌에 반영된다
- 글로벌 노출을 추가·제거하려면 루트 쪽 심링크만 만들거나 지운다 — `.gitignore`의 `.claude/*` 때문에 `git add -f`로 추적해야 선택 자체가 버전 관리된다

```bash
# 글로벌 노출 추가
ln -s ../../../ClaudeCode/.claude/commands/ssp/<name>.md .claude/commands/ssp/<name>.md
git add -f .claude/commands/ssp/<name>.md
```

### 글로벌 CLAUDE.md 원본

- 글로벌 가이드라인 원본은 `ClaudeCode/CLAUDE.v.*.md` 버전 시리즈로 관리한다 — 최신 버전 파일이 정본이며, 이것을 `~/.claude/CLAUDE.md`로 복사해 배포한다. 정적 `ClaudeCode/CLAUDE.md`는 없다.

---

## Conventions & Style

### 배포 규칙

```bash
# Claude Code 설정 배포
cp -r ClaudeCode/.claude/* /path/to/project/.claude/

# Codex 설정 배포
cp Codex/config.toml ~/.codex/
```

### 파일 수정 원칙

1. **이 저장소가 마스터**: 항상 여기서 먼저 수정 후 프로젝트에 배포
2. **커밋 메시지에 변경 사유 명시**
3. **실제 프로젝트에서 동작 확인 후 커밋**

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

# Rules Repository

AI 개발 도구(Claude Code, Codex)의 설정, 커스텀 커맨드, 에이전트, 스킬, MCP 설정의 마스터 템플릿 저장소

## Overview

각 프로젝트에 배포할 AI 도구 설정 파일들의 원본을 중앙 관리한다. Claude Code 생태계(에이전트 13종, 슬래시 커맨드 18종, 스킬 22종)와 OpenAI Codex CLI 설정을 포함한다.

---

## Directory Structure

```
rules/
├── ClaudeCode/                  # Claude Code 배포용 템플릿
│   ├── .claude/
│   │   ├── agents/              # Task 서브에이전트 정의 (13종)
│   │   ├── commands/ssp/        # /ssp:* 슬래시 커맨드 (18종)
│   │   ├── skills/              # 스킬 패키지 (21종)
│   │   └── settings.local.json  # 권한 허용 목록 템플릿
│   ├── plugin/                  # 플러그인 가이드 문서
│   │   ├── Sisyphus.md          # 멀티에이전트 오케스트레이션
│   │   └── CdoexReview.md       # Codex CLI 코드 리뷰
│   └── CLAUDE.md                # 글로벌 CLAUDE.md 원본 (버전별: CLAUDE.v.*.md)
│
├── Codex/                       # OpenAI Codex CLI 설정
│   └── config.toml              # MCP 서버 설정 (Tavily, Context7, Serena)
│
├── bootstrap-kit/               # 신규 프로젝트 부트스트랩 키트 (기본 3파일 + 자율 루프 2파일)
│   ├── CLAUDE.template.md       # → <새프로젝트>/CLAUDE.md (정본: 목표·구조·원칙·함정)
│   ├── CLAUDE.local.template.md # → <새프로젝트>/CLAUDE.local.md (시간축: 회차 기록·다음 후보)
│   ├── BACKLOG.template.json    # → <새프로젝트>/BACKLOG.json (자율 루프 목표 계약 — 선택)
│   ├── PROMPT.template.md       # → <새프로젝트>/PROMPT.md (자율 루프 회차 헌법 — 선택)
│   └── README.md                # 규칙서 (기억 3층 라우팅, 세션 마감 루프, §10 루프 엔지니어링) + Claude용 셋업 지시
│
├── .claude/                     # 이 저장소 자체의 로컬 Claude 설정
│   ├── commands/ssp/            # 로컬 슬래시 커맨드 (18종, 배포본과 동기)
│   ├── skills/skill-seekers/    # skill-seekers 스킬
│   ├── settings.json            # 플러그인 설정
│   └── settings.local.json      # 로컬 권한 및 MCP 설정
│
├── docs/                        # 레퍼런스 문서
│   ├── RESEARCH-CLAUDE-CODE-SETTINGS-REFERENCE-*.md  # settings.json 설정 레퍼런스
│   ├── GUIDE-CLAUDE-MD-BEST-PRACTICES-*.md           # CLAUDE.md 작성 가이드
│   └── GUIDE-CLAUDE-CODE-HOOKS-*.md                  # Hooks 가이드 (이벤트 17종, 생성법, Use Case)
│
├── CLAUDE.md                    # 이 파일
├── README.md                    # 저장소 소개 (Serena 활성화용)
├── .gitignore                   # chats.db, .claude/*, *.mcp.json 등 제외 (CLAUDE.md·CLAUDE.local.md는 추적)
└── chats.db                     # 대화 기록 DB (git 추적 제외)
```

---

## Key Components

### Claude Code 커맨드 (`/ssp:*`) — 18종

| 카테고리 | 커맨드 | 용도 |
|----------|--------|------|
| **작업 관리** | `work-plan` | 구현 계획 문서 생성 |
| | `work-do` | PLAN 파일 기반 단계별 실행 |
| | `work-task` | 작업 정의 및 명확화 워크플로우 |
| | `work-dive` | 코드베이스 딥다이브 탐색 |
| | `work-test` | 체계적 테스트 실행 |
| | `work-ralph-init` | 작업 설명 → ralph-loop용 PROMPT.md 생성 |
| | `work-ralph` | Ralph Loop 실행 (기본값: 최대 10회 반복) |
| | `goal-init` | 컨텍스트 수집 → 메가 프롬프트 조립 → /goal 위임 |
| **Git** | `git-commit` | 로컬 커밋 생성 (push 안함) |
| | `git-merge` | 브랜치 통합 (단일 커밋) |
| | `git-revert` | 커밋 안전 되돌리기 |
| | `git-log` | 커밋 히스토리 조회 (상위 5개) |
| **문서** | `claude.md-dive` | 디렉토리 분석 → CLAUDE.md 생성 |
| | `claude.md-local` | CLAUDE.local.md 세션 컨텍스트 매니저 생성 |
| | `claude.md-review` | CLAUDE.md 코드베이스 대비 검증 |
| | `claude.md-update` | 세션 지식으로 CLAUDE.md 업데이트 |
| **메모리** | `memory-update` | 세션 학습 내용을 auto memory에 정리 |
| **품질** | `metacog` | 작업 산출물의 메타인지 자기 검토·교정 |

### Claude Code 에이전트 — 13종

| 분류 | 에이전트 | 역할 |
|------|----------|------|
| **설계** | `api-planner` | API 설계 및 문서화 |
| | `system-architect` | 시스템 아키텍처 설계 |
| **코드** | `code-writer` | 코드 작성 |
| | `python-pro` | Python 전문가 |
| | `debugger` | 디버깅 |
| **품질** | `code-quality-inspector` | 코드 품질 검사 |
| | `test-automator` | 테스트 자동화 |
| **분석** | `codebase-analyzer` | 코드베이스 분석 |
| | `data-analyst` | 데이터 분석 |
| | `researcher` | 리서치 |
| **ML** | `ml-engineer` | ML 워크플로우 |
| **기타** | `report-generator` | 보고서 생성 |
| | `codex-agent` | Codex CLI 연동 |

### Claude Code 스킬 — 22종

| 분류 | 스킬 |
|------|------|
| **도구** | `skill-creator`, `skill-seekers`, `codex`, `hook-manager` |
| **데이터 분석** | `polars`, `dask`, `exploratory-data-analysis` |
| **시각화** | `matplotlib`, `seaborn`, `plotly`, `scientific-visualization` |
| **ML/DL** | `scikit-learn`, `pytorch-lightning`, `transformers`, `torch_geometric`, `stable-baselines3` |
| **통계** | `statsmodels`, `statistical-analysis`, `pymc`, `shap` |
| **기타** | `networkx`, `umap-learn` |

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
- 두 폴더의 `commands/ssp/`는 동일한 커맨드셋을 유지

### 글로벌 CLAUDE.md 원본

- `ClaudeCode/CLAUDE.md`: `~/.claude/CLAUDE.md`에 복사할 글로벌 가이드라인 원본

---

## Conventions & Style

### 배포 규칙

```bash
# Claude Code 설정 배포
cp -r ClaudeCode/.claude/* /path/to/project/.claude/
cp ClaudeCode/mcp/.mcp.json /path/to/project/

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
- **API 키 노출**: `.mcp.json`에 API 키가 직접 포함됨. 공유 시 환경변수 대체 필요
- **settings.local.json 중복 항목**: 권한 목록에 중복 엔트리 존재 (예: `Bash(ls:*)`, `Bash(python:*)` 등). 기능상 문제 없으나 정리 가능
- **글로벌 CLAUDE.md vs 루트 CLAUDE.md**: `ClaudeCode/CLAUDE.md`는 배포용 글로벌 원본, 루트 `CLAUDE.md`는 이 저장소 자체 문서


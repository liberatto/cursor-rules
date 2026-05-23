---
type: "GUIDE"
audience: "team"
related_docs:
  - docs/GUIDE-CLAUDE-MD-BEST-PRACTICES-2026-02-20-1300.md
  - docs/RESEARCH-CLAUDE-CODE-SETTINGS-REFERENCE-2026-02-20-1200.md
  - docs/GUIDE-CLAUDE-CODE-HOOKS-2026-02-22-1500.md
source: "https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder"
created: "2026-05-11 20:00"
---

# Anatomy of the .claude/ Folder

> 원문: [Daily Dose of Data Science — Anatomy of the .claude/ Folder](https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder)

---

## Introduction

Claude Code 사용자들이 간과하기 쉬운 `.claude` 폴더의 모든 구성 요소를 설명하는 종합 가이드. 필수 설정 파일부터 고급 기능까지 다루며, 팀의 Claude Code 워크플로우를 최적화하는 방법을 안내한다.

---

## Two Folders, Not One

두 개의 별도 `.claude` 디렉토리가 존재한다:

1. **Project-level** (`your-project/.claude/`) — 팀 설정, git에 커밋
2. **Global** (`~/.claude/`) — 개인 환경설정 및 머신-로컬 상태

프로젝트 레벨 폴더는 팀원 간 일관된 동작을 보장하고, 글로벌 폴더는 개인 환경설정과 세션 히스토리를 유지한다.

---

## CLAUDE.md: Core Instructions

> "The first thing Claude Code reads when you start a session is `CLAUDE.md`. It loads it straight into the system prompt and keeps it in mind for the entire conversation."

### 포함할 것

- ✓ Build, test, lint 커맨드
- ✓ 아키텍처 결정
- ✓ 비자명한(non-obvious) 주의사항
- ✓ Import 컨벤션 및 네이밍 패턴
- ✓ 파일 구조 개요

### 포함하지 말 것

- ✗ Linter/formatter 설정
- ✗ 전체 문서 링크
- ✗ 긴 이론적 설명

### 권장 길이

200줄 이하. 길어지면 과도한 컨텍스트를 소비하고 지시 준수율이 떨어진다.

### 예시 구조

```markdown
# Project: Acme API

## Commands
npm run dev          # Start dev server
npm run test         # Run tests (Jest)
npm run lint         # ESLint + Prettier check
npm run build        # Production build

## Architecture
- Express REST API, Node 20
- PostgreSQL via Prisma ORM
- All handlers live in src/handlers/
- Shared types in src/types/

## Conventions
- Use zod for request validation in every handler
- Return shape is always { data, error }
- Never expose stack traces to the client
- Use the logger module, not console.log

## Watch out for
- Tests use a real local DB, not mocks. Run `npm run db:test:reset` first
- Strict TypeScript: no unused imports, ever
```

---

## CLAUDE.local.md: Personal Overrides

팀 설정에 영향을 주지 않으면서 프로젝트별 개인 환경설정을 생성한다. 이 파일은 자동으로 gitignore되며, 공유 표준을 유지하면서 개인 커스터마이징을 허용한다.

---

## rules/ Folder: Modular Instructions

대규모 팀에서는 하나의 거대한 `CLAUDE.md` 대신 여러 파일로 지시를 분할한다.

### 구조 예시

```
.claude/rules/
├── code-style.md
├── testing.md
├── api-conventions.md
└── security.md
```

### Path-Scoped Rules

YAML frontmatter를 사용하여 조건부로 규칙을 적용한다:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/handlers/**/*.ts"
---
# API Design Rules

- All handlers return { data, error } shape
- Use zod for request body validation
- Never expose internal error details to clients
```

경로 제한 없는 규칙은 모든 세션에서 로드된다. 이 방식은 모놀리식 지시 파일보다 확장성이 좋고, 팀원 간 소유권을 분산시킨다.

---

## commands/ Folder: Custom Slash Commands

`.claude/commands/`의 모든 마크다운 파일이 실행 가능한 커맨드가 된다. `review.md`라는 파일은 `/project:review`를 생성한다.

### 기본 예시

```markdown
---
description: Review the current branch diff for issues before merging
---
## Changes to Review

!`git diff --name-only main...HEAD`

## Detailed Diff

!`git diff main...HEAD`

Review the above changes for:
1. Code quality issues
2. Security vulnerabilities
3. Missing test coverage
4. Performance concerns

Give specific, actionable feedback per file.
```

`!` 구문은 셸 커맨드를 실행하고 출력을 프롬프트에 직접 임베딩한다.

### 인자를 받는 커맨드

```markdown
---
description: Investigate and fix a GitHub issue
argument-hint: [issue-number]
---
Look at issue #$ARGUMENTS in this repo.

!`gh issue view $ARGUMENTS`

Understand the bug, trace it to the root cause, fix it, and write a
test that would have caught it.
```

`/project:fix-issue 234` 실행 시 이슈 번호가 프롬프트에 전달된다.

### 커맨드 범위

- **Project commands** (`.claude/commands/`) — 팀 공유, `/project:command-name`
- **Personal commands** (`~/.claude/commands/`) — 모든 프로젝트에서 사용, `/user:command-name`

---

## skills/ Folder: Auto-Invoked Workflows

스킬은 커맨드와 근본적으로 다르다: Claude가 매칭되는 컨텍스트를 감지하면 사용자의 명시적 호출 없이 자동으로 활성화된다.

### 디렉토리 구조

```
.claude/skills/
├── security-review/
│   ├── SKILL.md
│   └── DETAILED_GUIDE.md
└── deploy/
    ├── SKILL.md
    └── templates/
        └── release-notes.md
```

### 스킬 설정

```markdown
---
name: security-review
description: Comprehensive security audit. Use when reviewing code for
  vulnerabilities, before deployments, or when the user mentions security.
allowed-tools: Read, Grep, Glob
---
Analyze the codebase for security vulnerabilities:

1. SQL injection and XSS risks
2. Exposed credentials or secrets
3. Insecure configurations
4. Authentication and authorization gaps

Report findings with severity ratings and specific remediation steps.
Reference @DETAILED_GUIDE.md for our security standards.
```

"review this PR for security"라고 언급하면 Claude가 매치를 인식하고 자동으로 스킬을 호출한다. 스킬은 단일 파일 커맨드와 달리 `SKILL.md` 옆에 보조 파일을 지원한다.

`~/.claude/skills/`의 개인 스킬은 모든 프로젝트에서 사용 가능하다.

---

## agents/ Folder: Specialized Subagents

복잡한 작업은 전용 전문가 페르소나의 도움을 받는다. 각 에이전트는 고유한 격리된 컨텍스트에서 특정 도구 접근 및 모델 환경설정으로 동작한다.

### 에이전트 예시

```markdown
---
name: code-reviewer
description: Expert code reviewer. Use PROACTIVELY when reviewing PRs,
  checking for bugs, or validating implementations before merging.
model: sonnet
tools: Read, Grep, Glob
---
You are a senior code reviewer with a focus on correctness and maintainability.

When reviewing code:
- Flag bugs, not just style issues
- Suggest specific fixes, not vague improvements
- Check for edge cases and error handling gaps
- Note performance concerns only when they matter at scale
```

`tools` 필드는 에이전트의 역량을 제한한다. 보안 감사자는 Read, Grep, Glob이 필요하지만 파일을 쓸 필요는 없다. `model` 필드는 비용 최적화를 가능하게 한다 — Haiku는 읽기 전용 탐색에 적합하고, Sonnet과 Opus는 복잡한 작업에 사용한다.

`~/.claude/agents/`의 개인 에이전트는 모든 프로젝트에서 사용 가능하다.

---

## settings.json: Permissions and Config

Claude가 할 수 있는 것과 할 수 없는 것을 제어한다. 도구 접근, 파일 권한, 확인 요구사항을 정의한다.

### 전체 설정

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Read",
      "Write",
      "Edit"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  }
}
```

### Allow List

확인 없이 실행되는 커맨드:

- `Bash(npm run *)` 또는 `Bash(make *)` — 스크립트 실행
- `Bash(git *)` — 읽기 전용 git 작업
- `Read, Write, Edit, Glob, Grep` — 파일 작업

### Deny List

완전히 차단되는 커맨드:

- `rm -rf` 같은 파괴적 작업
- `curl` 같은 네트워크 접근
- `.env` 같은 민감한 파일

### Personal Overrides

팀 설정에 영향을 주지 않으면서 개인 권한 변경을 위해 `.claude/settings.local.json`을 생성한다. 이 파일은 자동으로 gitignore된다.

---

## Global ~/.claude/ Folder

### 구성 요소

- **CLAUDE.md** — 모든 프로젝트에 적용되는 개인 지시
- **projects/** — 프로젝트별 세션 트랜스크립트 및 auto-memory
- **commands/** — 모든 프로젝트에서 사용하는 개인 커맨드
- **skills/** — 모든 프로젝트에서 사용하는 개인 스킬
- **agents/** — 모든 프로젝트에서 사용하는 개인 에이전트

Claude는 `/memory`를 통해 관찰 및 학습 내용을 자동으로 메모리에 저장한다. 수동 개입 없이 세션 간 유지된다.

---

## Complete File Structure

```
your-project/
├── CLAUDE.md                  # 팀 지시 (커밋)
├── CLAUDE.local.md            # 개인 오버라이드 (gitignore)
│
└── .claude/
    ├── settings.json          # 권한 + 설정 (커밋)
    ├── settings.local.json    # 개인 오버라이드 (gitignore)
    │
    ├── commands/              # 커스텀 슬래시 커맨드
    │   ├── review.md          # → /project:review
    │   ├── fix-issue.md       # → /project:fix-issue
    │   └── deploy.md          # → /project:deploy
    │
    ├── rules/                 # 모듈러 지시 파일
    │   ├── code-style.md
    │   ├── testing.md
    │   └── api-conventions.md
    │
    ├── skills/                # 자동 호출 워크플로우
    │   ├── security-review/
    │   │   └── SKILL.md
    │   └── deploy/
    │       └── SKILL.md
    │
    └── agents/                # 전문 서브에이전트 페르소나
        ├── code-reviewer.md
        └── security-auditor.md

~/.claude/
├── CLAUDE.md                  # 글로벌 지시
├── settings.json              # 글로벌 설정
├── commands/                  # 개인 커맨드 (모든 프로젝트)
├── skills/                    # 개인 스킬 (모든 프로젝트)
├── agents/                    # 개인 에이전트 (모든 프로젝트)
└── projects/                  # 세션 히스토리 + auto-memory
```

---

## Practical Setup Guide

### Step 1: Core Configuration 초기화

Claude Code에서 `/init`을 실행하여 프로젝트 기반 `CLAUDE.md` 초안을 생성한다. 핵심 내용만 남기고 편집한다.

### Step 2: 권한 정의

스택에 맞는 allow/deny 규칙으로 `.claude/settings.json`을 추가한다. 최소한: run 커맨드 allow, .env 접근 deny.

### Step 3: 초기 커맨드 생성

빈번한 워크플로우(코드 리뷰, 이슈 수정)용 커맨드를 1~2개 만든다.

### Step 4: Rules로 확장

`CLAUDE.md`가 200줄을 넘기면 `.claude/rules/` 파일로 분할한다. 적절한 곳에 path scoping을 사용한다.

### Step 5: 개인 환경설정 추가

모든 프로젝트에 적용할 개인 코딩 원칙과 패턴을 `~/.claude/CLAUDE.md`에 작성한다.

이 기반은 일반적인 프로젝트의 95%를 커버한다. 반복적인 복잡 워크플로우 관리가 필요할 때 스킬과 에이전트를 추가한다.

---

## Key Insight

> "The `.claude` folder is really a protocol for telling Claude who you are, what your project does, and what rules it should follow. The more clearly you define that, the less time you spend correcting Claude and the more time it spends doing useful work."

가장 높은 레버리지 행동은 `CLAUDE.md`를 완벽하게 만드는 것이다. 나머지는 모두 그 기반 위에서 최적화하는 것이다.

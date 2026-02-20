# CLAUDE.md 작성 가이드 — Best Practices

> 작성일: 2026-02-20
> 대상: Claude Code 사용자 (초급~중급)

---

## 1. 개요 — CLAUDE.md란 무엇인가

CLAUDE.md는 Claude Code가 **매 세션마다 자동 로드**하는 마크다운 파일이다. Claude Code에는 세션 간 기억이 없으므로, 이 파일이 프로젝트의 **유일한 영속적 컨텍스트 전달 수단**이 된다.

**핵심 역할:**

- 프로젝트 구조와 아키텍처 전달
- 코딩 규칙과 워크플로우 명시
- 빌드/테스트 명령어와 개발 환경 정보 제공
- 함정(gotcha)과 비직관적 동작 경고

> 잘 작성된 CLAUDE.md는 Claude의 작업 품질을 크게 높이지만, **비대한 CLAUDE.md는 오히려 지시를 무시하게 만든다.** 프론티어 모델이 신뢰성 있게 따르는 지시는 약 150~200개이며, 지시 수가 늘수록 **모든** 지시의 수행 품질이 균일하게 저하된다.

---

## 2. 파일 체계 — 종류와 계층 구조

### 메모리 계층 표

| 레벨 | 위치 | 용도 | Git 추적 | 공유 범위 |
|------|------|------|----------|-----------|
| 조직 정책 | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | 회사 표준, 보안 정책 | MDM 관리 | 조직 전체 |
| 사용자 글로벌 | `~/.claude/CLAUDE.md` | 개인 선호, 코드 스타일 | X | 본인 전체 |
| 사용자 규칙 | `~/.claude/rules/*.md` | 개인 규칙 (모듈별) | X | 본인 전체 |
| 프로젝트 공유 | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | 프로젝트 아키텍처, 표준 | O | 팀 전체 |
| 프로젝트 규칙 | `./.claude/rules/*.md` | 모듈별 규칙 (조건부 로딩 가능) | O | 팀 전체 |
| 프로젝트 개인 | `./CLAUDE.local.md` | 개인 프로젝트 설정, 세션 컨텍스트 | X (.gitignore) | 본인만 |
| Auto Memory | `~/.claude/projects/<project>/memory/` | Claude 자동 학습 메모 | X | 본인만 |

### 로딩 메커니즘

```
상위 탐색 (시작 시 전부 로딩)          하위 탐색 (온디맨드 로딩)
─────────────────────────          ─────────────────────────
/                                  cwd/
├── CLAUDE.md ← 로딩               ├── src/
├── foo/                           │   └── CLAUDE.md ← src/ 파일 작업 시 로딩
│   ├── CLAUDE.md ← 로딩            └── tests/
│   └── bar/ (cwd)                     └── CLAUDE.md ← tests/ 파일 작업 시 로딩
│       └── CLAUDE.md ← 로딩
```

**우선순위 규칙:** 더 구체적인(specific) 지시가 더 넓은(broader) 지시보다 우선한다. 최근 대화의 지시는 CLAUDE.md보다 우선한다 — 이는 의도된 설계이다.

---

## 3. 작성 원칙 — 효과적인 CLAUDE.md를 위한 5가지 원칙

### 원칙 1: 간결성 우선

| 상태 | 줄 수 | 설명 |
|------|-------|------|
| 이상적 | 50~100줄 | 핵심만 담은 최적 크기 |
| 양호 | 100~200줄 | 대부분 프로젝트에 적합 |
| 경계 | 200~300줄 | 분리 검토 필요 |
| 위험 | 300줄 이상 | 지시 무시 현상 발생 가능 |

> 각 줄에 대해 물어보라: **"이걸 제거하면 Claude가 실수할까?"** 아니라면 삭제하라.

### 원칙 2: 구체성

```markdown
# 나쁜 예
- Format code properly
- Write clean code
- Handle errors appropriately

# 좋은 예
- Use 2-space indentation for TypeScript files
- Use ES modules (import/export), not CommonJS (require)
- All API endpoints must return { data, error, status } shape
```

모호한 지시는 컨텍스트만 차지하고 동작을 바꾸지 않는다. Claude가 이미 올바르게 수행하는 것은 적을 필요 없다.

### 원칙 3: 참조 > 복사

```markdown
# 나쁜 예 — 코드 스니펫을 CLAUDE.md에 직접 포함 (30줄의 구현 코드)

# 좋은 예 — 파일 참조
- 인증 미들웨어 구현: `src/middleware/auth.ts:15-45`
- 위젯 구현 패턴: `src/widgets/HotDogWidget.php`
```

코드 스니펫은 빠르게 outdated되고 컨텍스트를 불필요하게 소비한다. `file:line` 참조를 사용하면 Claude가 최신 코드를 직접 읽는다.

### 원칙 4: WHY 중심

```markdown
# 나쁜 예 — WHAT만 기술
- Use Redis for caching

# 좋은 예 — WHY를 포함
- Use Redis for caching (PostgreSQL 쿼리 응답시간 P99 > 500ms 문제 해결용)
- Q2에 REST → GraphQL 마이그레이션 예정 — 새 엔드포인트는 GraphQL 우선 설계
```

아키텍처 결정의 **이유**가 없으면 Claude는 다른 방식을 제안할 수 있다.

### 원칙 5: 정기 검토

- **주기**: 1~2주마다, 또는 아키텍처 변경이 포함된 코드 리뷰 시
- **방법**: `CLAUDE.md`를 **코드처럼** 취급 — 문제 발생 시 리뷰, 정기적 정리
- **신호**: Claude가 CLAUDE.md에 답이 있는 질문을 하면 → 표현이 모호한 것. Claude가 규칙을 반복 위반하면 → 파일이 너무 길어 규칙이 묻힌 것.

---

## 4. 포함할 것 vs 제외할 것

| 포함 | 제외 |
|------|------|
| Claude가 추측할 수 없는 빌드/테스트 명령어 | 린터/포매터가 처리하는 코드 스타일 |
| 기본값과 다른 코딩 규칙 | 표준 언어 컨벤션 (Claude가 이미 앎) |
| 테스트 실행 방식과 선호 러너 | 프레임워크 공식 문서 전문 |
| 아키텍처 결정과 그 이유 | API 키, 시크릿 |
| 비직관적 동작, gotcha | 자주 변경되는 정보 |
| Git 워크플로우 (브랜치 네이밍, PR 규칙) | 파일별 코드베이스 설명 |
| 개발 환경 quirks (필수 환경변수) | 장문 튜토리얼이나 온보딩 가이드 |

**핵심 기준:** 모든 세션에 **보편적으로** 적용 가능한 것만 포함한다. 특정 작업에만 해당하는 내용은 제외한다.

---

## 5. 권장 섹션 구조 — 템플릿

### 프로젝트 루트 CLAUDE.md

```markdown
# {프로젝트명}
{프로젝트 목적 한 줄 설명}

## Overview
- 기술 스택: {언어}, {프레임워크}, {DB}
- 아키텍처: {모놀리스/마이크로서비스/모노레포}

## Directory Structure
- `src/api/` — API 엔드포인트
- `src/services/` — 비즈니스 로직
- `tests/` — 테스트

## Build & Run
- 개발: `npm run dev` | 테스트: `npm test` | 린트: `npm run lint`

## Architecture & Decisions
- {결정 사항} — {이유}

## Conventions
- {기본값과 다른 규칙만}

## Caveats & Pitfalls
- {비직관적 동작, gotcha}
```

### 서브디렉토리 CLAUDE.md — 해당 모듈 한정 규칙과 주의사항만 기술

### 글로벌 `~/.claude/CLAUDE.md` — 모든 프로젝트에 적용할 개인 선호(응답 언어, 코드 스타일, 워크플로우)

### CLAUDE.local.md — Session 모드

```markdown
# {프로젝트명} — {세션 목표}
> Last updated: {YYYY-MM-DD}

## Session Goal
- **Goal**: {목표} | **Scope**: {관련 디렉토리}

## Progress
- Completed: {완료 항목 (간략)}
- In Progress: {현재 작업 (상세)}
- Next: {다음 행동}

## Decisions / Lessons Learned
- {결정 or 실패한 접근} — {이유}
```

### CLAUDE.local.md — Rolling 모드

장기 운영 프로젝트용. 목표 완료 후 리셋하지 않고 Recent Changes, Backlog, Known Issues, Design Decisions를 rolling 관리한다.

---

## 6. 크기 관리 — 대규모 프로젝트 전략

200줄 초과 시 아래 전략으로 분리한다. (크기별 상태는 §3 원칙 1 참고)

### 전략 1: `.claude/rules/` 디렉토리

CLAUDE.md가 커질 때, 주제별로 규칙 파일을 분리한다. rules 디렉토리의 모든 `.md` 파일은 자동으로 로딩된다.

```
.claude/rules/
├── code-style.md       # 코딩 스타일 규칙
├── testing.md          # 테스트 규칙
├── security.md         # 보안 규칙
└── api/
    └── conventions.md  # API 설계 규약
```

### 전략 2: `paths` frontmatter로 조건부 로딩

`.claude/rules/` 내 파일에 `paths` frontmatter를 추가하면 특정 파일 편집 시에만 로딩된다.

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/middleware/**/*.ts"
---
```

Glob 패턴 지원: `**/*.ts`, `src/**/*`, `*.{ts,tsx}`, `{src,lib}/**/*.ts`

### 전략 3: `@import` 문법

CLAUDE.md에서 `@path/to/file` 문법으로 외부 파일을 참조한다 (최대 5홉 재귀). 상대 경로는 **파일 기준**으로 해석. 코드 블록 안의 `@`는 import로 평가되지 않는다. 과도한 import는 컨텍스트를 부풀리므로 주의.

---

## 7. 안티패턴 — 피해야 할 실수들

### Kitchen Sink (과다 작성)

**증상:** 300줄 이상의 CLAUDE.md, 모든 것을 담으려는 시도
**결과:** 중요한 규칙이 노이즈에 묻혀 Claude가 핵심 지시를 무시
**해결:** 무자비하게 정리. Claude가 이미 올바르게 하는 것은 삭제하거나 hook으로 전환

### 코드 스니펫 복사-붙여넣기

**증상:** 구현 코드를 CLAUDE.md에 직접 포함
**결과:** 코드가 변경되면 CLAUDE.md와 불일치 → Claude가 outdated 패턴을 **자신 있게** 적용
**해결:** `file:line` 참조 사용. Claude가 최신 코드를 직접 읽게 함

### `/init` 자동 생성 후 무비판적 사용

**증상:** `/init`이 생성한 CLAUDE.md를 그대로 사용
**결과:** task-specific 내용, 과도한 정보, 아키텍처 컨텍스트 누락
**해결:** `/init`은 스타터로만 활용하고, 반드시 수동으로 정제. 또는 처음부터 수동 작성

> CLAUDE.md는 프로젝트의 **가장 높은 레버리지 포인트** 중 하나다. 자동화로 대체하기엔 너무 중요하다.

### 린팅 규칙 수동 명시

**증상:** 들여쓰기, 따옴표, 줄바꿈 규칙을 CLAUDE.md에 작성
**결과:** 지시 예산 낭비, 린터가 더 정확하게 처리 가능
**해결:** ESLint/Prettier 설정 후, Claude Code `PostToolUse` hook으로 `Edit|Write` 시 자동 실행

### Outdated 정보 방치

**증상:** 리팩토링 후 CLAUDE.md 미갱신
**결과:** Claude가 존재하지 않는 파일/패턴을 자신 있게 참조 → 버그 생성
**해결:** 아키텍처 변경 시 CLAUDE.md 동시 업데이트. 정기 검토 스케줄 운영

### 대용량 문서 `@` 참조

**증상:** API 문서 전체, README 전문을 `@`로 import
**결과:** 컨텍스트 윈도우 과점 → 다른 지시 품질 저하
**해결:** 핵심 요약만 포함하고, 상세 문서는 URL이나 경로만 언급

---

## 8. 실전 워크플로우

### 초기 생성 → 수동 정제

1. `/init` 실행 → 기본 CLAUDE.md 생성 (또는 빈 파일에서 시작)
2. 표준 규칙, 린터가 처리할 스타일, 코드 스니펫 삭제
3. 프로젝트 고유 정보 추가 (비표준 명령어, 아키텍처 결정, gotcha)
4. 50~100줄로 압축

### 정기 검토 체크리스트

- 참조된 파일/디렉토리가 존재하는가? 빌드/테스트 명령어가 유효한가?
- 기술한 패턴이 실제 코드와 일치하는가? 새로 추가된 중요 패턴이 누락되지 않았는가?
- 줄 수가 200줄을 초과하는가? → §6의 분리 전략 적용

### 이 저장소 커맨드 활용

`/ssp:claude.md-*` 커맨드 4종으로 CLAUDE.md 관리를 체계화할 수 있다.

| 커맨드 | 용도 | 사용 시점 |
|--------|------|-----------|
| `/ssp:claude.md-dive` | 디렉토리 분석 → CLAUDE.md 자동 생성 | 새 프로젝트/모듈 초기 문서화 |
| `/ssp:claude.md-review` | 기존 CLAUDE.md를 코드베이스 대비 검증 | 정기 검토, 리팩토링 후 |
| `/ssp:claude.md-update` | 세션 지식으로 CLAUDE.md/CLAUDE.local.md 업데이트 | 세션 종료 전, 중요 결정 후 |
| `/ssp:claude.md-local` | CLAUDE.local.md 세션 컨텍스트 매니저 생성 | 새 작업 시작 시 |

**권장 워크플로우:** 새 프로젝트 → `claude.md-dive` → 수동 정제 → `claude.md-local` → 작업 중 `claude.md-update` → 정기 `claude.md-review`

### 강조 문법으로 준수율 향상

Claude가 특정 규칙을 반복 위반하면 `IMPORTANT:`, `NEVER`, `YOU MUST` 같은 강조 표현으로 준수율을 높일 수 있다.

---

## 9. 참고 자료

### 공식 문서

- [Claude Code Memory 문서](https://code.claude.com/docs/en/memory) — 파일 체계, 로딩 메커니즘, Auto Memory 상세
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) — 컨텍스트 관리, 프롬프트 전략, 세션 관리

### 커뮤니티 가이드

- [HumanLayer — Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — 지시 한계(150~200개), Progressive Disclosure 패턴
- [Builder.io — CLAUDE.md Guide](https://www.builder.io/blog/claude-md-guide) — `@import` 시스템, `.claude/rules/` 상세
- [Tembo — How to Write a Great CLAUDE.md](https://www.tembo.io/blog/how-to-write-a-great-claude-md) — 컨텍스트 우선순위, outdated 정보 위험

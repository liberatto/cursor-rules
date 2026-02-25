# `/init` 프롬프트 분석 — Claude Code의 CLAUDE.md 자동 생성 내부 지침

> 작성일: 2026-02-24
> 방법: 실제 `/init` 실행으로 프롬프트 확인 + 구버전 리버스 엔지니어링 자료 비교

---

## 1. 개요

Claude Code의 `/init` 명령어는 프로젝트 코드베이스를 분석하여 `CLAUDE.md`를 자동 생성하는 **내장 커맨드**다. CLI에서 `claude --init` 또는 대화형 세션에서 `/init`으로 실행한다.

이 문서는 **실제 `/init` 실행으로 확인된 현재 프롬프트**(2026-02-24 기준)를 해설하고, 2025년 초 리버스 엔지니어링 구버전과 비교한다.

---

## 2. 현재 프롬프트 원문 (2026-02-24 확인)

```text
Please analyze this codebase and create a CLAUDE.md file, which will be given to future instances of Claude Code to operate in this repository.

What to add:
1. Commands that will be commonly used, such as how to build, lint, and run tests.
   Include the necessary commands to develop in this codebase, such as how to run
   a single test.
2. High-level code architecture and structure so that future instances can be
   productive more quickly. Focus on the "big picture" architecture that requires
   reading multiple files to understand.

Usage notes:
- If there's already a CLAUDE.md, suggest improvements to it.
- When you make the initial CLAUDE.md, do not repeat yourself and do not include
  obvious instructions like "Provide helpful error messages to users", "Write unit
  tests for all new utilities", "Never include sensitive information (API keys,
  tokens) in code or commits".
- Avoid listing every component or file structure that can be easily discovered.
- Don't include generic development practices.
- If there are Cursor rules (in .cursor/rules/ or .cursorrules) or Copilot rules
  (in .github/copilot-instructions.md), make sure to include the important parts.
- If there is a README.md, make sure to include the important parts.
- Do not make up information such as "Common Development Tasks", "Tips for
  Development", "Support and Documentation" unless this is expressly included in
  other files that you read.
- Be sure to prefix the file with the following text:

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

---

## 3. 구버전 프롬프트 (2025년 초 리버스 엔지니어링)

```text
Please analyze this codebase and create a CLAUDE.md file containing:
1. Build/lint/test commands - especially for running a single test
2. Code style guidelines including imports, formatting, types, naming conventions,
   error handling, etc.

Usage notes:
- The file you create will be given to agentic coding agents (such as yourself)
  that operate in this repository. Make it about 20 lines long.
- If there's already a CLAUDE.md, improve it.
- If there are Cursor rules (in .cursor/rules/ or .cursorrules) or Copilot rules
  (in .github/copilot-instructions.md), make sure to include them.
- Be sure to prefix the file with the following text:

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.
```

> 출처: [Kir Shatrov — Reverse engineering Claude Code](https://kirshatrov.com/posts/claude-code-internals) (2025년 4월)

---

## 4. 버전 비교 — 무엇이 바뀌었나

### 4-1. Diff 요약

| 항목 | 구버전 (2025 초) | 현재 (2026-02) | 변화 의미 |
|------|-----------------|----------------|-----------|
| **필수 콘텐츠 ①** | "Build/lint/test commands" | "Commands that will be commonly used, such as how to build, lint, and run tests" | 더 자연어적, 범위 확장 |
| **필수 콘텐츠 ②** | "Code style guidelines" | **"High-level code architecture and structure"** | 🔴 **코드 스타일 → 아키텍처**로 완전 교체 |
| **크기 제약** | "Make it about **20 lines** long" | ❌ **삭제됨** | 크기 제한 해제 |
| **대상 독자** | "agentic coding agents (such as yourself)" | "future instances of Claude Code" | 더 구체적 (Claude Code 한정) |
| **기존 파일** | "improve it" | "**suggest improvements** to it" | 직접 수정 → 개선 제안으로 완화 |
| **중복 방지** | 없음 | "do not repeat yourself" 명시 | 🆕 추가 |
| **명백한 지시 제외** | 없음 | 구체적 예시 3개로 금지 사항 명시 | 🆕 추가 |
| **파일 구조 제외** | 없음 | "Avoid listing every component or file structure" | 🆕 추가 |
| **일반론 제외** | 없음 | "Don't include generic development practices" | 🆕 추가 |
| **README 포함** | 없음 | "If there is a README.md, include important parts" | 🆕 추가 |
| **날조 금지** | 없음 | "Do not make up information" + 구체적 예시 | 🆕 추가 |

### 4-2. 핵심 변화 3가지

**① 코드 스타일 → 아키텍처로 교체**

구버전:
```
Code style guidelines including imports, formatting, types, naming conventions...
```

현재:
```
High-level code architecture and structure so that future instances can be
productive more quickly. Focus on the "big picture" architecture that requires
reading multiple files to understand.
```

- 코드 스타일은 린터/포매터가 처리 가능 → 프롬프트에서 **제거**
- 대신 "여러 파일을 읽어야 이해할 수 있는" 고수준 아키텍처를 요구
- **"productive more quickly"** — 온보딩 시간 단축이 명시적 목표

**② 20줄 제약 삭제**

- 구버전의 가장 강력한 제약이었던 "about 20 lines"가 완전히 사라짐
- Anthropic이 CLAUDE.md의 역할을 **치트시트 → 종합 프로젝트 가이드**로 확장한 것
- 사용자가 `/init` 결과를 그대로 쓰는 빈도가 높다는 피드백 반영 추정

**③ 안티패턴 방지 규칙 대폭 추가 (4개 → 10개)**

구버전은 Usage notes 4줄이었으나, 현재는 명시적 금지 사항이 대폭 추가됨:

```
금지 1: 자기 반복 (do not repeat yourself)
금지 2: 명백한 지시 (obvious instructions) — 예시 3개 명시
금지 3: 파일 구조 나열 (listing every component)
금지 4: 일반적 개발 관행 (generic development practices)
금지 5: 정보 날조 (make up information) — 예시 3개 명시
```

이는 `/init`의 **과거 출력 품질 문제**를 직접 해결하려는 프롬프트 엔지니어링이다.

---

## 5. 프롬프트 해부 — 구조 분석

### 5-1. 전체 구조

```
[핵심 지시] → "analyze this codebase and create a CLAUDE.md file"
    │
    ├── [What to add] — 2가지 필수 콘텐츠
    │   ├── ① 개발 명령어 (빌드, 린트, 테스트, 단일 테스트)
    │   └── ② 고수준 아키텍처 ("big picture", 다중 파일 이해 필요한 것)
    │
    ├── [Usage notes] — 8가지 제약 조건
    │   ├── 기존 파일 처리: "suggest improvements"
    │   ├── 금지 5종: 반복, 명백한 지시, 파일 구조 나열, 일반론, 날조
    │   ├── 포함 2종: Cursor/Copilot 규칙, README
    │   └── 표준 헤더 강제
    │
    └── [Header prefix] — 고정 텍스트
```

### 5-2. 필수 콘텐츠 상세

**① 개발 명령어**

```
Commands that will be commonly used, such as how to build, lint, and run tests.
Include the necessary commands to develop in this codebase, such as how to run
a single test.
```

- "commonly used" — 자주 쓰는 명령만 (모든 명령 아님)
- "such as" — 빌드/린트/테스트는 **예시**, 프로젝트에 따라 다른 명령도 포함 가능
- **"how to run a single test"** — 구버전부터 유지된 핵심 요구. TDD/디버깅의 기본 도구

**② 고수준 아키텍처**

```
High-level code architecture and structure so that future instances can be
productive more quickly. Focus on the "big picture" architecture that requires
reading multiple files to understand.
```

- **"high-level"** — 파일 단위가 아닌 시스템 단위
- **"reading multiple files to understand"** — 단일 파일에서 알 수 있는 것은 제외
- **"productive more quickly"** — 명시적 목적: 온보딩 속도 향상
- 구버전의 "code style" 대비 훨씬 가치 있는 정보를 요구

### 5-3. 금지 규칙 (Negative Instructions)

현재 프롬프트의 가장 큰 특징은 **"하지 마라" 규칙이 상세하다**는 것이다.

| 금지 규칙 | 구체적 예시 | 의도 |
|-----------|------------|------|
| "do not repeat yourself" | — | 중복 제거로 간결성 확보 |
| "do not include obvious instructions" | "Provide helpful error messages", "Write unit tests", "Never include sensitive info" | **모델이 자주 넣는 뻔한 조언** 방지 |
| "Avoid listing every component" | — | 파일 나열 대신 아키텍처에 집중 |
| "Don't include generic development practices" | — | 프로젝트 고유 정보만 |
| "Do not make up information" | "Common Development Tasks", "Tips for Development", "Support and Documentation" | **환각(hallucination) 방지** — 없는 섹션 날조 금지 |

> 마지막 규칙이 특히 주목할 만하다. LLM이 "있어 보이는" 섹션을 날조하는 문제를 직접 겨냥한다.

### 5-4. 포함 규칙

```
- Cursor rules (.cursor/rules/ or .cursorrules) → include the important parts
- Copilot rules (.github/copilot-instructions.md) → include the important parts
- README.md → include the important parts
```

- 세 곳 모두 **"important parts"** — 전문 복사가 아닌 핵심 추출
- README 포함은 **구버전에 없던 신규 규칙** — 프로젝트 개요 원천으로 활용

### 5-5. 기존 파일 처리

구버전: `improve it` → 현재: `suggest improvements to it`

- "improve" = 직접 수정 (위험)
- "suggest improvements" = 제안 (사용자 판단 존중)
- `/init` 재실행 시 기존 CLAUDE.md를 덮어쓰지 않도록 **더 보수적**으로 변경

---

## 6. 설계 인사이트 — 프롬프트에서 읽는 Anthropic의 전략

### 6-1. "20줄 제약" 삭제의 의미

구버전의 핵심이던 크기 제약이 사라진 것은 CLAUDE.md의 **역할 재정의**를 의미한다:

| 시기 | CLAUDE.md의 역할 | 크기 |
|------|-----------------|------|
| 2025 초 | 간결한 치트시트 | ~20줄 |
| 2026 현재 | 종합 프로젝트 가이드 | 제한 없음 |

추정 배경:
- 컨텍스트 윈도우 확장 (200K → 더 큰 윈도우)으로 비용 부담 감소
- 사용자들이 `/init` 결과를 그대로 쓰는 경향 → 더 풍부한 초기 문서 필요
- 아키텍처 설명은 20줄에 담기 불가능

### 6-2. "코드 스타일" → "아키텍처" 교체의 의미

```
구: Code style guidelines (imports, formatting, types, naming...)
신: High-level code architecture and structure
```

- **코드 스타일은 도구로 해결**: ESLint, Prettier, Black, Ruff 등이 처리
- **아키텍처는 코드에서 읽기 어려움**: 여러 파일에 분산된 설계 의도
- Anthropic이 CLAUDE.md를 **"AI 에이전트의 온보딩 문서"**로 재포지셔닝

### 6-3. 날조 방지의 명시

```
Do not make up information such as "Common Development Tasks", "Tips for
Development", "Support and Documentation" unless this is expressly included
in other files that you read.
```

- **"unless this is expressly included in other files that you read"** — 근거 기반 작성 강제
- LLM의 환각 문제를 프롬프트 레벨에서 직접 차단
- 구체적 예시 3개는 실제로 모델이 자주 날조하는 섹션명

### 6-4. 프롬프트가 여전히 하지 않는 것

| 하지 않는 것 | 의미 |
|-------------|------|
| 출력 섹션 구조 미지정 | 프로젝트별 유연한 구조 허용 |
| WHY(이유) 작성 지시 없음 | 아키텍처 결정의 "이유"는 여전히 자동 포착 어려움 |
| 크기 가이드 없음 | 모델 재량에 완전 위임 |
| Gotcha/함정 수집 지시 없음 | 비직관적 동작은 자동 분석 한계 |
| 갱신/관리 안내 없음 | 생성 후 유지보수 지침 부재 |

---

## 7. `/init` 프롬프트 진화의 교훈

### 변화 방향 요약

```
구버전 (2025 초)                    현재 (2026-02)
────────────────                   ────────────────
짧은 프롬프트 (11줄)                긴 프롬프트 (24줄)
긍정 지시 위주 (do this)            금지 지시 대폭 추가 (don't do this)
크기 제약 (20줄)                    크기 제약 없음
코드 스타일 중심                     아키텍처 중심
"improve it"                       "suggest improvements"
타 도구 규칙만 포함                  README도 포함
환각 방지 없음                      날조 금지 명시
```

### 핵심 교훈

1. **Negative instruction이 중요하다**: 모델이 자주 하는 실수를 구체적 예시와 함께 금지하는 것이 품질을 크게 올림
2. **프롬프트는 진화한다**: 사용자 피드백 → 문제 패턴 발견 → 금지 규칙 추가의 사이클
3. **도구가 해결할 수 있는 것은 프롬프트에서 빼라**: 코드 스타일 → 린터로 위임, CLAUDE.md에서 제거
4. **근거 기반 작성을 강제하라**: "unless this is expressly included in other files" 같은 조건부 허용
5. **`/init`은 여전히 스타터다**: 아키텍처 결정의 WHY, Gotcha, 팀 워크플로우는 수동 보완 필요

---

## 8. 참고 자료

### 프롬프트 원문 출처
- **현재 버전**: 2026-02-24 실제 `/init` 실행으로 확인
- **구버전**: [Kir Shatrov — Reverse engineering Claude Code](https://kirshatrov.com/posts/claude-code-internals) (2025년 4월)

### 관련 자료
- [Kaushik Gopal — Build your own /init command](https://kau.sh/blog/build-ai-init-command/) — 프롬프트 분석 및 커스텀 빌드 가이드
- [Anthropic — Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files) — 공식 CLAUDE.md 활용 가이드
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) — 공식 베스트 프랙티스
- [Claude Code Memory 문서](https://code.claude.com/docs/en/memory) — 파일 체계 및 로딩 메커니즘
- [Agiflow — Claude Code Internals](https://agiflow.io/blog/claude-code-internals-reverse-engineering-prompt-augmentation/) — 프롬프트 증강 메커니즘 분석

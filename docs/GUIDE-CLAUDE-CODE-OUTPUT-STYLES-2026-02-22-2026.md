# GUIDE: Claude Code Output Styles

> Source: [Output styles - Claude Code Docs](https://code.claude.com/docs/en/output-styles)
> Date: 2026-02-22

---

## Overview

Output Styles는 Claude Code의 시스템 프롬프트를 직접 수정하여, 소프트웨어 엔지니어링 이외의 용도로도 활용할 수 있게 하는 기능이다. 파일 읽기/쓰기, 로컬 스크립트 실행, TODO 추적 등 핵심 기능은 유지하면서 응답 방식만 변경한다.

---

## Built-in Styles (3종)

| Style | 설명 |
|-------|------|
| **Default** | 기본 시스템 프롬프트. 소프트웨어 엔지니어링 태스크에 최적화 |
| **Explanatory** | 코딩 작업 사이에 교육적 "Insights"를 제공. 구현 선택과 코드베이스 패턴 이해 지원 |
| **Learning** | 협업형 학습 모드. Insights 제공 + `TODO(human)` 마커로 사용자에게 직접 코드 작성 유도 |

---

## How Output Styles Work

시스템 프롬프트에 대한 영향:

```
┌─────────────────────────────────────────────────┐
│ Claude Code System Prompt                       │
├─────────────────────────────────────────────────┤
│ 1. 간결한 응답 지침        → 모든 style에서 제거  │
│ 2. 코딩 관련 지침          → custom style에서 제거 │
│    (keep-coding-instructions: true면 유지)       │
│ 3. 커스텀 style 지침       → 시스템 프롬프트 끝에  │
│                              추가됨              │
│ 4. 대화 중 스타일 준수      → 리마인더 자동 삽입   │
└─────────────────────────────────────────────────┘
```

핵심 포인트:
- **모든** output style은 간결한 응답(concise output) 관련 지침을 제거한다
- **커스텀** style은 코딩 관련 지침도 제거한다 (기본 동작)
- `keep-coding-instructions: true` 설정 시 코딩 지침을 유지할 수 있다
- 커스텀 지침은 시스템 프롬프트 **끝**에 추가된다
- 대화 중 스타일 준수를 위한 리마인더가 자동으로 삽입된다

---

## Change Output Style

```bash
# 메뉴에서 선택
/output-style

# 직접 지정
/output-style explanatory
/output-style learning

# /config 메뉴에서도 접근 가능
/config
```

변경 사항은 로컬 프로젝트 레벨(`.claude/settings.local.json`의 `outputStyle` 필드)에 저장된다. 다른 레벨의 settings 파일에서 직접 편집도 가능하다.

---

## Create Custom Output Style

### File Format

커스텀 output style은 YAML frontmatter + Markdown 본문으로 구성된다:

```markdown
---
name: My Custom Style
description: "A brief description of what this style does, to be displayed to the user"
keep-coding-instructions: true
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

### Frontmatter Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Output style 이름. UI 표시용 | 파일명에서 상속 |
| `description` | 설명. `/output-style` 메뉴에 표시 | None |
| `keep-coding-instructions` | 코딩 관련 시스템 프롬프트 유지 여부 | `false` |

### File Locations

| Level | Path |
|-------|------|
| User (전역) | `~/.claude/output-styles/` |
| Project (프로젝트) | `.claude/output-styles/` |

`/output-style:new` 명령으로 생성 시 사용자 레벨(`~/.claude/output-styles/`)에 저장된다.

---

## Comparisons to Related Features

| Feature | 동작 방식 | System Prompt 영향 |
|---------|-----------|-------------------|
| **Output Styles** | 기본 시스템 프롬프트의 SW 엔지니어링 부분을 **교체** | 직접 수정 |
| **CLAUDE.md** | 시스템 프롬프트 뒤에 user message로 **추가** | 수정 없음 |
| **--append-system-prompt** | 시스템 프롬프트에 **append** | 끝에 추가 |
| **Agents** | 특정 태스크 처리용. 모델, 도구, 컨텍스트 별도 설정 가능 | 별도 프롬프트 |
| **Skills** | `/skill-name`으로 호출하는 태스크별 프롬프트 | 호출 시 로드 |

### Output Styles vs CLAUDE.md vs --append-system-prompt

```
System Prompt (Default)
├── Output Style    → SW 엔지니어링 부분을 교체/제거
├── --append-system-prompt → 시스템 프롬프트 끝에 append
└── (system prompt 끝)
    └── CLAUDE.md   → user message로 별도 추가 (시스템 프롬프트 수정 없음)
```

### Output Styles vs Agents

- Output Styles: 메인 에이전트 루프에 직접 영향. **시스템 프롬프트만** 변경. 선택하면 항상 활성
- Agents: 특정 태스크 처리용으로 호출. 모델, 도구, 컨텍스트 등 추가 설정 가능

### Output Styles vs Skills

- Output Styles: 응답 **방식**(포맷, 톤, 구조) 변경. 선택 후 항상 활성
- Skills: **태스크별** 프롬프트. `/skill-name`으로 호출하거나 자동 로드

---

## Practical Notes

### keep-coding-instructions 선택 기준

- `true`: 코딩 작업을 주로 하되 응답 스타일만 바꾸고 싶을 때 (예: Data Scientist, Verbose 모드)
- `false`: 코딩과 무관한 용도로 사용할 때 (예: 글쓰기, 리서치, 교육)

### 주의사항

- 커스텀 style에서 `keep-coding-instructions`를 생략하면 기본값 `false`로 코딩 지침이 제거됨
- 코딩 작업용 커스텀 style을 만들 때는 반드시 `keep-coding-instructions: true` 명시 필요

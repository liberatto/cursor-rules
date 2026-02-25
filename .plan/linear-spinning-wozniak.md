# Plan: `work-handoff.md` 커맨드 수정

## Context

현재 `work-handoff.md`는 대화창에만 handoff 문서를 출력하고 파일로 저장하지 않는다. 세션 인계 문서를 `.handoff/` 폴더에 파일로 저장하면서 동시에 대화창에도 동일 내용을 출력하도록 변경한다.

## 변경 대상 파일

| 파일 | 역할 |
|------|------|
| `ClaudeCode/.claude/commands/ssp/work-handoff.md` | **마스터 템플릿** (배포용 원본) |
| `.claude/commands/ssp/work-handoff.md` | **로컬 복사본** (이 저장소에서 사용) |

## 변경 사항

### 1. `allowed-tools` 수정 (마스터 템플릿만)

현재 마스터 템플릿은 `Read, Grep, Glob, Bash, Task`로 제한되어 있어 파일 저장(`Write`)이 불가능하다.

- **변경**: `allowed-tools: Read, Grep, Glob, Bash, Task, Write`

> 로컬 복사본은 이미 `allowed-tools: *`이므로 변경 불필요.

### 2. 파일 저장 지시 추가

현재 마스터 템플릿 마지막 줄:
```
⚠️ **Do NOT create any files. Output directly in the conversation.**
```

이 줄을 제거하고 아래 내용으로 교체:

```markdown
## Output Instructions

1. **파일 저장**: `.handoff/HANDOFF-{TITLE}-{YYYY-MM-DD-HHMM}.md`에 저장
   - `{TITLE}`: 세션 주제를 UPPERCASE, 하이픈 구분으로 요약 (e.g., `API-REFACTOR`, `AUTH-BUGFIX`)
   - `{YYYY-MM-DD-HHMM}`: 현재 날짜/시간
   - `.handoff/` 폴더가 없으면 생성
2. **대화 출력**: 저장한 파일과 동일한 내용을 대화창에 출력
```

### 3. 로컬 복사본 동기화

로컬 복사본(`.claude/commands/ssp/work-handoff.md`)의 마지막 줄:
```
Generate the handoff document now.
```

동일한 Output Instructions 섹션으로 교체하여 마스터와 동기화.

## 최종 파일 구조 (마스터 기준)

```
---
allowed-tools: Read, Grep, Glob, Bash, Task, Write
argument-hint: [focus area or special instructions]
description: Generate a focused handoff document for the next session to continue work seamlessly
---

## User-Specified Focus Area           ← 유지
## Generation Instructions             ← 유지
## Handoff Document Template           ← 유지
## Writing Principles                  ← 유지
## Output Instructions                 ← **신규** (기존 경고문 대체)
```

## 검증 방법

1. 수정 후 `/ssp:work-handoff` 실행 시 `.handoff/` 폴더에 파일 생성 확인
2. 대화창에도 동일 내용 출력 확인
3. 파일명 형식 `HANDOFF-{TITLE}-{YYYY-MM-DD-HHMM}.md` 준수 확인

---
allowed-tools: *
argument-hint: "최종 목표를 한 줄로 (예: REST API에 인증 미들웨어 추가)"
description: "컨텍스트 자동 수집 → 성공 기준 도출 → 메가 프롬프트 조립 → 내장 /goal로 실행 위임"
---

# /ssp:goal — Mega Prompt Builder for /goal

## 🎯 사용자 요청

`$ARGUMENTS`

---

## Phase 1: Context Auto-Collect

아래 항목을 자동으로 수집한다. 사용자에게 묻지 않는다.

1. **Project** — `CLAUDE.md`, `README.md`, `package.json`, `pyproject.toml` 등에서 프로젝트 성격 파악
2. **Stack** — 언어, 프레임워크, 주요 의존성 식별
3. **Current State** — `git status`, 디렉토리 구조, 기존 코드 상태 파악
4. **Working Dir** — 현재 작업 디렉토리 확인
5. **Constraints** — CLAUDE.md, CLAUDE.local.md에서 **사용자 요청과 관련된 제약**만 추출 (무관한 일반 규칙은 제외)
6. **Audience** — 산출물의 사용 대상 (개발팀, 사용자, 자기 자신 등). 명확하지 않으면 가장 가능성 높은 대상으로 추정

---

## Phase 2: Success Criteria

사용자 요청을 기반으로 **측정 가능한 성공 기준 3~5개**를 도출한다.
마지막 두 항목은 항상 포함:

```
1. [구체적이고 측정 가능한 결과]
2. [구체적이고 측정 가능한 결과]
3. [구체적이고 측정 가능한 결과]
4. 최종 산출물이 오류 없이 실행된다
5. 실행 증거를 제시할 수 있다 (테스트 출력 · 스크린샷 · URL)
```

---

## Phase 3: 사용자 확인

Phase 1·2 결과를 **한 번에** 사용자에게 보여주고 승인을 받는다.

출력 형식:

```
━━━ 📋 컨텍스트 수집 결과 ━━━
📦 Project:       [수집 결과]
🛠️ Stack:         [수집 결과]
📂 Current State: [수집 결과]
📍 Working Dir:   [수집 결과]
🚧 Constraints:   [수집 결과]
👥 Audience:      [수집 결과]

━━━ 🎯 성공 기준 (도출) ━━━
1. [기준]
2. [기준]
3. [기준]
4. 최종 산출물이 오류 없이 실행된다
5. 실행 증거를 제시할 수 있다

━━━━━━━━━━━━━━━━━━━━━━━━━━━
위 내용으로 메가 프롬프트를 조립할까요?
조정이 필요하면 알려주세요.
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**⏸️ 여기서 일시 정지.** 사용자가 승인하거나 조정을 요청할 때까지 대기. 조정 사항이 있으면 반영 후 다시 확인.

---

## Phase 4: Mega Prompt Assembly & Delivery

승인되면 아래 메가 프롬프트를 조립하여 코드블록으로 출력한다.

````markdown
```
/goal $ARGUMENTS

—— CONTEXT ——
· Project: [Phase 1 수집값]
· Stack: [Phase 1 수집값]
· Current state: [Phase 1 수집값]
· Working dir: [Phase 1 수집값]
· Constraints: [Phase 1 수집값]
· Audience: [Phase 1 수집값]

—— SUCCESS CRITERIA (ALL MUST BE TRUE) ——
1. [Phase 2 확정 기준]
2. [Phase 2 확정 기준]
3. [Phase 2 확정 기준]
4. 최종 산출물이 오류 없이 실행된다
5. 실행 증거를 제시할 수 있다 (테스트 출력 · 스크린샷 · URL)

—— OPERATING RULES — NON-NEGOTIABLE ——
1. PLAN FIRST. Output a numbered task list before writing any code.
2. WORK AUTONOMOUSLY. Don't ask clarifying Qs unless genuinely blocked.
3. SELF-VERIFY. After every step: run tests, inspect output, confirm it worked.
4. DEBUG YOURSELF. If it fails, diagnose + fix. Don't hand it back.
5. USE EVERY TOOL. MCPs · terminal · web · code exec · pull real data.
6. NO PLACEHOLDERS. No TODOs · no stubs · real components + real states.
7. PROGRESS LOG. Track completed · in-flight · decisions · blockers.
8. STAY ON GOAL. Discoveries off-spec? Note + keep moving.
9. IF BLOCKED. Log the wall · continue everything parallelizable.
10. CHECK SUCCESS BEFORE STOPPING. Re-read criteria · confirm each is met.

—— QUALITY BAR ——
· Code: clean, typed, follows project conventions
· Design: looks like a well-funded startup shipped it
· Output: survives a senior code review
· Docs: every new pattern / env var / decision logged

—— FINAL DELIVERABLE ——
✅ Confirmation each criterion is satisfied
📁 Every file created / modified
🚀 How to run / test / deploy
📊 Proof (screenshot · test output · URL)
📝 Decisions made + anything to know
⚠️ Known limitations + follow-ups

Begin by outputting your plan. Then execute end-to-end without checking in until done or genuinely blocked.
```
````

조립된 프롬프트 출력 후, 아래 안내를 덧붙인다:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 메가 프롬프트 조립 완료

📋 사용법:
1. 위 코드블록 내용 전체를 복사
2. 새 입력란에 그대로 붙여넣기
3. 엔터 → 첫 줄의 /goal이 슬래시 커맨드로 인식되어 자율 실행 시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---
description: "Ralph Loop with defaults (max-iterations=10, completion-promise=DONE)"
argument-hint: "<PROMPT>"
---

Run the following slash command:

/ralph-loop:ralph-loop $ARGUMENTS  --max-iterations 10 --completion-promise "DONE"

IMPORTANT:

- You MUST output '<promise>DONE</promise>' when the task(i.e.`$ARGUMENTS`) is complete.
- If the task is not completed by the time max-iterations is reached, output a summary of all attempts made and the reason for failure.
- Once the ralph-loop terminates, reset and produce no further '<promise>DONE</promise>' output.

 ---END OF PROMPT---
Everything below is internal notes for the file maintainer, NOT instructions for Claude.

<!--
## 참고: 미션·제약을 담은 PROMPT.md 템플릿

루프에 시킬 일이 다단계이거나 제약이 많으면 인라인 인자 대신 `PROMPT.md` 파일로 분리하고
`@PROMPT.md`로 넘기는 것을 권장. 매 이터레이션 동일 입력 보장 + git 추적 + 리뷰 가능.

호출 예:
  /ssp:work-ralph @PROMPT.md
  /ralph-loop @PROMPT.md --max-iterations 30 --completion-promise "DONE"

권장 파일 레이아웃:
  repo/
  ├── PROMPT.md       # 미션·Done When·Never (불변, LLM 수정 금지)
  ├── progress.md     # 체크리스트 (LLM이 매 회 갱신, 누적 메모리)
  ├── specs/          # 참고 명세 — PROMPT.md에서 @specs/X.md 로 참조
  └── src/, tests/

### PROMPT.md 템플릿

```markdown
# Mission
<한 문단으로 무엇을 만들/고칠지. 모호어 금지.>

## Context
- 관련 파일: @specs/REQUIREMENTS.md, @progress.md
- 코드베이스 진입점: src/...
- 외부 의존: <API·DB·서비스>

## Constraints
- 기존 공개 API 시그니처 변경 금지
- 신규 의존성 추가 시 progress.md에 사유 기재
- 테스트 파일은 `tests/` 외 위치 금지
- 1 이터레이션당 변경 파일 ≤ 10

## Workflow (매 이터레이션)
1. progress.md 읽고 다음 미완료 항목 1개 선택
2. 해당 항목 구현 + 테스트
3. 게이트 명령 모두 실행 (아래 Done When)
4. 결과를 progress.md에 [x]/[ ] 갱신
5. 모든 게이트 통과 + 모든 항목 [x] 면 `<promise>DONE</promise>` 출력

## Done When (객관 게이트 — exit code 0 필수)
- `pytest -q` exits 0
- `mypy src/` exits 0
- `ruff check .` exits 0
- progress.md 모든 항목 `[x]`

## Never
- 테스트 삭제·skip·xfail 처리 금지
- progress.md 항목 임의 제거 금지
- PROMPT.md 자체 수정 금지
- 게이트 우회용 mock·하드코딩 금지
- 커밋 메시지에 "DONE" 문자열 포함 금지 (위조 방지)

## On Failure
게이트 실패 시:
- 실패 로그를 progress.md `## Notes` 섹션에 추가
- 가설·다음 시도 계획 1줄 기록
- 동일 실패 3회 연속이면 `<promise>BLOCKED</promise>` 출력 후 사람 개입 대기
```

### 게이트 설계 4요건
1. 객관성 — shell exit code로 판정 (LLM 자가 신고 불가)
2. 자동 실행 가능 — 매 회 자체 점검
3. 위조 불가 — 출력 grep 금지, 외부 명령만 신뢰
4. 점진 수렴 — progress.md `[x]` 단조 증가

### 적합 태스크
- TDD 구현, 타입/린트 0, 버그 재현→수정, 동작 보존 리팩터링,
  PoC 스캐폴드, 패턴 마이그레이션
### 부적합
- 설계·아키텍처 결정, UX 감수성, 요구 발굴, 보안 설계, PRD 작성
-->

<!--
[FIX] ralph-loop plugin stop-hook.sh race condition patch
- File: plugins/marketplaces/claude-plugins-official/plugins/ralph-loop/hooks/stop-hook.sh
- Location: Right after TRANSCRIPT_PATH extraction, before reading the transcript file
- Change: Add `sleep 0.5` (wait for transcript flush)
- Reason: stop hook reads the transcript before it is flushed to disk, failing to detect the <promise> tag
- Note: Plugin auto-updates will reset stop-hook.sh — reapply this patch if the same error recurs
-->

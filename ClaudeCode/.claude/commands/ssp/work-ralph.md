---
description: "Ralph Loop with defaults (max-iterations=10, completion-promise=DONE)"
argument-hint: "<PROMPT>"
---

Before executing, check the form of `$ARGUMENTS`:

- If it's a file reference (`@PROMPT.md`, `@path/to/X.md`) → proceed.
- If it's an inline natural-language task description → **stop and recommend** `/ssp:work-ralph-init "<task>"` first to generate a reviewed `PROMPT.md`. Reason: ralph-loop is immutable across 10–30 iterations; an unvalidated mission risks polluting the codebase. Only proceed with inline arguments if the user explicitly insists.

Run the following slash command:

/ralph-loop:ralph-loop $ARGUMENTS  --max-iterations 10 --completion-promise "DONE"

IMPORTANT:

- You MUST output '<promise>DONE</promise>' when the task(i.e.`$ARGUMENTS`) is complete.
- If the task is not completed by the time max-iterations is reached, output a summary of all attempts made and the reason for failure (no DONE promise).
- Once the ralph-loop terminates, do not re-emit '<promise>DONE</promise>' in subsequent turns of this parent session.

 ---END OF SKILL PROMPT---
Everything below is internal notes for the file maintainer, NOT instructions for Claude.

PROMPT.md 템플릿의 단일 출처는 `work-ralph-init.md` (자매 슬래시 커맨드).
중복 정의를 피하기 위해 본 파일에서는 보유하지 않음.

<!--
[FIX] ralph-loop plugin stop-hook.sh race condition patch
- File: plugins/marketplaces/claude-plugins-official/plugins/ralph-loop/hooks/stop-hook.sh
- Location: Right after TRANSCRIPT_PATH extraction, before reading the transcript file
- Change: Add `sleep 0.5` (wait for transcript flush)
- Reason: stop hook reads the transcript before it is flushed to disk, failing to detect the <promise> tag
- Note: Plugin auto-updates will reset stop-hook.sh — reapply this patch if the same error recurs
-->

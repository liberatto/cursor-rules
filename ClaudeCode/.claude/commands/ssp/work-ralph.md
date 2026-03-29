---
description: "Ralph Loop with defaults (max-iterations=10, completion-promise=DONE)"
argument-hint: "<PROMPT>"
---

Run the following slash command:

/ralph-loop:ralph-loop $ARGUMENTS  --max-iterations 10 --completion-promise "DONE"

IMPORTANT: 
- You MUST output '<promise>DONE</promise>' when the task(i.e.`$ARGUMENTS`) is complete.
- Once the ralph-loop terminates, reset and produce no further '<promise>DONE</promise>' output.


## This is a User's comments, not part of the user's prompt
<!--
[FIX] ralph-loop plugin stop-hook.sh race condition patch
- File: plugins/marketplaces/claude-plugins-official/plugins/ralph-loop/hooks/stop-hook.sh
- Location: Right after TRANSCRIPT_PATH extraction, before reading the transcript file
- Change: Add `sleep 0.5` (wait for transcript flush)
- Reason: stop hook reads the transcript before it is flushed to disk, failing to detect the <promise> tag
- Note: Plugin auto-updates will reset stop-hook.sh — reapply this patch if the same error recurs
-->
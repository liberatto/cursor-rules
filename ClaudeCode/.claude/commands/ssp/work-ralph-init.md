---
description: "Generate ralph-loop PROMPT.md from a task description (asks clarifying questions if essentials are missing)"
argument-hint: "<task description>"
---

You will produce a `PROMPT.md` file that defines a ralph-loop mission. The user's intended task description is:

**$ARGUMENTS**

A ralph-loop will iterate the same `PROMPT.md` up to N times until objective gates pass and emit `<promise>DONE</promise>`. The PROMPT.md is **immutable** during the loop, so getting it right now matters more than speed — a flawed mission will burn 10–30 iterations on the wrong target.

Your job has four phases.

---

## Phase 1 — Understand & infer

Read the user's task description. Then quickly inspect the project to infer defaults:

- **Test/lint/typecheck commands** — read `pyproject.toml`, `package.json`, `Cargo.toml`, `Makefile`, `pre-commit-config.yaml`, or similar. Note what gates are realistic (e.g., `pytest`, `ruff`, `mypy`, `npm test`, `tsc --noEmit`, `eslint`).
- **Project conventions** — glance at `CLAUDE.md`, `AGENTS.md`, or `README.md` if present, to learn naming/style constraints.
- **Codebase entry points** — if the task names a module, locate it; if not, identify the likely directory.

Spend at most ~5 tool calls on this. The point is *defaults to fill the template*, not a deep audit.

---

## Phase 2 — Decide whether to ask

Ralph-loop needs three essentials. For each, decide if you have enough to proceed or must ask:

| Essential | Ready when | Ask if |
| --- | --- | --- |
| **Mission concreteness** | Success is observable from outside (a test passes, a file exists, a metric crosses a threshold) | Description uses vague verbs ("개선", "정리", "최적화") without a measurable target |
| **Done When gates** | Project has identifiable test/lint/type commands, OR the user named specific commands | No test framework detected and user named none |
| **Scope shape** | Task is a single convergence (all tests green, all lint clean) **or** clearly enumerable (N modules, N endpoints) | Ambiguous whether progress.md checklist is needed |

**Optional but valuable** to ask if relevant:
- **Off-limits files/APIs** — public API stability, schema migrations, etc.
- **Failure ceiling** — max iterations the user wants (default 10)

### How to ask

If you decide to ask: use the `AskUserQuestion` tool **once**, with up to 4 questions. Phrase each question with concrete options drawn from the project context (don't ask "what gates?" abstractly — ask "which of these detected commands should be gates?"). Use multiSelect for gate selection.

If the description is already concrete and the project context is clear, **skip the questions entirely** and proceed to Phase 3. Don't ask redundant questions for the sake of asking.

### When to refuse

If the task is **unsuitable for ralph-loop** — architecture decisions, UX work, requirements gathering, security design, PRD writing, anything without objective shell-exit gates — stop and tell the user. Suggest `/ssp:work-plan` or a different workflow. Do not generate a PROMPT.md that pretends ralph-loop fits.

---

## Phase 3 — Generate PROMPT.md

Use the template below. Fill every angle-bracketed placeholder with task-specific content. Don't leave `<TODO>` markers — if you genuinely cannot fill a slot, that means Phase 2 didn't ask enough; go back and ask.

```markdown
# Mission
<one paragraph: what to build/fix, success state observable from outside. No vague verbs.>

## Context
- Related files: <@specs/X.md>, @progress.md
- Codebase entry: <src/path>
- External deps: <APIs, DBs, services — or "none">

## Constraints
- <project-specific, e.g., "public API in src/api/ unchanged">
- 1 iteration: changed files ≤ 10, changed lines ≤ 300, scope = 1 progress.md item (or 1 gate violation if single-gate)
- Beyond Context's listed files, no more than 5 new grep/read calls per iteration
- <add others from user clarification>

## Workflow (each iteration)
1. Read progress.md `## Status` (current iteration, last change, next action) and `## Items` if present. Pick the next unchecked item; single-gate mission: pick the next gate violation.
2. Implement that item OR fix one gate violation, write/update tests.
3. Run gates in order from Done When (fast first, slow last).
4. Update progress.md:
   - `## Status` → bump iteration counter, set `Last update`, write `Last change` (1 line summary of what changed this iteration), write `Next` (next planned action)
   - `## Items` → flip `[ ]` to `[x]` for completed items (multi-step only)
   - `## Notes` → on failure, append 5-line summary
5. All gates pass (+ all items `[x]` if multi-step) → set `## Status` State to `complete` and output `<promise>DONE</promise>`.

## Done When (objective gates — exit code 0 required, run in this order)
- <fast static check, e.g., `ruff check .` exits 0>
- <type check, e.g., `mypy src/` exits 0>
- <test, e.g., `pytest -q` exits 0>
- <(if multi-step) progress.md all `## Items` `[x]`>

## Never
- Delete, skip, or `xfail` tests
- Modify gate config files (`pyproject.toml`, `pytest.ini`, `mypy.ini`, `ruff.toml`, `setup.cfg`, `.pre-commit-config.yaml`, etc.) to bypass failures
- Remove or rename progress.md `## Items` entries, or rewrite past `Last change` history in `## Status`
- Modify PROMPT.md itself
- Use mocks, hardcoded values, or env-var branching to bypass gates
- Include "DONE" or `<promise>` strings in commit messages, code, or comments

## On Failure
On gate failure:
- Add 5-line summary to progress.md `## Notes` section
- Record hypothesis + next plan (1 line)
- Same failure 3 consecutive iterations:
  1. Write detailed report to progress.md `## BLOCKED` (full log, attempt history, suspected cause, what to ask the human)
  2. Output `<promise>DONE</promise>` to terminate the loop normally — operator reviews the BLOCKED section
  Reason: ralph-loop only recognizes the configured completion-promise (default "DONE"); a `BLOCKED` tag won't terminate.
```

### progress.md — always created, scope-adapted

Every ralph-loop mission gets a `progress.md`. It serves as cumulative memory **and** the operator's at-a-glance status board: one file tells whether the loop is healthy, what it just did, and what comes next.

**Standard structure** (you also create this file alongside PROMPT.md):

```markdown
# Progress — <mission slug>

## Status
- State: active                      # active | blocked | complete
- Iteration: 0 / <max-iterations>
- Last update: <YYYY-MM-DD HH:MM>
- Last change: (none yet — bootstrap)
- Next: <first action the loop will take>

## Items
- [ ] <item 1>
- [ ] <item 2>
...

## Notes
(append failure summaries here, one block per failure)

## BLOCKED
(empty unless circuit breaker triggers)
```

**Scope adaptation**:

| Mission shape | `## Items` | What the loop iterates on |
| --- | --- | --- |
| **Single-gate** (e.g., "all failing tests pass", "mypy errors → 0") | omit the section | Pick next gate violation each iteration; converges when all gates pass |
| **Multi-step** (e.g., "migrate N modules") | enumerate every step as `[ ]` | Pick next unchecked item; converges when all `[x]` AND all gates pass |

For single-gate missions, drop the `progress.md all ## Items [x]` line from Done When and remove `## Items` from progress.md, but keep `## Status`, `## Notes`, `## BLOCKED`. The Status header is what makes ralph-loop legible to the operator regardless of mission shape.

---

## Phase 4 — Save and hand off

1. Write `./PROMPT.md` to the current working directory.

2. Write `./progress.md` alongside it, pre-populated with the Standard structure above:
   - `## Status` — State: `active`, Iteration: `0 / <N>`, Last update: now, Last change: `(none yet — bootstrap)`, Next: <the first concrete action the loop should take, derived from your Mission/Items>
   - `## Items` — enumerated for multi-step; omitted for single-gate
   - `## Notes`, `## BLOCKED` — empty stubs

3. **If `./PROMPT.md` already exists**: read its first 20 lines, show them, then ask the user via AskUserQuestion: overwrite / save as `PROMPT-NEW.md` / abort. Do not silently overwrite. Apply the same check to `./progress.md`.

4. After writing, output a brief handoff (3–5 lines):
   - Mission one-liner
   - Gates that will run
   - Suggested isolation: `git switch -c ralph/<task-slug>`
   - Next command: `/ssp:work-ralph @PROMPT.md` (default 10 iterations) or `/ralph-loop:ralph-loop @PROMPT.md --max-iterations 30 --completion-promise "DONE"` for longer runs

Do not invoke ralph-loop yourself — the user reviews PROMPT.md and progress.md first. That review is the safety gate; bypassing it defeats the point of separating init from execution.

---
allowed-tools: Read, Glob, Grep, Edit, Task, Bash(git diff:*), Bash(git status:*), AskUserQuestion
description: "MetaCog self-review: metacognitive critical review and correction of work artifacts"
argument-hint: "[natural language or review|fix] [code|plan|research]"
---

# MetaCog Self-Review

Metacognitive scaffold-based self-review command.
Performs critical self-review (Phase 2) and corrective revision (Phase 3) on the user's initial work output (Phase 1).

**Core principle**: Phase 2 and Phase 3 MUST be separated into distinct inferences.
This is not single-prompt structuring — it achieves genuine Error Recovery through multi-turn chaining.

## Input

`$ARGUMENTS`

---

## Step 0: Parse Input & Map Parameters

Map user input to `mode` and `type` parameters. The user may provide natural language — interpret intent and map accordingly.

### Mode Detection

| Keywords | → mode |
|----------|--------|
| `review`, check, analyze, inspect, look over, audit, examine | `review` |
| `fix`, correct, revise, repair, patch, apply, update, improve | `fix` |

- If ambiguous: use AskUserQuestion — "Review only, or review and fix?"

### Type Detection

| Keywords | → type |
|----------|--------|
| `code`, implementation, function, logic, module, class | `code` |
| `plan`, design, architecture, blueprint, strategy | `plan` |
| `research`, analysis, findings, investigation, study | `research` |

- If not specified: auto-detect from git diff in Step 1
- If auto-detection fails: use AskUserQuestion

---

## Step 1: Context Gathering

### 1.1 Identify Changes

```bash
git status          # changed file list
git diff            # unstaged changes
git diff --cached   # staged changes
```

### 1.2 Auto-Detect Type (when type is not specified)

Determine type from file extensions and filenames:

- `.ts/.js/.py/.go/.java/.rs/...` → `code`
- `.md` with filename `PLAN-*` → `plan`
- `.md` with filename `RESEARCH-*` → `research`
- Mixed code + docs → if any code file exists → `code`
- Docs only but inconclusive → AskUserQuestion

### 1.3 Read Target Files

Read full contents of changed files using the Read tool. Skip:
- Lock files (package-lock.json, yarn.lock, etc.)
- Auto-generated files
- Binary files

### 1.4 Source Cross-Reference (research type only)

When the target artifact cites external sources (e.g., Confluence pages, API docs, papers, datasets), verify key claims against the originals. This step catches misquotation, misattribution, and fabricated figures that textual review alone cannot detect.

**Procedure:**

1. **Extract cited sources** — scan the artifact for page IDs, URLs, document titles, arXiv IDs, or named references.
2. **Prioritize verification targets** — focus on sources that back quantitative claims (figures, percentages, dates) or direct quotations. Skip sources cited only for background context.
3. **Retrieve originals** — use Task tool with appropriate subagents (e.g., `ktspace-atlassian-explorer` for Confluence, `general-purpose` for web/paper lookup). Launch multiple subagents in parallel when checking independent sources.
4. **Cross-check** — for each prioritized source, verify:
   - Quoted text matches the original (no silent paraphrasing presented as direct quotes)
   - Figures and statistics exist in the original and are cited in correct context
   - Summarized content faithfully represents the original (no cherry-picking or omission of key items)
   - Attribution is accurate (correct author, correct document, correct section)
5. **Record discrepancies** — any mismatch found here becomes a finding in Step 2 under the `Source cross-reference` checklist item, with the original text cited as evidence.

**Skip conditions** — skip this step when:
- No external sources are cited (self-contained analysis)
- Sources are inaccessible (e.g., internal systems without MCP tools, paywalled papers)
- The user explicitly requests text-only review

---

## Step 2: Phase 2 — Critical Self-Review

### Execution Branch by Mode

- **`review` mode**: Main agent performs Phase 2 directly.
- **`fix` mode**: Spawn a subagent via Task tool to perform Phase 2. This ensures Phase 2 and Phase 3 run as separate inferences.

### Subagent Instructions (fix mode)

When spawning a `general-purpose` subagent via Task tool, pass:

1. List of changed files and their diff content
2. Work type (code/plan/research)
3. The corresponding checklist for that type
4. Instruction: "Return results in the Review Report format. Do NOT modify any files."

The subagent operates **read-only** — it must not edit any code.

### Type-Specific Checklists

#### Code

```
- [ ] Logic errors: boundary values, off-by-one, null/undefined handling
- [ ] Omissions: missing error handling, unhandled edge cases
- [ ] Excess: code beyond requested scope, unnecessary abstractions
- [ ] Consistency: style mismatch with existing codebase
- [ ] Security: injection, auth/authz, sensitive data exposure
```

#### Plan

```
- [ ] Logical gaps: missing causal links between steps
- [ ] Implicit assumptions: unstated preconditions
- [ ] Feasibility: ignored technical constraints
- [ ] Missing perspectives: failure scenarios, rollback plans
- [ ] Scope creep: over-engineering beyond requirements
```

#### Research

```
- [ ] Confirmation bias: cherry-picked evidence supporting conclusions
- [ ] Source reliability: quality and recency of references
- [ ] Source cross-reference: cited figures, quotes, and summaries match originals (from Step 1.4)
- [ ] Logic structure: premise → evidence → conclusion coherence
- [ ] Missing alternatives: absent counterarguments or alternative interpretations
- [ ] Over-generalization: broad conclusions from limited data
```

### Review Principles

1. **Scope lock**: Review ONLY changed code/content. Existing code is out of scope.
2. **Explicit bias check**: Explicitly examine for confirmation bias, anchoring, and availability heuristic.
3. **Self-contained findings**: Each finding MUST include location, cause, and suggestion. The report alone must be sufficient for decision-making.

---

## Step 3: Output

### review mode → Report and stop

Output the Review Report in the format below and stop. Do NOT modify any files.

```markdown
# MetaCog Review Report

## Summary
- **Target**: N files changed (type: {type})
- **Findings**: 🔴 critical N, 🟡 minor N
- **Verdict**: ✅ Good | ⚠️ Revision recommended | ❌ Revision required

## Findings

### 🔴 Critical

#### [C1] Title
- **Location**: `filepath:line`
- **Category**: Logic error | Omission | Security | ...
- **Current behavior**: How the current code/content works
- **Problem**: Why this is an issue
- **Suggestion**: Specific fix direction (with code snippet)

### 🟡 Minor

#### [M1] Title
- **Location**: `filepath:line`
- **Category**: Consistency | Readability | ...
- **Problem**: ...
- **Suggestion**: ...

## Checklist Applied
- [x] Item — N issues found
- [x] Item — No issues
- ...
```

After the report, show follow-up options:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Review complete. Next steps:

  "Fix C1 and M2"          → Fix specific findings
  /ssp:metacog fix         → Run full review + fix
  /ssp:work-plan           → Create plan from report
  /ssp:work-task           → Define tasks per finding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### fix mode → Receive subagent report, then apply corrections

1. Receive the Review Report from the subagent (Phase 2).
2. Apply corrections for each finding using the Edit tool (Phase 3 — separate inference).
3. Report results in Task Completion Report format.

```markdown
# 1. Status & Summary

- **Status**: ✅ Corrections applied
- **Overview**: critical N, minor N found → all corrected
- **Actions**:
  1. 🔴 [C1] Title → Fixed
  2. 🟡 [M1] Title → Fixed

# 2. Key Information

- **Key Outcomes**: N files modified
- **Decisions**: Judgment calls made during correction (if any)
- **Limitations**: Items that could not be auto-corrected (if any)
```

#### fix mode correction principles

- **If a problem is found, it MUST be fixed.** Expressing uncertainty is not a fix.
- **If a fix is not possible, state the specific reason.**
- **Stay in scope.** Only fix what the findings identify. Do not "improve" surrounding code.

---

## Guidelines

1. **Phase separation is mandatory**: In `fix` mode, Phase 2 (review) and Phase 3 (correction) MUST run as separate inferences. Phase 2 uses a subagent; Phase 3 uses the main agent.
2. **Scope control**: Verify only the correctness and completeness of changed code/content. Existing code improvements and style refactoring are out of scope.
3. **Report even when clean**: If no issues are found, report a "Good" verdict with the applied checklist.
4. **Assign Finding IDs**: Every finding gets a unique ID (C1, C2, M1, M2...) to enable follow-up references.

---
allowed-tools: *
argument-hint: "<plan-file> [step-id or phase]"
description: Execute a specific step or phase from a PLAN file. Updates progress and validates completion.
---

# Implementation Executor

## 📋 Input

`$ARGUMENTS`

---

## 🔍 Phase 1: Setup

### 1.1 Parse Input

Interpret input as:

- `docs/PLAN-*.md Step 1.1` → Execute specific step
- `docs/PLAN-*.md Phase 2` → Execute entire phase
- `Step 2.3` → Use most recent PLAN file

### 1.2 Load Plan & Check Dependencies

1. Locate and parse the plan file
2. Verify prerequisite steps are completed
3. Display target scope:

```
🎯 Target: Step {X.Y} - {Title}
   Files: {Expected files}
   Validation: {Success criteria}

⚠️ Only this step will be executed.
```

If prerequisites are incomplete, ask before proceeding.

---

## 🛠️ Phase 2: Execution

### Scope Discipline

- **DO**: Complete only the specified step(s)
- **DO NOT**: Implement adjacent steps, even if "quick"
- **DO NOT**: Refactor unrelated code

### Uncertainty Handling

If encountering ambiguity:

```
❓ Clarification Needed
   Issue: {Description}
   Options: A) {Option A} | B) {Option B}
```

**STOP and wait for response. Do not assume.**

### Progress Tracking (for multi-part steps)

```
⏳ Step {X.Y}: [2/3] Implementing core logic...
```

---

## ✅ Phase 3: Completion

### 3.1 Validate

Before marking complete:

- Code compiles/runs without errors
- Tests pass (if applicable)
- Step's success criteria met

### 3.2 Update Plan File

**Mark step complete** with timestamp and brief summary:

```markdown
- [x] Step X.Y: Description ✅ {date}
  > Done: {1-3 sentence summary of what was implemented}
```

**Clean up obsolete info** - remove outdated assumptions, update estimates.

### 3.3 Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Step {X.Y} Completed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Changed: {file1.py}, {file2.py}
📝 Plan: {completed}/{total} steps done

📌 Next: Step {X.Z} - {title}
   Run: /implement Step {X.Z}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ⚠️ Constraints

1. **Single Step Focus**: Execute ONLY the specified step(s)
2. **No Silent Assumptions**: Ask when uncertain
3. **Plan is Source of Truth**: All actions trace back to plan

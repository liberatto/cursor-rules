---
allowed-tools: *
argument-hint: "<task description>"
description: Define tasks with structured clarification workflow. Resolves ambiguity → Documents understanding → Awaits execution approval.
---

# Task Clarification & Planning

## 📋 Input Task

`$ARGUMENTS`

---

## 🔍 Phase 1: Ambiguity Analysis & Clarification

Analyze the task from the following perspectives. **Ask clarifying questions only if there are unclear points or assumptions needed.**
Limit questions to a maximum of 7. If the task is already clear, proceed directly to Phase 2.

### Required Checkpoints

1. **Scope**: Are boundaries and inclusions/exclusions clearly defined?
2. **Requirements**: Are functional and non-functional requirements sufficient?
3. **Success Criteria**: Are completion conditions and quality standards specified?

### Optional Checkpoints (for complex tasks)

1. **Edge Cases**: Exception handling and boundary conditions
2. **Technical Constraints**: Tech stack, compatibility, performance limits
3. **Dependencies**: Prerequisites and external dependencies
4. **Implementation Options**: Available approaches and their trade-offs

### Question Format

- If 4 or fewer questions: Use the `AskUserQuestion` tool to present questions via UI
- If 5 or more questions: Output questions directly as text in the terminal

```
❓ [Category] Question content
   - Context: Why this information is needed
   - Options: (if applicable) Present as A or B choices
```

---

## 📝 Phase 2: Task Understanding Report

After questions are resolved (or if none needed), report your understanding in the following format:

### Task Summary
>
> [1-2 sentence summary of task objective]

### Requirements

| Type | Details |
|------|---------|
| Functional | • Item 1 • Item 2 |
| Non-functional | • Item 1 • Item 2 |
| Constraints | • Item 1 |

### Subtasks & Approach

```
1. [Subtask 1] - Approach summary
2. [Subtask 2] - Approach summary
3. [Subtask 3] - Approach summary
```

### Key Deliverables

- [ ] Deliverable 1: Description
- [ ] Deliverable 2: Description

### Assumptions

- Assumption 1: Description (needs confirmation: yes/no)
- Assumption 2: Description

### Risks & Considerations

- ⚠️ Risk factors or important notes (if any)

---

## ✅ Phase 3: Awaiting Execution

If the above is accurate, output the following:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No more questions, we can move on!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**⏸️ Wait for explicit instruction to proceed with execution.**

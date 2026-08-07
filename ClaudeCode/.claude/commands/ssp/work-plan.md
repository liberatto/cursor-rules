---
allowed-tools: *
argument-hint: "<task name or description>"
description: Investigate first, then produce a restated goal, falsifiable assumptions, and an implementation plan — and stop before implementing.
---

# Implementation Planning

## 📋 Input

`$ARGUMENTS`

---

## 🤝 Operating Principle

Work like a contractor who bills for rework: the cost of a wrong assumption is yours to avoid, and the cost of an unnecessary question is mine to pay.

Everything below serves one purpose — surfacing a wrong understanding while it is still cheap to correct. A restatement that turns out wrong is the cheapest possible outcome of this command.

---

## ⚖️ Phase 0: Proportionality — Decide the Depth First

This ceremony scales with blast radius. Pick the mode before doing anything else, and say which mode you picked and why in one line.

| Mode | When | Output |
|------|------|--------|
| **Skip** | Typo fix, rename, or a change under ~20 lines with one obvious correct form | Don't plan. Just do it — this command was the wrong tool |
| **Light** | Single-file or single-module change, reversible, no shared interface touched | Goal + Assumptions + Plan **inline in the response**. No file |
| **Full** | New module, schema change, multi-phase work, or anything touching auth, money, migrations, or deletion | The full `docs/PLAN-*.md` document (Phase 3) |

In **Full** mode, be more suspicious than usual of your own assumptions — the ones you didn't think to write down are the ones that cost.

---

## 🔍 Phase 1: Investigate Before You Ask

### 1.1 Research You Owe

Read the relevant code, tests, configs, and dependency manifests **first**. Anything discoverable in under a minute of searching is not a question — it's research you owe the user.

Never ask about any of these; find them:

- Test framework and how tests are run
- Language/runtime version
- Lint and formatting rules
- Error handling conventions
- Directory layout and module boundaries
- Existing abstractions that already solve part of the problem
- Related `PLAN/PRD/STRATEGY/ANALYSIS-*.md` files in `docs/`, and `CLAUDE.md` / `README.md`

If the codebase contradicts itself — two conventions for the same thing, a config that disagrees with the code — that **is** worth raising. Report it as a finding, not as a question.

### 1.2 Blocking Questions (0–3)

Ask only when a wrong answer means **throwing work away**, not adjusting it. Everything else becomes a numbered assumption in Phase 2 instead.

Each question carries your recommended default, so the user can reply "yes to all" and unblock everything at once. Never ask an open question where a proposed answer would do.

```
❓ [Area] Question
   - Why blocking: What gets thrown away if this is answered differently
   - Recommended default: What you'll assume unless told otherwise
```

If nothing is genuinely blocking, say so explicitly and list zero. A padded question list costs the user a round trip for nothing.

---

## 📐 Phase 2: Goal, Assumptions, and Design

### 2.1 Goal Restatement

One paragraph restating what was asked **in your own words**, including the acceptance criteria you'll hold yourself to. Do not paraphrase the request back — re-derive it from what you read in Phase 1.

### 2.2 Assumptions

Numbered, specific, **falsifiable**. The test is whether the user could look at one and say "no, that's wrong."

- ✅ "Inputs are under 10k rows and fit in memory"
- ✅ "Callers never invoke this concurrently for the same key"
- ❌ "The code should be maintainable" — nothing could contradict it

Cover whichever of these the task actually touches. Skip the rest rather than filling them with placeholders:

| Area | What to pin down |
|------|------------------|
| **Data** | Shape, volume, trust level, encoding, what a malformed input looks like |
| **Failure** | What should happen on timeout, partial write, or downstream 500 — retry, fail loud, or degrade |
| **Boundaries** | Who calls this, what's public API vs. internal, backwards-compat obligations |
| **State** | Concurrency, idempotency, transactionality, ordering guarantees |
| **Environment** | Runtime version, where it deploys, what it's allowed to reach |
| **Scope** | What you're deliberately *not* doing, and what you're leaving as TODO |
| **Testing** | What you'll write tests for and what you'll leave uncovered |

### 2.3 System Context

- How does this task fit into the existing system?
- What components will be affected or created?

### 2.4 Technical Design Considerations

- Data flow and dependencies
- Integration points with existing code/systems
- Technology choices and rationale

### 2.5 Design Decisions

Where you chose between **real alternatives**, name the alternative and say why you rejected it. A decision with no rejected alternative wasn't a decision.

```
Decision: [What was decided]
Context: [Why this decision was needed]
Options Considered: [Alternatives]
Rationale: [Why this option was chosen — and why the others were not]
```

---

## 📝 Phase 3: Plan Document Generation

**Full mode only.** In Light mode, deliver Phases 1–2 plus the file/signature/order list inline and go straight to Phase 4.

### File Naming Convention

```
docs/PLAN-{TASK-NAME}-{YYYY-MM-DD-HHMM}.md
```

- `TASK-NAME`: Uppercase, hyphen-separated (e.g., `HYBRID-SEARCH`)
- Timestamp: Confirm with the `date` command — never guess it

### Plan Document Template

````markdown
# Implementation Plan: {Task Title}

> **Created**: {YYYY-MM-DD HH:MM}
> **Status**: Draft | In Progress | Completed
> **Related**: {Links to related docs/issues}

---

## 1. Overview

### 1.1 Goal (Restated)
[One paragraph in your own words — what is being built and what "done" means]

### 1.2 Objectives
- Primary: [Main goal]
- Secondary: [Additional goals]

### 1.3 Success Criteria
- [ ] Criterion 1: Measurable outcome
- [ ] Criterion 2: Measurable outcome

---

## 2. Requirements & Assumptions

### 2.1 Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-01 | Description | High/Med/Low | |
| FR-02 | Description | High/Med/Low | |

### 2.2 Non-Functional Requirements
| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-01 | Performance | e.g., <200ms | |
| NFR-02 | Scalability | e.g., 10K users | |

### 2.3 Constraints
- Technical: [e.g., Must use existing DB schema]
- Resource: [e.g., Complete within 2 sprints]
- Dependency: [e.g., Requires API v2 release]

### 2.4 Assumptions
Numbered and falsifiable. Each one is something the user can contradict.

| # | Area | Assumption | If wrong |
|---|------|------------|----------|
| A-01 | Data | e.g., Inputs stay under 10k rows and fit in memory | Streaming rewrite of §4 Phase 2 |
| A-02 | Failure | e.g., Downstream 500 means fail loud, no retry | Retry/backoff layer added |
| A-03 | Scope | e.g., Migration of legacy records is explicitly out of scope | Separate plan required |

---

## 3. Architecture & Technical Design

### 3.1 System Architecture
[Text description or ASCII diagram]

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Component  │────▶│  Component  │────▶│  Component  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 3.2 Component Design
| Component | Responsibility | Technology | Notes |
|-----------|---------------|------------|-------|
| Component 1 | Description | Tech stack | |
| Component 2 | Description | Tech stack | |

### 3.3 Data Flow
[Describe how data moves through the system]

### 3.4 Key Design Decisions
| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|---------------------|--------------|
| Decision 1 | Why chosen | Option A | One clause |

---

## 4. Implementation Plan

### 4.0 Files & Signatures
| File | Action | Key signatures introduced or changed |
|------|--------|--------------------------------------|
| `path/to/file.py` | Create / Modify | `def handle(req: Request) -> Result` |

### 4.1 Phase Breakdown

#### Phase 1: Foundation
**Duration**: [Estimated time]
**Goal**: [Phase objective]

- [ ] Step 1.1: Description
  - Details: What specifically needs to be done
  - Files: `path/to/file.py`
  - Validation: How to verify completion

- [ ] Step 1.2: Description
  - Details: ...
  - Files: ...
  - Validation: ...

#### Phase 2: Core Implementation
**Duration**: [Estimated time]
**Goal**: [Phase objective]

- [ ] Step 2.1: Description
- [ ] Step 2.2: Description

#### Phase 3: Integration & Testing
**Duration**: [Estimated time]
**Goal**: [Phase objective]

- [ ] Step 3.1: Description
- [ ] Step 3.2: Description

#### Phase 4: Validation & Cleanup
**Duration**: [Estimated time]
**Goal**: [Phase objective]

- [ ] Step 4.1: Description
- [ ] Step 4.2: Description

### 4.2 Dependency Graph

```
Step 1.1 ──┬──▶ Step 2.1 ──▶ Step 3.1
           │
Step 1.2 ──┘              ──▶ Step 3.2
```

---

## 5. Validation Strategy

### 5.1 Testing Approach
| Test Type | Scope | Tools | Criteria |
|-----------|-------|-------|----------|
| Unit | Components | pytest | 80% coverage |
| Integration | APIs | pytest | All endpoints |
| E2E | User flows | Playwright | Critical paths |

### 5.2 Deliberately Uncovered
| What | Why not tested | Risk accepted |
|------|----------------|---------------|
| e.g., Retry backoff timing | Requires a clock harness | Timing regressions land silently |

### 5.3 Acceptance Criteria
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Documentation updated

---

## 6. Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | High/Med/Low | High/Med/Low | Strategy |
| Risk 2 | High/Med/Low | High/Med/Low | Strategy |

---

## 7. Deliverables

| Deliverable | Description | Location |
|-------------|-------------|----------|
| Source Code | Implementation | `src/feature/` |
| Tests | Test suite | `tests/feature/` |
| Documentation | API docs, README | `docs/` |
| Config | Configuration files | `config/` |

---

## 8. Context & References

### 8.1 Gathered Context
[What was actually read in Phase 1 — files, tests, configs. Name them]

### 8.2 Related Resources
- [Link to related documentation]
- [Link to design specs]
- [Link to issues/tickets]

### 8.3 Open Questions
- [ ] Question 1: [Non-blocking — to be resolved before/during implementation]

---

## Appendix

### A. Glossary
| Term | Definition |
|------|------------|
| Term 1 | Definition |

### B. Change Log
| Date | Author | Changes |
|------|--------|---------|
| {date} | Claude | Initial plan created |
````

---

## ⏸️ Phase 4: Stop

**Then wait. Do not begin implementing.**

In Full mode, save the file and output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Plan Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 File: docs/PLAN-{TASK-NAME}-{YYYY-MM-DD-HHMM}.md
📊 Phases: {N} phases, {M} action items
❓ Blocking questions: {0-3}
📌 Assumptions: {N} — reply "yes to all" to accept the defaults
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to begin? Use:
  /ssp:work-do docs/PLAN-{filename}.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

In Light mode, end with the same blocking-questions and assumptions summary inline — no file, no box.

---

## 🔁 Phase 5: After Approval

Implement the plan **as approved**.

If you discover mid-implementation that an assumption was wrong, or that the plan doesn't survive contact with the code — stop and say so, naming which assumption broke. Do not quietly improvise a different design, and do not press on with an approach you now believe is wrong.

A plan that had to change is a normal outcome. A plan that silently stopped describing what you're building is not.

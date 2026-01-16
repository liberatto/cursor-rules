---
allowed-tools: *
argument-hint: "<task name or description>"
description: Create a comprehensive implementation plan with architecture, workflow, and actionable steps. 
---

# Implementation Planning

## 📋 Input

`$ARGUMENTS`

---

## 🔍 Phase 1: Context Gathering

Before creating the plan, gather all relevant context:

### 1.1 Scan for Existing Context

- Check for related `PLAN/PRD/STRATEGY/ANAL-*.md` files in `docs/`
- Review `CLAUDE.md` or `README.md` for project context
- Identify relevant source files, configs, or documentation
- Look for any previous task definitions or requirements documents

### 1.2 Clarify if Needed

If critical information is missing for planning, ask **up to 5 targeted questions**:

```
❓ [Area] Question
   - Why needed: Brief explanation
   - Default assumption: What you'll assume if not answered
```

If sufficient context exists, proceed to Phase 2.

---

## 📐 Phase 2: Architecture & Design Analysis

Analyze and document the following aspects:

### 2.1 System Context

- How does this task fit into the existing system?
- What components will be affected or created?

### 2.2 Technical Design Considerations

- Data flow and dependencies
- Integration points with existing code/systems
- Technology choices and rationale

### 2.3 Design Decisions

Document key decisions using ADR-lite format:

```
Decision: [What was decided]
Context: [Why this decision was needed]
Options Considered: [Alternatives]
Rationale: [Why this option was chosen]
```

---

## 📝 Phase 3: Plan Document Generation

Create the plan file with the following specifications:

### File Naming Convention

```
docs/PLAN-{task-name}-{YYYYMMDD}-{HHMM}.md
```

- `task-name`: Upperrcase, hyphen-separated (e.g., `HYBRID-SEARCH`)
- Date/Time: Use current timestamp

### Plan Document Template

```markdown
# Implementation Plan: {Task Title}

> **Created**: {YYYY-MM-DD HH:MM}
> **Status**: Draft | In Progress | Completed
> **Related**: {Links to related docs/issues}

---

## 1. Overview

### 1.1 Task Summary
[1-2 paragraph description of what needs to be accomplished]

### 1.2 Objectives
- Primary: [Main goal]
- Secondary: [Additional goals]

### 1.3 Success Criteria
- [ ] Criterion 1: Measurable outcome
- [ ] Criterion 2: Measurable outcome

---

## 2. Requirements

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
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| Decision 1 | Why chosen | Option A, Option B |

---

## 4. Implementation Plan

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

### 5.2 Acceptance Criteria
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
[All relevant information discovered during planning]

### 8.2 Related Resources
- [Link to related documentation]
- [Link to design specs]
- [Link to issues/tickets]

### 8.3 Open Questions
- [ ] Question 1: [To be resolved before/during implementation]
- [ ] Question 2: [To be resolved before/during implementation]

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
```

---

## ✅ Phase 4: Completion

After creating the plan file:

1. **Save** the file to `docs/PLAN-{task-name}-{date}-{time}.md`
2. **Output** a summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Plan Created Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 File: docs/PLAN-{task-name}-{date}-{time}.md
📊 Phases: {N} phases, {M} action items
⏱️ Estimated effort: {estimate}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to begin implementation? Use:
  /implement docs/PLAN-{filename}.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**⏸️ Do NOT start implementation. Wait for explicit instruction.**

```

# User's `CLAUDE.md`(Global Principles)

---

## Language Standards

- **Primary Language**: Always respond in natural Korean (한국어).
- **Code Comments**: Write in Korean with English for technical terms that don't have natural Korean equivalents (e.g., "API endpoint" OK, but "사용자" preferred over "user").
- **Variable/Function Names**: Use English following standard conventions(@see Code Quality Standards).
- **Technical Documentation**: Korean explanations with English code examples.

---

## Core Working Principles

### 1. Verify Before Acting

- **Never Assume**: Use `Grep`, `Read`, `Glob` , `Bash` , `Task(Explore)` to validate context before code changes.
- **Check State**: Run `pwd`, `ls` when directory context is unclear.
- **Ground in Facts**: Base all responses on verified information from tools and codebase.

### 2. Understand Requirements Clearly

- **Restate Goal**: Briefly summarize the core objective before execution.
- **Scope Discipline (Anti-Gold Plating)**: Deliver precisely what is requested. Avoid adding unrequested features, dependencies, or "just-in-case" logic
- **Ask When Unclear**: Stop and request clarification if (a) multiple valid interpretations exist, (b) critical information is missing, or (c) change carries breaking risk.

### 3. Make Safe, Minimal Changes

- **Analyze First**: Review code structure, dependencies, and side effects before editing
- **Smallest Edit**: Make the minimum change needed to achieve the goal.
- **Communicate Risk**: For breaking changes (data loss, security impact, production outage), explain risk and seek confirmation first. For routine changes, proceed and note any minor risks in completion report.

### 4. Leverage Full Context

- **Cross-Reference & Synthesize**: Contextualize the request by synthesizing conversation history, provided files, and tool execution results.
- **Knowledge Augmentation**: Proactively use `WebSearch` or MCP tools to bridge information gaps or verify time-sensitive data.
- **Self-Correction & Iteration**: Evaluate the relevance of search results; if the depth is inadequate, perform recursive searches with refined queries.

### 5. Deliver Quality Results

- **Reusable Code**: Structure logic for reuse across the codebase.
- **Zero-Placeholder Policy**: Provide fully functional code without omitting logic. If partial delivery is necessary, explicitly mark extension points as API Interface or Abstract Logic.
- **Idiomatic Compliance**: Strictly follow language-specific idioms (e.g., PEP8, Effective Java) and the established coding style of the current project.

### 6. Self-Validate Work

- **Requirement Traceability**: Perform a final cross-check to ensure every functional and non-functional requirement is mapped to the implementation.
- **Robustness Stress-Test**: Simulate execution for happy paths, boundary conditions, and potential failure modes to ensure exception handling is robust.
- **Systematic Debugging & Escalation**: Upon failure, diagnose the root cause and report findings. Attempt alternative strategies; if blocked by ambiguity, escalate by asking for clarification.

### 7. No Shortcuts - Solve or Report

- **Never Fake Progress**: No hardcoded values, mocks, or hacks to appear functional.
- **Root Cause Over Symptoms**: Prioritize solving the actual problem. If only a workaround is feasible, implement it but clearly document the limitation and underlying cause.
- **Stop and Escalate When Stuck**: If no real solution is found, halt and explain the blockers clearly rather than producing incomplete work.
- **Report Honestly**: Clearly distinguish "solved" from "worked around" or "partially implemented".
- **Seek Input**: When stuck, describe what was attempted, why it failed, suggest alternatives, and ask for guidance.

---

## Task Completion Reports

**Required Format:**

```markdown

# 1. Status & Summary

- **Completion Status**: Start with emoji indicator (✅ completed, ⚠️ has issues, ❌ failed).
- **Overview**: Concise summary of what was accomplished 1-2 sentence.
- **Actions Taken**: List major actions using numbered list with emoji per item.

# 2. Key Information *(include relevant sections only)*

- **Key Outcomes**: Highlight primary results, deliverables, or findings (quantifiable metrics, files created, insights discovered).
- **Decisions**: Explain important choices (architecture, performance, behavior).
- **Assumptions**: State information inferred without explicit confirmation.
- **Limitations**: Note incomplete aspects, risks, or follow-up needed.
- **Errors**: What failed, why, and what was tried.

```

---

## Code Quality Standards

### Naming Conventions

  | Language | Variables/Functions | Classes | Constants |
  |----------|-------------------|---------|-----------|
  | Python | `snake_case` | `PascalCase` | `UPPER_CASE_WITH_UNDERSCORES` |
  | Java | `camelCase` | `PascalCase` | `UPPER_CASE_WITH_UNDERSCORES` |
  | JavaScript | `camelCase` | `PascalCase` | `UPPER_CASE_WITH_UNDERSCORES` |
  | Other | Follow official language conventions |

### Documentation

- **Functions/Classes**: Write docstrings for all public APIs.
- **Complex Logic**: Add inline comments explaining non-obvious decisions.
- **Parameters**: Document inputs, outputs, and exceptions.
- **Examples**: Include usage examples for non-trivial cases.

### Code Organization

- **Single Responsibility**: Each function/class does one thing well.
- **Meaningful Names**: Use clear, descriptive identifiers.
- **Logical Grouping**: Organize related functionality together.
- **Focused Functions**: Keep functions short and readable.

### Error Handling

- **Robust Patterns**: Use language-appropriate error handling (try-catch, Result types, etc.)
- **Clear Messages**: Provide actionable error messages with context.
- **Graceful Degradation**: Handle failures without crashing when possible.

---

## Document Naming Convention

### Markdown File Naming Rules

- **Format**: `{PREFIX}-{BRIEF-DESCRIPTION}-{YYYY-MM-DD-HHMM}.md`
- **Style**: ALL UPPERCASE for prefix and description, hyphen-separated.
- **Timestamp**: Use current date/time (e.g., `2025-10-02-1430`)
- **Verification**: Confirm related code/docs exist before creating.
- **Default Location**: Save to `docs/` folder unless specified otherwise.

### Document Type Prefixes

 | Prefix | Purpose | Example |
 |--------|---------|---------|
 | `PRD` | Product Requirements | `PRD-USER-AUTH-FEATURE-2025-10-02-1430.md` |
 | `PLAN` | Implementation Plans | `PLAN-DATABASE-MIGRATION-2025-10-02-1430.md` |
 | `RESEARCH` | Research Findings | `RESEARCH-GRAPHQL-VS-REST-2025-10-02-1430.md` |
 | `REPORT` | Status/Progress Reports | `REPORT-Q3-PERFORMANCE-2025-10-02-1430.md` |
 | `GUIDE` | How-to Guides | `GUIDE-DEPLOY-PRODUCTION-2025-10-02-1430.md` |
 | `ANALYSIS` | Technical Analysis | `ANALYSIS-MEMORY-LEAK-ROOT-CAUSE-2025-10-02-1430.md` |
 | `ADR` | Architecture Decision Record | `ADR-MICROSERVICES-MIGRATION-2025-10-02-1430.md` |
 | `NOTE` | Quick Notes/Memos | `NOTE-MEETING-MINUTES-2025-10-02-1430.md` |
 | `DOCUMENTATION` | General Documentation | `DOCUMENTATION-API-REFERENCE-2025-10-02-1430.md` |

## Important Notes

### Date Handling

- **Current Date**: Always use `Current Date` from user environment info.
- **⚠️ Warning**: Do NOT confuse LLM knowledge cutoff date with today's date.

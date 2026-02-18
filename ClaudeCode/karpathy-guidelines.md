# User's `CLAUDE.md` - Global Principles

---

## Language Standards

- **Primary Language**: Always respond in natural Korean (한국어).
- **Code Comments**: Write in Korean with English for technical terms that don't have natural Korean equivalents (e.g., "API endpoint" OK, but "사용자" preferred over "user").
- **Variable/Function Names**: Use English following standard conventions(@see Code Quality Standards).
- **Technical Documentation**: Korean explanations with English code examples.

---

## Core Working Principles

### 1. Think Before Coding/Acting

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```markdown
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

### 5. No Shortcuts

**Solve or Report. Don't fake progress.**

- No hardcoded values, mocks, or hacks to appear functional.
- Prioritize solving the actual problem.
- If no real solution is found, halt and explain the blockers clearly.
- When stuck, describe what was attempted, why it failed, suggest alternatives, and ask for guidance.

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

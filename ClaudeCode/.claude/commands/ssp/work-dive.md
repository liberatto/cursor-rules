---
allowed-tools: *
argument-hint: "<topic or question>"
description: Deep-dive into codebase and external sources to understand a specific topic.
---

# Research & Context Gathering for Planning or Task Definition

## 📋 Input

`$ARGUMENTS`

---

## 🔍 Phase 1: Internal Discovery

### 1.1 Codebase Analysis

Scan the project for relevant information:

- **Source code**: Related modules, classes, functions
- **Documentation**: `docs/*`, `README.md`, `CLAUDE.md`, `CLAUDE.local.md` inline comments
- **Configuration**: Config files, environment settings
- **Tests**: Test cases that reveal expected behavior
- **History**: Recent changes in related areas (if git available)

### 1.2 Identify Knowledge Gaps

After internal scan, note:

- What was found internally
- What information is still missing
- What needs external verification

---

## 🌐 Phase 2: External Research (if needed)

If internal sources are insufficient:

### 2.1 Web Search

- Search for official documentation, best practices, technical articles
- Prioritize authoritative sources (official docs, reputable tech blogs, papers)

### 2.2 MCP Tools (if available)

- Use available MCP servers for additional context
- Check connected knowledge bases or APIs

### 2.3 Source Tracking

For each external finding, note:

```
📚 Source: {title or description}
   URL: {link}
   Relevance: {why this matters}
```

---

## 📝 Phase 3: Research Report

Output a structured summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 Research Report: {Topic}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Summary
{2-3 sentence overview of key findings}

## Key Concepts
- {Concept 1}: {Brief explanation}
- {Concept 2}: {Brief explanation}
- {Concept 3}: {Brief explanation}

## Internal Findings
- {What exists in codebase}
- {Relevant patterns/conventions found}
- {Related components identified}

## External Context
- {Key insight from external source} [Source: {name}]
- {Best practice or recommendation} [Source: {name}]

## Implications for Implementation
- {How this affects potential task/plan}
- {Constraints or considerations discovered}
- {Recommended approach based on findings}

## References
1. {Internal}: {path/to/file or doc}
2. {External}: {URL or source name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Research complete. Ready for next step.

Suggested follow-ups:
  /task {define the task based on this research}
  /plan {create implementation plan}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📄 Optional: Save Report

If research is substantial, offer to save:

```
💾 Save this report?
   Location: docs/RESEARCH-{topic}-{date}.md
   [Y/n]
```

---

## ⚠️ Guidelines

1. **No Code Snippets**: Focus on concepts and understanding
2. **Cite Sources**: Always attribute external information
3. **Stay Focused**: Research only the specified topic
4. **Be Actionable**: Frame findings for practical use

```

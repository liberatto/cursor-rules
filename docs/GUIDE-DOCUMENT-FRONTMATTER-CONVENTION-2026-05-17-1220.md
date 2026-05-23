---
type: "GUIDE"
audience: "team"
related_docs:
  - docs/GUIDE-CLAUDE-MD-BEST-PRACTICES-2026-02-20-1300.md
created: "2026-05-17 12:20"
tags:
  - frontmatter
  - documentation-convention
  - metadata
---

# Document Frontmatter

Add YAML frontmatter to every Markdown document created in this repository. This ensures context (purpose, audience, lineage) is embedded in the file itself and survives moves, renames, and time gaps.

- **Minimum fields** (always include):

```yaml
---
type: "PRD"                                            # document's nature (PRD, GUIDE, NOTE, REPORT, etc.)
audience: "team"                                       # intended reader (author, team, stakeholders, public, etc.)
related_docs:                                          # docs needed for full context
  - path/to/related-1.md
  - path/to/related-2.md
created: "2026-05-10 16:30"                            # YYYY-MM-DD HH:MM
---
```

- **Optional fields** (add only when useful):
  - `status`: `draft` / `wip` / `archived`
  - `tags`: search and classification keywords
  - `supersedes` / `superseded_by`: document replacement chain
- **Timestamp**: Run `date "+%Y-%m-%d %H:%M"` to obtain the `created` value. Never guess.
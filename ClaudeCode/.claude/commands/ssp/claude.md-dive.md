---
allowed-tools: Bash(git:*), Bash(ls:*), Bash(find:*)
description: Investigate and document the directory architecture, then create or update the Claude memory files based on your findings.
argument-hint: [directory-path]
---

# Investigate and Document the Directory Architecture

**Instructions:**  
Analyze the target directory specified in `$ARGUMENTS`, or default to the current working directory if none is provided.

## 1. Investigate the Architecture

Examine the structure, design principles, and implementation details within this directory and all subdirectories. Focus on identifying:

- Design patterns and how they are applied  
- Internal and external dependencies, along with their intended roles  
- Core abstractions, interfaces, and how components interact  
- Naming conventions, file organization, and overall code layout  

Provide enough detail to give a clear understanding of how the module is structured and why it is designed this way.

## 2. Create or Update Documentation

Generate a `CLAUDE.md` file including the insights from your analysis.  
If a `CLAUDE.md` file already exists, update it to reflect your latest findings.

Include the following sections:

- **Module Purpose & Responsibilities**: What this directory/module is meant to do  
- **Architectural Decisions**: Key design choices and their rationale  
- **Implementation Highlights**: Important mechanisms, algorithms, or workflows  
- **Common Patterns**: Repeated patterns, conventions, or idioms used in the code  
- **Notable Caveats or Behaviors**: Any non-obvious details, pitfalls, or unexpected behavior developers should be aware of  

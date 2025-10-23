---
allowed-tools: *
description: Analyze the user-provided $ARGUMENTS and design a structured, actionable step-by-step plan, including architecture and workflow.
model: sonnet
---

User input(task): 

`$ARGUMENTS`

Analyze the user-provided `$ARGUMENTS` and design a structured, actionable step-by-step plan, including architecture and workflow.

Create a plan file named: `PLAN-{task-name}-{date}-{time}.md` and save it under the docs/ folder.

The Plan file should contain:

- Concise task definition
- Requirements
- Architecture & technical design
- Implementation & validation plan
- Issues and risks
- Key deliverables
- Action points for step by step implementation with [ ] checkboxes for marking them done
- All the context information for this task you found before

Don't start any implementation yet, just create the plan file.

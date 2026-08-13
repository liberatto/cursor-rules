# Prompt Templates Reference — Claude Code Edition

Full template library for Prompt Master. Read the relevant template when the user's task type matches. Do not load all templates at once — only the one you need.

## Table of Contents

| Template | Best For |
|----------|----------|
| [A — RTF](#template-a--rtf) | Simple one-shot tasks |
| [B — RISEN](#template-b--risen) | Complex multi-step projects |
| [C — Chain of Thought](#template-c--chain-of-thought) | Logic, math, analysis, debugging |
| [D — Few-Shot](#template-d--few-shot) | Consistent structured output, pattern replication |
| [E — ReAct + Stop Conditions](#template-e--react--stop-conditions) | Autonomous agentic execution (core template) |
| [F — Prompt Decompiler](#template-f--prompt-decompiler) | Breaking down, adapting, or splitting existing prompts |

---

## Template A — RTF

*Role, Task, Format. Use for fast one-shot tasks where the request is clear and simple.*

```
Role: [One sentence defining who the AI is]
Task: [Precise verb + what to produce]
Format: [Exact output format and length]
```

**Example:**
```
Role: You are a senior Python developer.
Task: Write a utility function that validates email addresses using regex, with proper error handling.
Format: Single Python function with type hints and docstring. No external dependencies.
```

---

## Template B — RISEN

*Role, Instructions, Steps, End Goal, Narrowing. Use for complex projects, multi-step tasks, and any output that requires a clear sequence of actions.*

```
Role: [Expert identity the AI should adopt]
Instructions: [Overall task in plain terms]
Steps:
  1. [First action]
  2. [Second action]
  3. [Continue as needed]
End Goal: [What the final output must achieve]
Narrowing: [Constraints, scope limits, what to exclude]
```

**Example:**
```
Role: You are a senior backend engineer with expertise in REST API design.
Instructions: Add pagination to the /api/users endpoint.
Steps:
  1. Read src/routes/users.ts and understand the current query logic
  2. Add page and limit query parameters with defaults (page=1, limit=20)
  3. Update the database query to use OFFSET and LIMIT
  4. Add total count and pagination metadata to the response
End Goal: GET /api/users?page=2&limit=10 returns the correct slice with pagination metadata.
Narrowing: Only modify src/routes/users.ts and src/models/user.ts. Do not add new dependencies. Do not change existing response fields.
```

---

## Template C — Chain of Thought

*Use for logic-heavy tasks, debugging, and multi-factor analysis where careful reasoning before action is needed.*

```
[Task statement]

Before making changes, think through this carefully:
<thinking>
1. What is the actual problem being asked?
2. What constraints must the solution respect?
3. What are the possible approaches?
4. Which approach is best and why?
</thinking>

Then implement the chosen approach.
```

**When to use:**
- Debugging where the cause is not obvious
- Comparing two technical approaches
- Any architectural decision
- Analysis where a wrong first impression is likely

**When NOT to use:**
- Simple tasks where the answer is clear (unnecessary overhead)
- Creative tasks (CoT can kill natural voice)

---

## Template D — Few-Shot

*Use when the output format is easier to show than describe. Examples outperform written instructions for format-sensitive tasks every time.*

```
[Task instruction]

Here are examples of the exact format needed:

<examples>
  <example>
    <input>[example input 1]</input>
    <output>[example output 1]</output>
  </example>
  <example>
    <input>[example input 2]</input>
    <output>[example output 2]</output>
  </example>
</examples>

Now apply this exact pattern to: [actual input]
```

**Rules:**
- 2 to 5 examples is the sweet spot. More rarely helps and wastes tokens.
- Examples must include edge cases, not just easy cases.
- Use XML tags to wrap examples — Claude parses XML reliably.

---

## Template E — ReAct + Stop Conditions

*Claude Code의 핵심 템플릿. 자율적으로 도구를 실행하고 파일을 편집하는 에이전트 실행에 최적화.*

```
Objective:
[Single, unambiguous goal in one sentence]

Starting State:
[Current file structure / codebase state / environment]

Target State:
[What should exist when done]

Allowed Actions:
- [Specific action the agent may take]
- Install only packages listed in [requirements.txt / package.json]

Forbidden Actions:
- Do NOT modify files outside [directory/scope]
- Do NOT run the dev server or deploy
- Do NOT push to git
- Do NOT delete files without showing a diff first
- Do NOT make architecture decisions without human approval

Stop Conditions:
Pause and ask for human review when:
- A file would be permanently deleted
- A new external service or API needs to be integrated
- Two valid implementation paths exist and the choice affects architecture
- An error cannot be resolved in 2 attempts
- The task requires changes outside the stated scope

Checkpoints:
After each major step, output: ✅ [what was completed]
At the end, output a full summary of every file changed.
```

**Example:**
```
Objective:
Add JWT authentication middleware to the Express API server.

Starting State:
- Express server in src/app.ts, routes in src/routes/
- No auth currently implemented
- PostgreSQL with users table (id, email, password_hash)

Target State:
- src/middleware/auth.ts with JWT verify middleware
- POST /auth/login and POST /auth/register in src/routes/auth.ts
- All existing routes under /api/* require valid JWT
- Tests pass

Allowed Actions:
- Create new files in src/middleware/ and src/routes/
- Modify src/app.ts to register new routes and middleware
- Install jsonwebtoken and bcrypt (already in package.json)

Forbidden Actions:
- Do NOT modify existing route handlers
- Do NOT change database schema
- Do NOT modify .env or config files
- Do NOT add features beyond login/register/verify

Stop Conditions:
Pause and ask when:
- Token expiry strategy needs a decision (short-lived vs refresh tokens)
- Password hashing rounds need to be decided
- Any existing test breaks

Checkpoints:
After each step output: ✅ [what was completed]
```

---

## Template F — Prompt Decompiler

*Use when the user pastes an existing prompt and wants to break it down, simplify, or split it.*

**Detect which task is needed:**
- **Break down** — explain what each part of the prompt does
- **Simplify** — remove redundancy and tighten without losing meaning
- **Split** — divide a complex one-shot prompt into a cleaner sequence

**Break down output format:**
```
Original prompt: [paste]

Structure analysis:
- Role/Identity: [what role is assigned and why]
- Task: [what action is being requested]
- Constraints: [what limits are set]
- Format: [what output shape is expected]
- Weaknesses: [what is missing or could cause wrong output]

Recommended fix: [rewritten version with gaps filled]
```

**Split output format:**
```
Original prompt: [paste]

This prompt is doing [N] things. Split into [N] sequential prompts:

Prompt 1 — [what it handles]:
[prompt block]

Prompt 2 — [what it handles]:
[prompt block]

Run these in order. Each output feeds the next.
```

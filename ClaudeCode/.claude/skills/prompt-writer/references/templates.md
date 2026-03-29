# Prompt Templates Reference — Claude Code Edition

Full template library for Prompt Master. Read the relevant template when the user's task type matches. Do not load all templates at once — only the one you need.

## Table of Contents

| Template | Best For |
|----------|----------|
| [A — RTF](#template-a--rtf) | Simple one-shot tasks |
| [B — RISEN](#template-b--risen) | Complex multi-step projects |
| [C — CRISPE](#template-d--crispe) | Creative work, brand voice |
| [D — Reasoning Output](#template-d--reasoning-output) | When the user needs to see the reasoning behind the answer |
| [E — Few-Shot](#template-e--few-shot) | Consistent structured output, pattern replication |
| [F — ReAct + Stop Conditions](#template-f--react--stop-conditions) | Autonomous agentic execution (core template) |
| [G — Prompt Decompiler](#template-g--prompt-decompiler) | Breaking down, adapting, or splitting existing prompts |

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

## Template C — CRISPE

*Capacity, Role, Insight, Statement, Personality, Experiment. Use for creative work, brand voice writing, and any task where personality, tone, and iteration matter.*

```
Capacity: [What capability or expertise the AI should have]
Role: [Specific persona to adopt]
Insight: [Key background insight that shapes the response]
Statement: [The core task or question]
Personality: [Tone and style — witty / authoritative / casual / sharp]
Experiment: [Request variants or alternatives to explore]
```

**Example:**
```
Capacity: Expert copywriter specializing in SaaS product launches.
Role: Brand voice for a productivity tool aimed at developers.
Insight: Developers hate marketing speak and respond to honesty and specificity.
Statement: Write the hero headline and sub-headline for the landing page.
Personality: Sharp, dry, confident — no adjectives, no exclamation marks.
Experiment: Give 3 variants ranging from minimal to bold.
```

---

## Template D — Reasoning Output

*Claude Code performs extended thinking internally, but its reasoning is hidden from the user. Use this template when the user needs to see the decision rationale, comparison analysis, or justification in the output.*

```
[Task statement]

After completing the task, include a "## Reasoning" section that explains:
1. What options or approaches were considered
2. What tradeoffs were evaluated
3. Why the chosen approach was selected
4. What was explicitly ruled out and why
```

**When to use:**
- Architecture decisions where the user needs to review the rationale
- Choosing between two or more valid approaches
- Code review or debugging where "why this way" needs to be visible
- When the user needs to share or document the result with others

**When NOT to use:**
- Simple tasks where the rationale is self-evident
- When the user only wants the result, not the process

**Important:** NEVER use `<thinking>` tags in generated prompts. Claude's extended thinking already handles internal reasoning — forcing `<thinking>` output causes double reasoning and post-hoc rationalization. Instead, request reasoning as an explicit output section.

---

## Template E — Few-Shot

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

## Template F — ReAct + Stop Conditions

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

## Template G — Prompt Decompiler

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

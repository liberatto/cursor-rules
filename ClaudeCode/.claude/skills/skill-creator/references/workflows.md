# Claude Code Workflow Patterns

## Sequential Workflows

For tasks with clear step-by-step procedures:

```markdown
## Setup Workflow

1. Detect project type (check for package.json, pyproject.toml, etc.)
2. Verify prerequisites (git, node/python, etc.)
3. Run initialization script
4. Configure project settings
5. Verify setup completed successfully
```

**Best Practice:** Number steps and include the tool/script for each step.

## Conditional Workflows

For tasks with branching logic based on context:

```markdown
## Workflow Selection

**Determine the task type:**

├─ **New project?**
│  └─ Run `scripts/init_project.py`
│
├─ **Adding to existing project?**
│  ├─ Has package.json → Follow Node.js workflow
│  ├─ Has pyproject.toml → Follow Python workflow
│  └─ Other → Follow generic workflow
│
└─ **Debugging/fixing?**
   └─ See [references/troubleshooting.md](references/troubleshooting.md)
```

## Project Detection Pattern

Essential for Claude Code skills that need to adapt to project context:

```markdown
## Project Detection

Check these files to determine project type and configuration:

| File | Indicates | Action |
|------|-----------|--------|
| `package.json` | Node.js project | Use npm/yarn commands |
| `pyproject.toml` | Modern Python | Use poetry/pip |
| `requirements.txt` | Python (legacy) | Use pip |
| `Cargo.toml` | Rust project | Use cargo |
| `go.mod` | Go project | Use go commands |
| `.git/` | Git enabled | Can use git commands |
| `Makefile` | Build automation | Check for targets |

**Detection Script:**
```bash
python scripts/detect_project.py --path .
```
```

## Multi-Stage Workflows

For complex operations spanning multiple steps:

```markdown
## API Development Workflow

### Stage 1: Setup
1. Create project structure
2. Install dependencies
3. Configure environment

### Stage 2: Development
1. Define data models
2. Create endpoints
3. Add validation

### Stage 3: Testing
1. Write unit tests
2. Run integration tests
3. Check coverage

### Stage 4: Deployment
1. Build container
2. Push to registry
3. Deploy to environment
```

## Error Recovery Pattern

Handle failures gracefully:

```markdown
## Error Recovery

If a step fails:

1. **Check prerequisites**
   - Required tools installed?
   - Correct permissions?
   - Network available?

2. **Review error message**
   - See [references/errors.md](references/errors.md) for common errors

3. **Retry or rollback**
   - Use `scripts/cleanup.py` to reset state
   - Retry from the failed step

4. **Escalate if needed**
   - Document what was tried
   - Provide error logs
```

## Iterative Refinement Pattern

For tasks requiring multiple passes:

```markdown
## Code Review Workflow

1. **Initial Analysis**
   - Run linter: `npm run lint` / `ruff check .`
   - Run type checker: `tsc --noEmit` / `mypy .`

2. **Fix Issues**
   - Address critical errors first
   - Then warnings
   - Then style issues

3. **Verify Fixes**
   - Re-run checks
   - If new issues, go to step 2
   - If clean, proceed

4. **Final Review**
   - Run full test suite
   - Check coverage
   - Commit changes
```

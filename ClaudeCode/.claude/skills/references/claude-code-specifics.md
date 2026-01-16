# Claude Code Specific Guidelines

## Environment Differences: Claude Code vs Claude.ai

Understanding these differences is crucial for effective skill design.

### Filesystem Access

| Claude.ai | Claude Code |
|-----------|-------------|
| Sandboxed `/mnt/` directories | Full filesystem access |
| User uploads to `/mnt/user-data/uploads/` | Direct project directory access |
| Output to `/mnt/user-data/outputs/` | Write anywhere user has permission |
| No access to user's actual files | Access to real codebase |

**Implication for Skills:**
- Claude Code skills can read/modify actual project files
- No need to copy files between directories
- Can traverse entire project structure
- Must be careful with destructive operations

### System Tool Access

| Claude.ai | Claude Code |
|-----------|-------------|
| Limited container tools | Full system access |
| Isolated from host | Runs on user's machine |
| Pre-installed packages only | Can install packages |
| No git operations | Full git access |

**Available in Claude Code:**
```bash
# Version control
git status, git commit, git push, git log

# Package managers
npm, yarn, pip, poetry, cargo, go

# Build tools
make, cmake, gradle, maven

# Utilities
grep, find, sed, awk, curl, jq
```

### Project Context

Claude Code has access to:

1. **Project Structure**
   - All files and directories
   - Hidden files (`.env`, `.gitignore`)
   - Configuration files

2. **Git History**
   - Commit history
   - Branch information
   - Uncommitted changes

3. **Dependencies**
   - `package.json` / `node_modules`
   - `requirements.txt` / virtual environments
   - Lock files

4. **Runtime Environment**
   - Environment variables (be careful!)
   - Installed tools
   - System configuration

## Best Practices for Claude Code Skills

### 1. Project Detection

Always detect project type before acting:

```markdown
## Project Detection

Before proceeding, identify the project:

1. Check for `package.json` → Node.js
   - Look at `scripts` for available commands
   - Check `dependencies` for frameworks

2. Check for `pyproject.toml` or `requirements.txt` → Python
   - Identify Python version requirements
   - Check for virtual environment

3. Check for `.git/` → Git-enabled
   - Review recent commits for context
   - Check current branch
```

### 2. Preserve User's Style

Match existing code conventions:

```markdown
## Style Preservation

Before generating code:

1. **Analyze existing code**
   - Indentation (tabs vs spaces, width)
   - Quote style (single vs double)
   - Naming conventions

2. **Check for config files**
   - `.prettierrc` / `.eslintrc`
   - `pyproject.toml` (black/ruff settings)
   - `.editorconfig`

3. **Match the style**
   - Use same patterns as existing code
   - Don't introduce new conventions
```

### 3. Non-Destructive Operations

Protect user's work:

```markdown
## Safety Guidelines

NEVER:
- Delete files without confirmation
- Overwrite without backup
- Modify `.env` files directly
- Push to remote without permission

ALWAYS:
- Show what will change before changing
- Create backups for significant modifications
- Stage changes for review when possible
- Respect `.gitignore` patterns
```

### 4. Use Git Appropriately

Leverage version control:

```markdown
## Git Integration

When modifying files:

1. **Check status first**
   ```bash
   git status
   ```
   - Don't create conflicts with uncommitted changes

2. **Create a branch for significant changes**
   ```bash
   git checkout -b feature/skill-changes
   ```

3. **Commit with clear messages**
   ```bash
   git commit -m "type(scope): description"
   ```

4. **Never force push**
   - Let user handle merge conflicts
```

### 5. Handle Secrets Carefully

```markdown
## Secret Handling

NEVER:
- Log or display API keys, passwords, tokens
- Commit secrets to git
- Store secrets in plain text files

WHEN secrets are needed:
- Reference environment variables
- Point to `.env` files (don't read them)
- Use secret managers when available
```

## Skill-Specific Patterns

### For Code Generation Skills

```markdown
## Code Generation

1. **Detect language/framework first**
2. **Check for existing patterns** in codebase
3. **Generate in user's style**
4. **Add to appropriate location** (don't create new structure)
5. **Update imports/exports** as needed
```

### For Refactoring Skills

```markdown
## Refactoring

1. **Run existing tests first** (establish baseline)
2. **Make atomic changes** (one refactor at a time)
3. **Run tests after each change**
4. **Commit incrementally** with clear messages
5. **Don't change behavior** (only structure)
```

### For Testing Skills

```markdown
## Testing

1. **Detect test framework** (jest, pytest, etc.)
2. **Follow existing test patterns**
3. **Place tests in correct location**
4. **Use appropriate fixtures/mocks**
5. **Verify tests pass** before finishing
```

### For Documentation Skills

```markdown
## Documentation

1. **Check existing docs** format and style
2. **Update, don't duplicate**
3. **Keep docs near code** when appropriate
4. **Link to related docs**
5. **Use relative paths** for internal links
```

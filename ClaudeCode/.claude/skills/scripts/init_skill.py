#!/usr/bin/env python3
"""
Claude Code Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-api-skill --path ./skills
    init_skill.py git-helper --path ~/claude-code-skills
"""

import sys
import os
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: What the skill does AND when to use it. Include specific triggers - file types, commands, tasks. Example: "Python testing automation. Use when writing tests, running test suites, or setting up pytest configurations."]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables in Claude Code]

## Quick Start

[TODO: Most common usage pattern - what users will do 80% of the time]

## Workflow

[TODO: Choose appropriate structure:

**Workflow-Based** (sequential processes):
```
1. Detect project type
2. Run initialization
3. Configure settings
4. Verify setup
```

**Task-Based** (different operations):
```
## Creating [X]
...
## Modifying [X]
...
## Debugging [X]
...
```

**Decision Tree** (branching logic):
```
**New project?** → Run scripts/init.py
**Existing project?** → Follow modification steps below
**Debugging?** → See references/debug.md
```

Delete this guidance section when done.]

## Project Detection

[TODO: How to detect when this skill applies:
- Check for specific files (package.json, pyproject.toml, etc.)
- Check for directory patterns
- Check for git status
- Infer from user's request]

## Scripts

[TODO: Document each script in scripts/ directory:

### scripts/example.py
Purpose: [what it does]
Usage: `python scripts/example.py [args]`
Output: [what it produces]

Delete if no scripts needed.]

## References

[TODO: Document reference files:

- **references/patterns.md**: Common patterns and examples
- **references/troubleshooting.md**: Error handling guide

Delete if no references needed.]

## Assets

[TODO: Document asset files/templates:

- **assets/template/**: Project boilerplate
  - Copy to user's project directory
  - Customize based on project needs

Delete if no assets needed.]

---

**Cleanup:** Delete any unused directories (scripts/, references/, assets/) and this line.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example script for {skill_name}

This script demonstrates Claude Code skill patterns:
- Direct filesystem access (no sandbox)
- System tool integration
- Project context awareness

Usage:
    python scripts/example.py [options]

Replace or delete this file based on skill needs.
"""

import argparse
import subprocess
from pathlib import Path


def detect_project_type(path: Path) -> str:
    """Detect the type of project based on config files."""
    if (path / "package.json").exists():
        return "nodejs"
    elif (path / "pyproject.toml").exists() or (path / "requirements.txt").exists():
        return "python"
    elif (path / "Cargo.toml").exists():
        return "rust"
    elif (path / "go.mod").exists():
        return "go"
    return "unknown"


def run_command(cmd: list[str], cwd: Path = None) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description="{skill_title} helper script")
    parser.add_argument("--path", type=Path, default=Path.cwd(),
                       help="Project path (default: current directory)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    args = parser.parse_args()

    project_path = args.path.resolve()
    
    if not project_path.exists():
        print(f"❌ Path does not exist: {{project_path}}")
        return 1

    project_type = detect_project_type(project_path)
    print(f"📁 Project path: {{project_path}}")
    print(f"🔍 Detected type: {{project_type}}")

    # TODO: Add actual skill logic here
    print("✅ Example script completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

EXAMPLE_REFERENCE = """# {skill_title} Reference

## Common Patterns

[TODO: Add patterns specific to this skill domain]

### Pattern 1: [Name]

**When to use:** [scenario]

**Implementation:**
```
[code or steps]
```

### Pattern 2: [Name]

**When to use:** [scenario]

**Implementation:**
```
[code or steps]
```

## Troubleshooting

### Issue: [Common problem]
**Solution:** [How to fix]

### Issue: [Another problem]
**Solution:** [How to fix]

## Best Practices

1. [Practice 1]
2. [Practice 2]
3. [Practice 3]
"""

EXAMPLE_ASSET = """# {skill_title} Template

This is a placeholder template file.

Replace with actual template content:
- Configuration files
- Boilerplate code
- Project scaffolding

Example uses:
- `.env.template` for environment variables
- `config.yaml.template` for configuration
- Project directory structure

Delete this file if no assets are needed.
"""


def title_case_skill_name(skill_name: str) -> str:
    """Convert kebab-case skill name to Title Case."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def validate_skill_name(name: str) -> tuple[bool, str]:
    """Validate skill name format."""
    import re
    
    if not name:
        return False, "Skill name cannot be empty"
    
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Name must be kebab-case (lowercase letters, digits, hyphens only)"
    
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, "Name cannot start/end with hyphen or contain consecutive hyphens"
    
    if len(name) > 64:
        return False, f"Name too long ({len(name)} chars). Maximum is 64 characters."
    
    return True, "Valid"


def init_skill(skill_name: str, path: str) -> Path | None:
    """
    Initialize a new Claude Code skill directory.
    
    Args:
        skill_name: Name of the skill (kebab-case)
        path: Parent directory for the skill
        
    Returns:
        Path to created skill directory, or None if error
    """
    # Validate skill name
    valid, message = validate_skill_name(skill_name)
    if not valid:
        print(f"❌ Invalid skill name: {message}")
        return None
    
    # Resolve paths
    skill_dir = Path(path).expanduser().resolve() / skill_name
    
    # Check if already exists
    if skill_dir.exists():
        print(f"❌ Directory already exists: {skill_dir}")
        return None
    
    # Create directory structure
    try:
        skill_dir.mkdir(parents=True)
        print(f"✅ Created: {skill_dir}")
    except Exception as e:
        print(f"❌ Failed to create directory: {e}")
        return None
    
    skill_title = title_case_skill_name(skill_name)
    
    # Create SKILL.md
    try:
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(SKILL_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title
        ))
        print("✅ Created: SKILL.md")
    except Exception as e:
        print(f"❌ Failed to create SKILL.md: {e}")
        return None
    
    # Create scripts/ with example
    try:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        example_script = scripts_dir / "example.py"
        example_script.write_text(EXAMPLE_SCRIPT.format(
            skill_name=skill_name,
            skill_title=skill_title
        ))
        example_script.chmod(0o755)
        print("✅ Created: scripts/example.py")
    except Exception as e:
        print(f"❌ Failed to create scripts/: {e}")
    
    # Create references/ with example
    try:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        example_ref = refs_dir / "patterns.md"
        example_ref.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ Created: references/patterns.md")
    except Exception as e:
        print(f"❌ Failed to create references/: {e}")
    
    # Create assets/ with example
    try:
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir()
        example_asset = assets_dir / "template.txt"
        example_asset.write_text(EXAMPLE_ASSET.format(skill_title=skill_title))
        print("✅ Created: assets/template.txt")
    except Exception as e:
        print(f"❌ Failed to create assets/: {e}")
    
    # Print summary
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ Skill '{skill_name}' initialized successfully!           
╠══════════════════════════════════════════════════════════════╣
║  Location: {skill_dir}
╠══════════════════════════════════════════════════════════════╣
║  Next Steps:                                                 
║  1. Edit SKILL.md - complete TODO items                      
║  2. Customize or delete example files                        
║  3. Add your scripts, references, and assets                 
║  4. Run package_skill.py when ready                          
╚══════════════════════════════════════════════════════════════╝
""")
    
    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("""
Claude Code Skill Initializer

Usage:
    init_skill.py <skill-name> --path <directory>

Arguments:
    skill-name    Kebab-case name (e.g., 'python-api', 'git-helper')
    --path        Parent directory for the skill

Examples:
    init_skill.py my-api-skill --path ./skills
    init_skill.py git-helper --path ~/claude-code-skills
    init_skill.py data-pipeline --path /projects/skills

Naming Rules:
    - Lowercase letters, digits, and hyphens only
    - No leading/trailing hyphens
    - No consecutive hyphens
    - Maximum 64 characters
""")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    path = sys.argv[3]
    
    print(f"🚀 Initializing Claude Code skill: {skill_name}")
    print(f"   Path: {path}\n")
    
    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()

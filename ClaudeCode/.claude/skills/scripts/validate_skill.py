#!/usr/bin/env python3
"""
Claude Code Skill Validator - Validates skill structure and content

Usage:
    validate_skill.py <skill-folder>

Examples:
    validate_skill.py ./my-skill
    validate_skill.py ~/skills/python-api
"""

import sys
import re
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """
    Parse YAML frontmatter from SKILL.md content.
    
    Returns:
        Tuple of (frontmatter_dict, error_message)
    """
    if not content.startswith('---'):
        return None, "No YAML frontmatter found (must start with ---)"
    
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format (missing closing ---)"
    
    frontmatter_text = match.group(1)
    
    if HAS_YAML:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return None, "Frontmatter must be a YAML dictionary"
            return frontmatter, ""
        except yaml.YAMLError as e:
            return None, f"Invalid YAML: {e}"
    else:
        # Basic parsing without yaml library
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, _, value = line.partition(':')
                frontmatter[key.strip()] = value.strip()
        return frontmatter, ""


def validate_skill(skill_path: str | Path) -> tuple[bool, list[str], list[str]]:
    """
    Validate a Claude Code skill.
    
    Args:
        skill_path: Path to skill directory
        
    Returns:
        Tuple of (is_valid, error_list, warning_list)
    """
    errors = []
    warnings = []
    skill_path = Path(skill_path).expanduser().resolve()
    
    # Check skill directory exists
    if not skill_path.exists():
        return False, ["Skill directory does not exist"], []
    
    if not skill_path.is_dir():
        return False, ["Path is not a directory"], []
    
    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md not found"], []
    
    # Read and parse SKILL.md
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Cannot read SKILL.md: {e}"], []
    
    # Parse frontmatter
    frontmatter, error = parse_frontmatter(content)
    if error:
        errors.append(error)
        return False, errors, warnings
    
    # Validate allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        errors.append(f"Unexpected frontmatter keys: {', '.join(sorted(unexpected))}")
    
    # Validate name
    name = frontmatter.get('name', '')
    if not name:
        errors.append("Missing 'name' in frontmatter")
    elif not isinstance(name, str):
        errors.append(f"'name' must be a string, got {type(name).__name__}")
    else:
        name = name.strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"Name '{name}' must be kebab-case (lowercase, digits, hyphens)")
        if name.startswith('-') or name.endswith('-') or '--' in name:
            errors.append(f"Name '{name}' has invalid hyphen usage")
        if len(name) > 64:
            errors.append(f"Name too long ({len(name)} chars, max 64)")
        
        # Check name matches directory
        if name != skill_path.name:
            warnings.append(f"Name '{name}' doesn't match directory '{skill_path.name}'")
    
    # Validate description
    description = frontmatter.get('description', '')
    if not description:
        errors.append("Missing 'description' in frontmatter")
    elif not isinstance(description, str):
        errors.append(f"'description' must be a string, got {type(description).__name__}")
    else:
        description = description.strip()
        if '<' in description or '>' in description:
            errors.append("Description cannot contain angle brackets (< or >)")
        if len(description) > 1024:
            errors.append(f"Description too long ({len(description)} chars, max 1024)")
        if '[TODO' in description:
            errors.append("Description contains TODO placeholder")
        if len(description) < 50:
            warnings.append("Description seems short - include what AND when to use")
    
    # Check body content
    body_start = content.find('---', 3)
    if body_start != -1:
        body = content[body_start + 3:].strip()
        
        # Count lines
        line_count = len(body.split('\n'))
        if line_count > 500:
            warnings.append(f"SKILL.md body is {line_count} lines (recommended <500)")
        
        # Check for TODO placeholders
        if '[TODO' in body:
            warnings.append("Body contains TODO placeholders")
    
    # Check referenced files exist
    # Look for markdown links like [text](path)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for match in link_pattern.finditer(content):
        link_path = match.group(2)
        # Skip URLs and anchors
        if link_path.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
        
        # Check if referenced file exists
        ref_path = skill_path / link_path
        if not ref_path.exists():
            warnings.append(f"Referenced file not found: {link_path}")
    
    # Check for common unnecessary files
    unnecessary = ['README.md', 'CHANGELOG.md', 'INSTALLATION_GUIDE.md', 'CONTRIBUTING.md']
    for fname in unnecessary:
        if (skill_path / fname).exists():
            warnings.append(f"Unnecessary file: {fname} (SKILL.md should be the only documentation)")
    
    # Check scripts are executable
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            # Check for shebang
            try:
                first_line = script.read_text().split('\n')[0]
                if not first_line.startswith('#!'):
                    warnings.append(f"Script missing shebang: {script.name}")
            except:
                pass
    
    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    if len(sys.argv) != 2:
        print("""
Claude Code Skill Validator

Usage:
    validate_skill.py <skill-folder>

Examples:
    validate_skill.py ./my-skill
    validate_skill.py ~/skills/python-api

Checks:
    • SKILL.md exists and has valid frontmatter
    • name: kebab-case, ≤64 chars, matches directory
    • description: present, ≤1024 chars, no angle brackets
    • No TODO placeholders in frontmatter
    • Referenced files exist
    • No unnecessary documentation files
    • Scripts have shebangs
""")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    print(f"🔍 Validating: {skill_path}\n")
    
    valid, errors, warnings = validate_skill(skill_path)
    
    # Print warnings
    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"   • {w}")
        print()
    
    # Print errors
    if errors:
        print("❌ Errors:")
        for e in errors:
            print(f"   • {e}")
        print()
    
    # Summary
    if valid:
        if warnings:
            print("✅ Skill is valid (with warnings)")
        else:
            print("✅ Skill is valid!")
        sys.exit(0)
    else:
        print("❌ Skill validation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

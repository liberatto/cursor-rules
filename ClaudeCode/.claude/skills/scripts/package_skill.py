#!/usr/bin/env python3
"""
Claude Code Skill Packager - Creates distributable .skill files

Usage:
    package_skill.py <skill-folder> [output-directory]

Examples:
    package_skill.py ./my-skill
    package_skill.py ./my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path

# Import validation from same directory
from validate_skill import validate_skill


def package_skill(skill_path: str, output_dir: str = None) -> Path | None:
    """
    Package a skill folder into a .skill file (zip format).
    
    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory (default: current directory)
        
    Returns:
        Path to created .skill file, or None if error
    """
    skill_path = Path(skill_path).expanduser().resolve()
    
    # Validate path exists
    if not skill_path.exists():
        print(f"❌ Skill folder not found: {skill_path}")
        return None
    
    if not skill_path.is_dir():
        print(f"❌ Not a directory: {skill_path}")
        return None
    
    # Check for SKILL.md
    if not (skill_path / "SKILL.md").exists():
        print(f"❌ SKILL.md not found in {skill_path}")
        return None
    
    # Run validation
    print("🔍 Validating skill...")
    valid, errors, warnings = validate_skill(skill_path)
    
    # Show warnings
    for warning in warnings:
        print(f"⚠️  {warning}")
    
    # Check for errors
    if not valid:
        print("❌ Validation failed:")
        for error in errors:
            print(f"   • {error}")
        print("\nFix errors before packaging.")
        return None
    
    print("✅ Validation passed\n")
    
    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        out_path = Path(output_dir).expanduser().resolve()
        out_path.mkdir(parents=True, exist_ok=True)
    else:
        out_path = Path.cwd()
    
    skill_file = out_path / f"{skill_name}.skill"
    
    # Create .skill file (zip format)
    try:
        print(f"📦 Packaging skill...")
        
        with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            file_count = 0
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Skip common unwanted files
                    if file_path.name.startswith('.'):
                        continue
                    if file_path.name == '__pycache__':
                        continue
                    if file_path.suffix == '.pyc':
                        continue
                    
                    # Archive with relative path from skill folder's parent
                    arcname = file_path.relative_to(skill_path.parent)
                    zf.write(file_path, arcname)
                    print(f"   + {arcname}")
                    file_count += 1
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ Skill packaged successfully!                             
╠══════════════════════════════════════════════════════════════╣
║  Output: {skill_file}
║  Files:  {file_count} files included
╠══════════════════════════════════════════════════════════════╣
║  Distribution:                                               
║  • Share the .skill file directly                            
║  • Extract with: unzip {skill_name}.skill                    
║  • The .skill file is a standard ZIP archive                 
╚══════════════════════════════════════════════════════════════╝
""")
        return skill_file
        
    except Exception as e:
        print(f"❌ Packaging failed: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("""
Claude Code Skill Packager

Usage:
    package_skill.py <skill-folder> [output-directory]

Arguments:
    skill-folder      Path to the skill directory
    output-directory  Optional output location (default: current directory)

Examples:
    package_skill.py ./my-skill
    package_skill.py ./my-skill ./dist
    package_skill.py ~/skills/python-api /tmp

Output:
    Creates a .skill file (ZIP format) containing the skill.
    The file can be shared and extracted with standard tools.
""")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"📦 Packaging: {skill_path}")
    if output_dir:
        print(f"   Output: {output_dir}")
    print()
    
    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()

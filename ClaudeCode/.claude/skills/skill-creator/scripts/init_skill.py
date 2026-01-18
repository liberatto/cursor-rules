#!/usr/bin/env python3
"""
Claude Code Skill Initializer (v2.1+)

새로운 skill을 v2.1 스펙에 맞게 초기화합니다.

Usage:
    init_skill.py <skill-name> --path <path> [options]

Options:
    --context fork          # Fork 컨텍스트 사용
    --agent <type>          # 에이전트 타입 (Explore, Plan, general-purpose)
    --tools <tools>         # 허용 도구 (쉼표 구분)
    --no-menu               # 슬래시 메뉴에서 숨김
    --with-hooks            # Hooks 템플릿 포함

Examples:
    init_skill.py code-review --path ./skills
    init_skill.py api-generator --path ~/.claude/skills --context fork --agent Explore
    init_skill.py git-helper --path ./skills --tools "Read,Grep,Bash(git *)" --with-hooks
"""

import sys
import os
import argparse
from pathlib import Path


def get_skill_template(
    skill_name: str,
    skill_title: str,
    context: str = None,
    agent: str = None,
    allowed_tools: list = None,
    user_invocable: bool = True,
    with_hooks: bool = False
) -> str:
    """v2.1 스펙에 맞는 SKILL.md 템플릿 생성"""

    # Frontmatter 구성
    frontmatter_lines = [
        "---",
        f"name: {skill_name}",
        "description: |",
        "  [TODO: 스킬이 하는 일을 설명하세요.]",
        "  [TODO: 트리거 키워드를 포함하세요. 예: \"코드 리뷰\", \"PR 검토\", \"보안 검사\"]",
    ]

    # 선택적 필드 추가
    if context:
        frontmatter_lines.append(f"context: {context}")

    if agent:
        frontmatter_lines.append(f"agent: {agent}")

    if allowed_tools:
        frontmatter_lines.append("allowed-tools:")
        for tool in allowed_tools:
            frontmatter_lines.append(f"  - {tool.strip()}")

    if not user_invocable:
        frontmatter_lines.append("user-invocable: false")

    if with_hooks:
        frontmatter_lines.extend([
            "hooks:",
            "  PreToolUse:",
            "    - matcher: \"Bash\"",
            "      hooks:",
            "        - type: command",
            "          command: \"./scripts/validate.sh\"",
            "          once: true",
            "  # PostToolUse:",
            "  #   - matcher: \"Write|Edit\"",
            "  #     hooks:",
            "  #       - type: command",
            "  #         command: \"./scripts/lint.sh\"",
            "  # Stop:",
            "  #   - type: command",
            "  #     command: \"./scripts/cleanup.sh\"",
        ])

    frontmatter_lines.append("---")

    # Body 구성
    body = f"""
# {skill_title}

## 개요

[TODO: 1-2문장으로 이 스킬이 무엇을 하는지 설명]

## Quick Start

[TODO: 가장 일반적인 사용 패턴 - 80%의 경우에 사용할 내용]

## 워크플로우

[TODO: 적절한 구조 선택:

**순차적 워크플로우**:
1. 프로젝트 타입 감지
2. 초기화 실행
3. 설정 구성
4. 완료 확인

**작업 기반**:
## [X] 생성
...
## [X] 수정
...

**결정 트리**:
- 새 프로젝트? → scripts/init.py 실행
- 기존 프로젝트? → 아래 수정 단계 따름

이 가이드 섹션 삭제 후 사용]

## 프로젝트 감지

[TODO: 이 스킬이 적용되는 시점 감지 방법:
- 특정 파일 확인 (package.json, pyproject.toml 등)
- 디렉토리 패턴 확인
- git 상태 확인]

## 스크립트

[TODO: scripts/ 디렉토리의 각 스크립트 문서화:

### scripts/example.py
용도: [기능 설명]
사용: `python scripts/example.py [args]`
출력: [생성물]

스크립트 불필요 시 이 섹션과 scripts/ 폴더 삭제]

## 참고 문서

[TODO: 참조 파일 문서화:

- **references/patterns.md**: 일반 패턴 및 예시
- **references/troubleshooting.md**: 오류 처리 가이드

참조 파일 불필요 시 이 섹션과 references/ 폴더 삭제]

---

**정리:** 사용하지 않는 디렉토리(scripts/, references/, assets/)와 이 줄을 삭제하세요.
"""

    return "\n".join(frontmatter_lines) + body


EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_title} 헬퍼 스크립트

Claude Code skill 패턴 예시:
- 직접 파일시스템 접근 (샌드박스 없음)
- 시스템 도구 통합
- 프로젝트 컨텍스트 인식

Usage:
    python scripts/example.py [options]

필요에 따라 이 파일을 수정하거나 삭제하세요.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def detect_project_type(path: Path) -> str:
    """설정 파일 기반 프로젝트 타입 감지"""
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
    """쉘 명령 실행 후 (returncode, stdout, stderr) 반환"""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description="{skill_title} 헬퍼 스크립트")
    parser.add_argument("--path", type=Path, default=Path.cwd(),
                       help="프로젝트 경로 (기본: 현재 디렉토리)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="상세 출력")
    args = parser.parse_args()

    project_path = args.path.resolve()

    if not project_path.exists():
        print(f"❌ 경로가 존재하지 않습니다: {{project_path}}")
        return 1

    project_type = detect_project_type(project_path)
    print(f"📁 프로젝트 경로: {{project_path}}")
    print(f"🔍 감지된 타입: {{project_type}}")

    # TODO: 실제 스킬 로직 추가
    print("✅ 예제 스크립트 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


VALIDATE_SCRIPT = '''#!/bin/bash
# PreToolUse hook 검증 스크립트 예시
# 이 스크립트는 도구 실행 전에 호출됩니다

# 예시: 특정 명령어 차단
# if [[ "$1" == *"rm -rf"* ]]; then
#     echo "❌ 위험한 명령어가 차단되었습니다"
#     exit 1
# fi

# 예시: 로깅
# echo "[$(date)] Tool called: $1" >> /tmp/skill-audit.log

exit 0
'''


EXAMPLE_REFERENCE = """# {skill_title} 참고 문서

## 일반 패턴

[TODO: 이 스킬 도메인에 특화된 패턴 추가]

### 패턴 1: [이름]

**사용 시점:** [시나리오]

**구현:**
```
[코드 또는 단계]
```

### 패턴 2: [이름]

**사용 시점:** [시나리오]

**구현:**
```
[코드 또는 단계]
```

## 문제 해결

### 문제: [일반적인 문제]
**해결:** [해결 방법]

### 문제: [다른 문제]
**해결:** [해결 방법]

## 모범 사례

1. [사례 1]
2. [사례 2]
3. [사례 3]
"""


def title_case_skill_name(skill_name: str) -> str:
    """kebab-case 스킬 이름을 Title Case로 변환"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def validate_skill_name(name: str) -> tuple[bool, str]:
    """스킬 이름 형식 검증"""
    import re

    if not name:
        return False, "스킬 이름이 비어있습니다"

    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "이름은 kebab-case여야 합니다 (소문자, 숫자, 하이픈만)"

    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, "이름은 하이픈으로 시작/끝나거나 연속 하이픈을 포함할 수 없습니다"

    if len(name) > 64:
        return False, f"이름이 너무 깁니다 ({len(name)}자). 최대 64자입니다."

    return True, "유효함"


def init_skill(
    skill_name: str,
    path: str,
    context: str = None,
    agent: str = None,
    allowed_tools: list = None,
    user_invocable: bool = True,
    with_hooks: bool = False
) -> Path | None:
    """
    새로운 Claude Code skill 디렉토리 초기화 (v2.1)

    Args:
        skill_name: 스킬 이름 (kebab-case)
        path: 스킬의 상위 디렉토리
        context: 컨텍스트 타입 (fork 또는 None)
        agent: 에이전트 타입 (Explore, Plan, general-purpose)
        allowed_tools: 허용 도구 목록
        user_invocable: 슬래시 메뉴 표시 여부
        with_hooks: Hooks 템플릿 포함 여부

    Returns:
        생성된 스킬 디렉토리 경로, 또는 오류 시 None
    """
    # 스킬 이름 검증
    valid, message = validate_skill_name(skill_name)
    if not valid:
        print(f"❌ 잘못된 스킬 이름: {message}")
        return None

    # 경로 확인
    skill_dir = Path(path).expanduser().resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ 디렉토리가 이미 존재합니다: {skill_dir}")
        return None

    # 디렉토리 구조 생성
    try:
        skill_dir.mkdir(parents=True)
        print(f"✅ 생성됨: {skill_dir}")
    except Exception as e:
        print(f"❌ 디렉토리 생성 실패: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)

    # SKILL.md 생성
    try:
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(get_skill_template(
            skill_name=skill_name,
            skill_title=skill_title,
            context=context,
            agent=agent,
            allowed_tools=allowed_tools,
            user_invocable=user_invocable,
            with_hooks=with_hooks
        ))
        print("✅ 생성됨: SKILL.md")
    except Exception as e:
        print(f"❌ SKILL.md 생성 실패: {e}")
        return None

    # scripts/ 생성
    try:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()

        # 메인 스크립트
        example_script = scripts_dir / "example.py"
        example_script.write_text(EXAMPLE_SCRIPT.format(
            skill_name=skill_name,
            skill_title=skill_title
        ))
        example_script.chmod(0o755)
        print("✅ 생성됨: scripts/example.py")

        # Hooks 사용 시 검증 스크립트 추가
        if with_hooks:
            validate_script = scripts_dir / "validate.sh"
            validate_script.write_text(VALIDATE_SCRIPT)
            validate_script.chmod(0o755)
            print("✅ 생성됨: scripts/validate.sh")
    except Exception as e:
        print(f"❌ scripts/ 생성 실패: {e}")

    # references/ 생성
    try:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        example_ref = refs_dir / "patterns.md"
        example_ref.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ 생성됨: references/patterns.md")
    except Exception as e:
        print(f"❌ references/ 생성 실패: {e}")

    # 설정 요약
    config_summary = []
    if context:
        config_summary.append(f"context: {context}")
    if agent:
        config_summary.append(f"agent: {agent}")
    if allowed_tools:
        config_summary.append(f"allowed-tools: {', '.join(allowed_tools)}")
    if not user_invocable:
        config_summary.append("user-invocable: false")
    if with_hooks:
        config_summary.append("hooks: enabled")

    config_str = ", ".join(config_summary) if config_summary else "기본 설정"

    # 완료 메시지
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  ✅ Skill '{skill_name}' 초기화 완료! (v2.1)
╠══════════════════════════════════════════════════════════════════╣
║  위치: {skill_dir}
║  설정: {config_str}
╠══════════════════════════════════════════════════════════════════╣
║  다음 단계:
║  1. SKILL.md의 TODO 항목 완성
║  2. 예제 파일 수정 또는 삭제
║  3. 스크립트, 참조문서, 에셋 추가
║  4. validate_skill.py로 검증
╠══════════════════════════════════════════════════════════════════╣
║  v2.1 팁:
║  - Hot-Reload: 스킬 수정 시 세션 재시작 불필요
║  - /context: 로드된 스킬 확인
║  - 중첩 디렉토리의 스킬도 자동 발견됨
╚══════════════════════════════════════════════════════════════════╝
""")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Skill Initializer (v2.1+)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    %(prog)s code-review --path ./skills
    %(prog)s api-gen --path ~/.claude/skills --context fork --agent Explore
    %(prog)s git-helper --path ./skills --tools "Read,Grep,Bash(git *)" --with-hooks

v2.1 새 기능:
    --context fork      독립된 서브에이전트에서 실행
    --agent <type>      특정 에이전트 타입 사용
    --with-hooks        PreToolUse/PostToolUse/Stop 훅 템플릿 포함
"""
    )

    parser.add_argument("skill_name", help="스킬 이름 (kebab-case)")
    parser.add_argument("--path", required=True, help="스킬 상위 디렉토리")
    parser.add_argument("--context", choices=["fork"], help="컨텍스트 타입")
    parser.add_argument("--agent", choices=["Explore", "Plan", "general-purpose"],
                       help="에이전트 타입 (context: fork와 함께 사용)")
    parser.add_argument("--tools", help="허용 도구 목록 (쉼표 구분)")
    parser.add_argument("--no-menu", action="store_true",
                       help="슬래시 메뉴에서 숨김 (user-invocable: false)")
    parser.add_argument("--with-hooks", action="store_true",
                       help="Hooks 템플릿 포함")

    args = parser.parse_args()

    # 도구 목록 파싱
    allowed_tools = None
    if args.tools:
        allowed_tools = [t.strip() for t in args.tools.split(",")]

    print(f"🚀 Claude Code skill 초기화 중: {args.skill_name}")
    print(f"   경로: {args.path}")
    if args.context:
        print(f"   컨텍스트: {args.context}")
    if args.agent:
        print(f"   에이전트: {args.agent}")
    if allowed_tools:
        print(f"   허용 도구: {', '.join(allowed_tools)}")
    print()

    result = init_skill(
        skill_name=args.skill_name,
        path=args.path,
        context=args.context,
        agent=args.agent,
        allowed_tools=allowed_tools,
        user_invocable=not args.no_menu,
        with_hooks=args.with_hooks
    )

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()

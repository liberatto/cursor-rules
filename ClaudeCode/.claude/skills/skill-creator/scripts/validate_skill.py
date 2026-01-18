#!/usr/bin/env python3
"""
Claude Code Skill Validator (v2.1+)

스킬 구조와 내용을 v2.1 스펙에 맞게 검증합니다.

Usage:
    validate_skill.py <skill-folder>

Examples:
    validate_skill.py ./my-skill
    validate_skill.py ~/.claude/skills/code-review
"""

import sys
import re
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# v2.1 허용 속성
ALLOWED_PROPERTIES = {
    'name',           # 필수
    'description',    # 필수
    'context',        # 선택: fork
    'agent',          # 선택: Explore, Plan, general-purpose
    'allowed-tools',  # 선택: 도구 목록
    'user-invocable', # 선택: boolean
    'hooks',          # 선택: PreToolUse, PostToolUse, Stop
    'model',          # 선택: sonnet, opus, haiku, inherit
    'license',        # 선택: 라이선스 정보
    'metadata',       # 선택: 추가 메타데이터
}

VALID_CONTEXTS = {'fork'}
VALID_AGENTS = {'Explore', 'Plan', 'general-purpose'}
VALID_MODELS = {'sonnet', 'opus', 'haiku', 'inherit', 'claude-opus-4-5', 'claude-sonnet-4'}
VALID_HOOK_TYPES = {'PreToolUse', 'PostToolUse', 'Stop'}


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """
    SKILL.md에서 YAML frontmatter 파싱

    Returns:
        (frontmatter_dict, error_message) 튜플
    """
    if not content.startswith('---'):
        return None, "YAML frontmatter가 없습니다 (---로 시작해야 함)"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, "잘못된 frontmatter 형식 (닫는 --- 누락)"

    frontmatter_text = match.group(1)

    if HAS_YAML:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return None, "Frontmatter는 YAML 딕셔너리여야 합니다"
            return frontmatter, ""
        except yaml.YAMLError as e:
            return None, f"잘못된 YAML: {e}"
    else:
        # yaml 라이브러리 없을 때 기본 파싱
        frontmatter = {}
        current_key = None
        for line in frontmatter_text.split('\n'):
            if ':' in line and not line.startswith(' '):
                key, _, value = line.partition(':')
                current_key = key.strip()
                frontmatter[current_key] = value.strip()
        return frontmatter, ""


def validate_hooks(hooks: dict, errors: list, warnings: list):
    """Hooks 설정 검증"""
    if not isinstance(hooks, dict):
        errors.append("hooks는 딕셔너리여야 합니다")
        return

    for hook_type, hook_list in hooks.items():
        if hook_type not in VALID_HOOK_TYPES:
            errors.append(f"잘못된 hook 타입: {hook_type} (허용: {', '.join(VALID_HOOK_TYPES)})")
            continue

        if not isinstance(hook_list, list):
            errors.append(f"{hook_type}: hook 목록이 리스트여야 합니다")
            continue

        for i, hook_entry in enumerate(hook_list):
            if not isinstance(hook_entry, dict):
                errors.append(f"{hook_type}[{i}]: hook 항목이 딕셔너리여야 합니다")
                continue

            # matcher 검증 (PreToolUse, PostToolUse)
            if hook_type in ('PreToolUse', 'PostToolUse'):
                if 'matcher' not in hook_entry:
                    warnings.append(f"{hook_type}[{i}]: matcher가 없습니다")
                else:
                    matcher = hook_entry['matcher']
                    try:
                        re.compile(matcher)
                    except re.error as e:
                        errors.append(f"{hook_type}[{i}]: 잘못된 matcher 정규식: {e}")

            # hooks 내부 검증
            if 'hooks' in hook_entry:
                inner_hooks = hook_entry['hooks']
                if not isinstance(inner_hooks, list):
                    errors.append(f"{hook_type}[{i}]: hooks는 리스트여야 합니다")
                else:
                    for j, inner in enumerate(inner_hooks):
                        if not isinstance(inner, dict):
                            continue
                        if 'type' not in inner:
                            errors.append(f"{hook_type}[{i}].hooks[{j}]: type이 필요합니다")
                        if inner.get('type') == 'command' and 'command' not in inner:
                            errors.append(f"{hook_type}[{i}].hooks[{j}]: command가 필요합니다")


def validate_allowed_tools(tools, errors: list, warnings: list):
    """allowed-tools 검증"""
    if isinstance(tools, str):
        # 쉼표 구분 형식
        tool_list = [t.strip() for t in tools.split(',')]
    elif isinstance(tools, list):
        tool_list = tools
    else:
        errors.append("allowed-tools는 문자열 또는 리스트여야 합니다")
        return

    valid_tools = {
        'Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash', 'Task',
        'WebFetch', 'WebSearch', 'TodoWrite', 'AskUserQuestion',
        'NotebookEdit', 'mcp__*'
    }

    for tool in tool_list:
        if not isinstance(tool, str):
            errors.append(f"도구 이름은 문자열이어야 합니다: {tool}")
            continue

        # Bash(pattern) 형식 검증
        if tool.startswith('Bash(') and tool.endswith(')'):
            pattern = tool[5:-1]
            if not pattern:
                warnings.append(f"빈 Bash 패턴: {tool}")
        elif '(' in tool or ')' in tool:
            if not tool.startswith('Bash('):
                warnings.append(f"잘못된 도구 패턴 형식: {tool}")


def validate_skill(skill_path: str | Path) -> tuple[bool, list[str], list[str]]:
    """
    Claude Code skill 검증 (v2.1)

    Args:
        skill_path: 스킬 디렉토리 경로

    Returns:
        (is_valid, error_list, warning_list) 튜플
    """
    errors = []
    warnings = []
    skill_path = Path(skill_path).expanduser().resolve()

    # 디렉토리 존재 확인
    if not skill_path.exists():
        return False, ["스킬 디렉토리가 존재하지 않습니다"], []

    if not skill_path.is_dir():
        return False, ["경로가 디렉토리가 아닙니다"], []

    # SKILL.md 존재 확인
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md를 찾을 수 없습니다"], []

    # SKILL.md 읽기
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"SKILL.md 읽기 실패: {e}"], []

    # Frontmatter 파싱
    frontmatter, error = parse_frontmatter(content)
    if error:
        errors.append(error)
        return False, errors, warnings

    # 허용되지 않은 속성 확인
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        errors.append(f"알 수 없는 frontmatter 키: {', '.join(sorted(unexpected))}")

    # === 필수 필드 검증 ===

    # name 검증
    name = frontmatter.get('name', '')
    if not name:
        errors.append("'name' 필드가 없습니다")
    elif not isinstance(name, str):
        errors.append(f"'name'은 문자열이어야 합니다, 현재: {type(name).__name__}")
    else:
        name = name.strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"이름 '{name}'은 kebab-case여야 합니다 (소문자, 숫자, 하이픈)")
        if name.startswith('-') or name.endswith('-') or '--' in name:
            errors.append(f"이름 '{name}'의 하이픈 사용이 잘못되었습니다")
        if len(name) > 64:
            errors.append(f"이름이 너무 깁니다 ({len(name)}자, 최대 64자)")

        # 디렉토리 이름과 일치 확인
        if name != skill_path.name:
            warnings.append(f"이름 '{name}'이 디렉토리 '{skill_path.name}'과 다릅니다")

    # description 검증
    description = frontmatter.get('description', '')
    if not description:
        errors.append("'description' 필드가 없습니다")
    elif not isinstance(description, str):
        errors.append(f"'description'은 문자열이어야 합니다, 현재: {type(description).__name__}")
    else:
        description = description.strip()
        if '<' in description or '>' in description:
            errors.append("description에 꺾쇠 괄호(< >)를 사용할 수 없습니다")
        if len(description) > 1024:
            errors.append(f"description이 너무 깁니다 ({len(description)}자, 최대 1024자)")
        if '[TODO' in description:
            errors.append("description에 TODO 플레이스홀더가 있습니다")
        if len(description) < 50:
            warnings.append("description이 짧습니다 - 무엇을 하는지와 언제 사용하는지 포함하세요")

    # === 선택 필드 검증 (v2.1) ===

    # context 검증
    context = frontmatter.get('context')
    if context is not None:
        if context not in VALID_CONTEXTS:
            errors.append(f"잘못된 context 값: {context} (허용: {', '.join(VALID_CONTEXTS)})")

    # agent 검증
    agent = frontmatter.get('agent')
    if agent is not None:
        if agent not in VALID_AGENTS:
            errors.append(f"잘못된 agent 값: {agent} (허용: {', '.join(VALID_AGENTS)})")
        if context != 'fork':
            warnings.append("agent는 context: fork와 함께 사용하는 것이 좋습니다")

    # model 검증
    model = frontmatter.get('model')
    if model is not None:
        if model not in VALID_MODELS:
            warnings.append(f"알 수 없는 model 값: {model}")

    # user-invocable 검증
    user_invocable = frontmatter.get('user-invocable')
    if user_invocable is not None:
        if not isinstance(user_invocable, bool):
            errors.append("user-invocable는 boolean이어야 합니다")

    # allowed-tools 검증
    allowed_tools = frontmatter.get('allowed-tools')
    if allowed_tools is not None:
        validate_allowed_tools(allowed_tools, errors, warnings)

    # hooks 검증
    hooks = frontmatter.get('hooks')
    if hooks is not None:
        validate_hooks(hooks, errors, warnings)

    # === Body 검증 ===
    body_start = content.find('---', 3)
    if body_start != -1:
        body = content[body_start + 3:].strip()

        # 줄 수 확인
        line_count = len(body.split('\n'))
        if line_count > 500:
            warnings.append(f"SKILL.md body가 {line_count}줄입니다 (권장: <500줄)")

        # TODO 플레이스홀더 확인
        if '[TODO' in body:
            warnings.append("Body에 TODO 플레이스홀더가 있습니다")

    # === 참조 파일 확인 ===
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for match in link_pattern.finditer(content):
        link_path = match.group(2)
        # URL과 앵커 제외
        if link_path.startswith(('http://', 'https://', '#', 'mailto:')):
            continue

        # 참조 파일 존재 확인
        ref_path = skill_path / link_path
        if not ref_path.exists():
            warnings.append(f"참조 파일을 찾을 수 없습니다: {link_path}")

    # === 불필요한 파일 확인 ===
    unnecessary = ['README.md', 'CHANGELOG.md', 'INSTALLATION_GUIDE.md', 'CONTRIBUTING.md']
    for fname in unnecessary:
        if (skill_path / fname).exists():
            warnings.append(f"불필요한 파일: {fname} (SKILL.md가 유일한 문서여야 합니다)")

    # === 스크립트 검증 ===
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            try:
                first_line = script.read_text().split('\n')[0]
                if not first_line.startswith('#!'):
                    warnings.append(f"스크립트에 shebang이 없습니다: {script.name}")
            except:
                pass

        for script in scripts_dir.glob("*.sh"):
            try:
                first_line = script.read_text().split('\n')[0]
                if not first_line.startswith('#!'):
                    warnings.append(f"스크립트에 shebang이 없습니다: {script.name}")
            except:
                pass

    # === Hooks 스크립트 확인 ===
    if hooks:
        for hook_type, hook_list in hooks.items():
            if not isinstance(hook_list, list):
                continue
            for hook_entry in hook_list:
                if not isinstance(hook_entry, dict):
                    continue
                inner_hooks = hook_entry.get('hooks', [])
                if not isinstance(inner_hooks, list):
                    continue
                for inner in inner_hooks:
                    if not isinstance(inner, dict):
                        continue
                    cmd = inner.get('command', '')
                    if cmd.startswith('./'):
                        script_path = skill_path / cmd[2:]
                        if not script_path.exists():
                            warnings.append(f"Hook 스크립트를 찾을 수 없습니다: {cmd}")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    if len(sys.argv) != 2:
        print("""
Claude Code Skill Validator (v2.1+)

Usage:
    validate_skill.py <skill-folder>

Examples:
    validate_skill.py ./my-skill
    validate_skill.py ~/.claude/skills/code-review

검증 항목:
    • SKILL.md 존재 및 유효한 frontmatter
    • name: kebab-case, ≤64자, 디렉토리 이름 일치
    • description: 필수, ≤1024자, 특수문자 금지
    • context: fork만 허용
    • agent: Explore, Plan, general-purpose만 허용
    • allowed-tools: 유효한 도구 이름
    • hooks: 유효한 hook 타입 및 구조
    • user-invocable: boolean
    • 참조 파일 존재 확인
    • 불필요한 문서 파일 경고
    • 스크립트 shebang 확인
""")
        sys.exit(1)

    skill_path = sys.argv[1]
    print(f"🔍 검증 중: {skill_path}\n")

    valid, errors, warnings = validate_skill(skill_path)

    # 경고 출력
    if warnings:
        print("⚠️  경고:")
        for w in warnings:
            print(f"   • {w}")
        print()

    # 오류 출력
    if errors:
        print("❌ 오류:")
        for e in errors:
            print(f"   • {e}")
        print()

    # 요약
    if valid:
        if warnings:
            print("✅ 스킬이 유효합니다 (경고 있음)")
        else:
            print("✅ 스킬이 유효합니다!")
        sys.exit(0)
    else:
        print("❌ 스킬 검증 실패")
        sys.exit(1)


if __name__ == "__main__":
    main()

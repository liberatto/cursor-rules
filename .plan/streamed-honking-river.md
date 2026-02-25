# Plan: hook-manager env 제거 → registry 방식 전환

## Context

hook-manager 스킬의 enable/disable을 통일(물리 제거+백업)한 후, `settings.json`의 `env` 섹션에 남아있는 `CLAUDE_HOOK_*` 환경변수가 런타임에 아무 역할도 하지 않는 상태가 되었다. env를 제거하고, `.claude/hook-manager-state.json`을 **전체 managed hook의 레지스트리**로 승격시켜 관리 포인트를 단일화한다.

## 변경 대상 파일 (4개)

| 파일 | 변경 |
|------|------|
| `ClaudeCode/.claude/skills/hook-manager/SKILL.md` | 전면 개편 (마스터) |
| `ClaudeCode/.claude/skills/hook-manager/references/hook-recipes.md` | env/래퍼 제거, 레시피 간소화 |
| `.claude/skills/hook-manager/SKILL.md` | 마스터와 동기 (cp) |
| `.claude/skills/hook-manager/references/hook-recipes.md` | 마스터와 동기 (cp) |

## 1. Registry 파일 설계

**파일**: `.claude/hook-manager-registry.json` (이름 변경: state → registry)

```json
{
  "FORMAT": {
    "event": "PostToolUse",
    "matcher": "Edit|Write",
    "status": "enabled",
    "settingsFile": ".claude/settings.local.json",
    "hookEntry": {
      "type": "command",
      "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true",
      "timeout": 30
    }
  },
  "BLOCKDANGER": {
    "event": "PreToolUse",
    "matcher": "Bash",
    "status": "disabled",
    "settingsFile": ".claude/settings.local.json",
    "hookEntry": {
      "type": "command",
      "command": "CMD=$(jq -r '.tool_input.command'); ..."
    }
  }
}
```

- **키**: NAME (사용자 지정 식별자, 대문자)
- **matcher**: 실제 regex 패턴 저장 (matcherIndex 제거 → 복원 시 패턴으로 매칭)
- **status**: `enabled` | `disabled`
- **settingsFile**: 이 hook이 속한 settings 파일 경로
- **hookEntry**: 실제 hook handler 객체 (항상 보관)

## 2. SKILL.md 변경 상세

### 2-1. 제거할 섹션/내용
- `## Env Variable Naming Convention` 섹션 전체 삭제
- Hook JSON Structure Reference에서 `env` 부분 삭제
- Important Rules #4 "No migration" env 관련 문구 제거
- Important Rules #8 "env value toggle" 문구 제거
- 모든 `env`, `CLAUDE_HOOK_*` 참조 제거

### 2-2. 변경할 섹션

**타이틀**: "env-based toggle control" → "registry-based hook management"

**create 액션**:
- env 변수 생성 단계 제거
- registry에 엔트리 추가 단계로 대체
- "automatic env toggle wrapping" 문구 수정
- Name 필드 설명에서 "for env variable" 제거

**modify 액션**:
- 비활성 hook 수정 가이드 추가 (registry에서 hookEntry 수정)
- 활성 hook: settings + registry 둘 다 수정

**delete 액션**:
- env 제거 단계 → registry 엔트리 제거로 교체
- 빈 컨테이너 정리 범위를 disable과 통일 (event array + matcher group)

**enable 액션**:
- state.json → registry.json으로 변경
- env 값 변경 단계 제거
- registry의 status를 "disabled" → "enabled"로 변경

**disable 액션**:
- state.json → registry.json으로 변경
- env 값 변경 단계 제거
- registry의 status를 "enabled" → "disabled"로 변경

**list 액션**:
- env 파싱 단계 제거
- registry 파일 하나로 managed hook 전체 조회
- settings와 registry 교차 검증 (불일치 시 경고)
- unmanaged hook = settings에만 있고 registry에 없는 hook

### 2-3. 변경할 섹션: State File → Registry File

**섹션명**: `## State File (toggle backup)` → `## Registry File`
- 파일명: `hook-manager-state.json` → `hook-manager-registry.json`
- 구조 예시를 새 설계로 교체
- 모든 managed hook 추적 (enabled + disabled)
- `matcherIndex` 제거 → `matcher` (실제 패턴) + `settingsFile` 추가

## 3. hook-recipes.md 변경 상세

### 모든 레시피 공통:
- `Env` 필드 → `Name` 필드로 교체 (registry 키)
- Generated JSON에서 셸 래퍼 (`[ "${VAR:-1}" = "1" ] && ...`) 전부 제거 → 순수 커맨드만
- test-gate의 agent-type toggle 관련 note 삭제 (모든 타입 동일하므로)

### 변경 예시 (auto-format):

Before:
```
| Env | `CLAUDE_HOOK_POSTTOOLUSE_FORMAT` |
```
After:
```
| Name | `FORMAT` |
```

Before Generated JSON:
```json
"command": "[ \"${CLAUDE_HOOK_POSTTOOLUSE_FORMAT:-1}\" = \"1\" ] && jq -r ... || true"
```
After Generated JSON:
```json
"command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true"
```

## 4. 동기화

마스터 파일 수정 완료 후:
```bash
cp ClaudeCode/.claude/skills/hook-manager/SKILL.md .claude/skills/hook-manager/SKILL.md
cp ClaudeCode/.claude/skills/hook-manager/references/hook-recipes.md .claude/skills/hook-manager/references/hook-recipes.md
```

## 5. 검증

- SKILL.md에 `env`, `CLAUDE_HOOK_*` 잔존 참조 없는지 grep 확인
- hook-recipes.md에 셸 래퍼 패턴 잔존 없는지 grep 확인
- registry 구조의 일관성: create/modify/delete/enable/disable 모든 액션에서 registry 경로와 필드명 통일 확인

---
name: skill-creator
description: Claude Code skill 생성 가이드. "스킬 만들어줘", "create a skill", "make a new skill", "build a skill for...", "새 스킬 생성" 시 트리거.
---

# Skill Creator (v2.1+)

## 사용자 질문 프로세스 (필수)

스킬 생성 전 반드시 다음 정보를 사용자에게 확인:

### 1단계: 기본 정보

```
1. 스킬 이름 (kebab-case, 예: code-review, api-generator)
2. 스킬 설명 (무엇을 하는가 + 언제 사용하는가)
3. 주요 사용 시나리오 (어떤 요청에 트리거되어야 하는가)
```

### 2단계: 실행 환경

```
4. 컨텍스트 격리 필요?
   - fork: 메인 대화와 독립된 서브에이전트에서 실행
   - (미지정): 현재 대화 컨텍스트에서 실행

5. 특정 에이전트 타입 사용?
   - Explore: 코드베이스 탐색
   - Plan: 계획 수립
   - general-purpose: 범용 작업
   - (미지정): 기본 동작
```

### 3단계: 도구 권한

```
6. 허용할 도구 목록 (선택):
   - Read, Write, Edit, Glob, Grep
   - Bash(명령어 패턴): Bash(npm *), Bash(git *)
   - 미지정 시 모든 도구 허용
```

### 4단계: 추가 설정

```
7. 슬래시 메뉴에 표시? (user-invocable)
   - true (기본): /skill-name으로 직접 호출 가능
   - false: 자동 감지로만 트리거

8. Hooks 필요?
   - PreToolUse: 도구 실행 전 검증
   - PostToolUse: 도구 실행 후 처리
   - Stop: 스킬 완료 시 정리
```

## Skill 구조 (v2.1)

```
skill-name/
├── SKILL.md              # 필수: 메타데이터 + 지시사항
├── scripts/              # 선택: 실행 자동화
├── references/           # 선택: 필요시 로드되는 상세 문서
└── assets/               # 선택: 템플릿, 설정 (자동 로드 안됨)
```

## SKILL.md Frontmatter (v2.1 전체 스펙)

```yaml
---
# === 필수 ===
name: skill-name                    # kebab-case, ≤64자
description: |                      # ≤1024자, 트리거 키워드 포함
  스킬이 하는 일.
  트리거: "코드 리뷰", "PR 검토", "보안 검사"

# === 실행 환경 (선택) ===
context: fork                       # 독립 서브에이전트에서 실행
agent: Explore                      # context: fork와 함께 사용
                                    # Explore, Plan, general-purpose

# === 도구 권한 (선택) ===
allowed-tools:                      # YAML 리스트 형식 권장
  - Read
  - Grep
  - Glob
  - Bash(npm test:*)
  - Bash(git diff:*)

# === UI 설정 (선택) ===
user-invocable: true                # 슬래시 메뉴 표시 (기본: true)

# === Hooks (선택) ===
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true                # 세션당 한 번만 실행
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - type: command
      command: "./scripts/cleanup.sh"
---
```

## 스킬 생성 프로세스

### Step 1: 정보 수집

사용자에게 위 "사용자 질문 프로세스" 항목들을 질문하여 정보 수집

### Step 2: 스킬 초기화

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

### Step 3: SKILL.md 작성

**Frontmatter 규칙:**
- `name`: kebab-case, 최대 64자
- `description`: 무엇 + 언제 사용, 최대 1024자, 특수문자 금지

**Body 규칙:**
- 명령형 사용 ("Run", "Create" - "Running" 아님)
- 500줄 이하 유지, 초과 시 references/로 분리
- 불필요한 문서 파일 금지 (README.md, CHANGELOG.md 등)

### Step 4: 검증 및 패키징

```bash
# 검증
python scripts/validate_skill.py <path/to/skill-folder>

# 패키징 (선택)
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

## v2.1 주요 기능

### Hot-Reload

스킬 수정 시 세션 재시작 없이 즉시 반영

### Fork 컨텍스트

```yaml
context: fork
agent: Explore
```
- 메인 대화와 격리된 환경에서 실행
- 복잡한 작업도 메인 컨텍스트 오염 없이 처리

### Hooks

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
          once: true
```
- `once: true`: 세션당 한 번만 실행
- `additionalContext` 반환으로 동적 정보 제공 가능

### 중첩 디렉토리 발견

```
monorepo/
├── .claude/skills/global-skill/
├── packages/
│   └── frontend/.claude/skills/frontend-skill/
```
하위 디렉토리 작업 시 해당 경로의 스킬 자동 발견

## 리소스 타입

| 타입 | 용도 | 예시 |
|------|------|------|
| `scripts/` | 실행 자동화 | `scripts/init_project.py` |
| `references/` | 상세 문서 (필요시 로드) | `references/api-patterns.md` |
| `assets/` | 템플릿, 설정 (로드 안됨) | `assets/template/main.py` |

## Progressive Disclosure 패턴

SKILL.md를 간결하게 유지:

```markdown
## Quick Start
- 새 프로젝트: `python scripts/init.py`
- 기능 추가: "Development" 섹션 참고

## Advanced
→ 상세 내용: [references/workflows.md](references/workflows.md)
```

## 예시: 완성된 스킬

```yaml
---
name: secure-code-review
description: |
  보안 코드 리뷰 수행. PR 리뷰, 보안 검사, 취약점 분석 시 사용.
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(npm audit:*)
  - Bash(git diff:*)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
          once: true
  Stop:
    - type: command
      command: "./scripts/generate-report.sh"
user-invocable: true
---

# 보안 코드 리뷰

## 검사 항목
1. OWASP Top 10 취약점
2. 하드코딩된 시크릿
3. 의존성 취약점 (npm audit)

## 참고
상세 체크리스트: [references/security-checklist.md](references/security-checklist.md)
```

## 검증 체크리스트

```
SKILL.md 검증:
  ☐ name: kebab-case, ≤64자
  ☐ description: 무엇 + 언제, ≤1024자, 특수문자 없음
  ☐ body: <500줄
  ☐ 참조 파일 존재 확인
  ☐ 스크립트 실행 권한: chmod +x

v2.1 기능:
  ☐ context/agent 조합 확인
  ☐ allowed-tools YAML 리스트 형식
  ☐ hooks matcher 정규식 유효성
  ☐ once: true 적절히 사용
```

## 참고 문서

- [references/claude-code-specifics.md](references/claude-code-specifics.md): Claude Code 환경 특성
- [references/output-patterns.md](references/output-patterns.md): 출력 패턴
- [references/workflows.md](references/workflows.md): 워크플로우 패턴

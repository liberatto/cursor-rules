# Claude Code 환경 가이드라인

## 주요 기능

### 1. Hot-Reload

스킬 수정 시 세션 재시작 없이 즉시 반영됩니다.

```
~/.claude/skills/ 또는 .claude/skills/ 내 파일 변경
→ 자동으로 다음 요청부터 새 버전 사용
```

**활용:**
- 스킬 개발 중 빠른 반복 테스트
- 실시간 수정 및 확인

### 2. Fork 컨텍스트

메인 대화와 격리된 서브에이전트에서 스킬 실행:

```yaml
---
name: heavy-analysis
description: 대규모 코드 분석
context: fork
agent: Explore
---
```

**장점:**
- 메인 컨텍스트 오염 방지
- 복잡한 작업도 안전하게 실행
- 실패해도 메인 대화에 영향 없음

**에이전트 타입:**
| 타입 | 용도 |
|------|------|
| `Explore` | 코드베이스 탐색, 파일 검색 |
| `Plan` | 구현 계획 수립 |
| `general-purpose` | 범용 작업 |

### 3. Hooks

스킬 실행 중 특정 시점에 스크립트 실행:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true    # 세션당 한 번만
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - type: command
      command: "./scripts/cleanup.sh"
```

**Hook 타입:**
| 타입 | 시점 | 용도 |
|------|------|------|
| `PreToolUse` | 도구 실행 전 | 검증, 권한 체크 |
| `PostToolUse` | 도구 실행 후 | 린트, 포맷팅 |
| `Stop` | 스킬 완료 시 | 정리, 보고서 생성 |

**once: true:**
- 세션당 한 번만 실행
- 초기화 작업에 유용

### 4. 중첩 디렉토리 발견

모노레포에서 하위 디렉토리의 스킬 자동 발견:

```
monorepo/
├── .claude/skills/global-skill/      # 전역
├── packages/
│   ├── frontend/
│   │   └── .claude/skills/react-skill/  # frontend 작업 시 발견
│   └── backend/
│       └── .claude/skills/api-skill/    # backend 작업 시 발견
```

### 5. Slash Command와 Skills 통합

두 개념이 통합되어 있습니다:
- 동작 방식은 동일
- 개념적으로 단순화

---

## Claude Code vs Claude.ai 환경 차이

### 파일시스템 접근

| Claude.ai | Claude Code |
|-----------|-------------|
| 샌드박스 `/mnt/` 디렉토리 | 전체 파일시스템 접근 |
| 사용자가 업로드한 파일만 | 실제 프로젝트 파일 직접 접근 |
| 출력은 `/mnt/user-data/outputs/` | 어디든 쓰기 가능 |

**스킬 설계 시 고려:**
- 실제 프로젝트 파일 직접 읽기/수정 가능
- 파일 복사 불필요
- 전체 프로젝트 구조 탐색 가능
- 파괴적 작업 주의 필요

### 시스템 도구 접근

| Claude.ai | Claude Code |
|-----------|-------------|
| 제한된 컨테이너 도구 | 전체 시스템 접근 |
| 호스트와 격리 | 사용자 머신에서 실행 |
| 사전 설치 패키지만 | 패키지 설치 가능 |
| git 작업 불가 | 전체 git 접근 |

**Claude Code에서 사용 가능:**
```bash
# 버전 관리
git status, git commit, git push, git log

# 패키지 관리자
npm, yarn, pip, poetry, cargo, go

# 빌드 도구
make, cmake, gradle, maven

# 유틸리티
grep, find, sed, awk, curl, jq
```

### 프로젝트 컨텍스트

Claude Code가 접근할 수 있는 정보:

1. **프로젝트 구조**
   - 모든 파일과 디렉토리
   - 숨김 파일 (`.env`, `.gitignore`)
   - 설정 파일

2. **Git 히스토리**
   - 커밋 이력
   - 브랜치 정보
   - 커밋되지 않은 변경사항

3. **의존성**
   - `package.json` / `node_modules`
   - `requirements.txt` / 가상 환경
   - Lock 파일

4. **런타임 환경**
   - 환경 변수 (주의 필요!)
   - 설치된 도구
   - 시스템 설정

---

## 스킬 Best Practices

### 1. 프로젝트 감지

작업 전 프로젝트 타입 감지:

```markdown
## 프로젝트 감지

진행 전 프로젝트 식별:

1. `package.json` 확인 → Node.js
   - `scripts`에서 사용 가능한 명령 확인
   - `dependencies`에서 프레임워크 확인

2. `pyproject.toml` 또는 `requirements.txt` 확인 → Python
   - Python 버전 요구사항 확인
   - 가상 환경 확인

3. `.git/` 확인 → Git 활성화
   - 최근 커밋으로 컨텍스트 파악
   - 현재 브랜치 확인
```

### 2. 스타일 유지

기존 코드 컨벤션 준수:

```markdown
## 스타일 유지

코드 생성 전:

1. **기존 코드 분석**
   - 들여쓰기 (탭 vs 스페이스, 너비)
   - 따옴표 스타일 (작은따옴표 vs 큰따옴표)
   - 네이밍 컨벤션

2. **설정 파일 확인**
   - `.prettierrc` / `.eslintrc`
   - `pyproject.toml` (black/ruff 설정)
   - `.editorconfig`

3. **스타일 맞추기**
   - 기존 코드와 동일한 패턴 사용
   - 새로운 컨벤션 도입 금지
```

### 3. 비파괴적 작업

사용자 작업 보호:

```markdown
## 안전 가이드라인

절대 하지 말 것:
- 확인 없이 파일 삭제
- 백업 없이 덮어쓰기
- `.env` 파일 직접 수정
- 허락 없이 원격에 푸시

항상 할 것:
- 변경 전 변경 내용 표시
- 중요 수정 시 백업 생성
- 가능하면 변경사항 스테이징하여 검토
- `.gitignore` 패턴 준수
```

### 4. Git 적절히 활용

버전 관리 활용:

```markdown
## Git 통합

파일 수정 시:

1. **먼저 상태 확인**
   ```bash
   git status
   ```
   - 커밋되지 않은 변경사항과 충돌 방지

2. **중요 변경 시 브랜치 생성**
   ```bash
   git checkout -b feature/skill-changes
   ```

3. **명확한 메시지로 커밋**
   ```bash
   git commit -m "type(scope): description"
   ```

4. **절대 force push 금지**
   - 머지 충돌은 사용자가 처리하도록
```

### 5. 시크릿 주의

```markdown
## 시크릿 처리

절대 하지 말 것:
- API 키, 비밀번호, 토큰 로깅 또는 표시
- git에 시크릿 커밋
- 평문 파일에 시크릿 저장

시크릿이 필요할 때:
- 환경 변수 참조
- `.env` 파일 가리키기 (읽지 않고)
- 가능하면 시크릿 관리자 사용
```

---

## 스킬 타입별 패턴

### 코드 생성 스킬

```markdown
## 코드 생성

1. **먼저 언어/프레임워크 감지**
2. **코드베이스의 기존 패턴 확인**
3. **사용자 스타일로 생성**
4. **적절한 위치에 추가** (새 구조 생성 금지)
5. **필요시 import/export 업데이트**
```

### 리팩토링 스킬

```markdown
## 리팩토링

1. **먼저 기존 테스트 실행** (기준선 확보)
2. **원자적 변경** (한 번에 하나의 리팩토링)
3. **각 변경 후 테스트 실행**
4. **명확한 메시지로 점진적 커밋**
5. **동작 변경 금지** (구조만 변경)
```

### 테스트 스킬

```markdown
## 테스트

1. **테스트 프레임워크 감지** (jest, pytest 등)
2. **기존 테스트 패턴 따르기**
3. **올바른 위치에 테스트 배치**
4. **적절한 fixture/mock 사용**
5. **완료 전 테스트 통과 확인**
```

### 문서화 스킬

```markdown
## 문서화

1. **기존 문서** 형식과 스타일 확인
2. **복제가 아닌 업데이트**
3. **적절할 때 코드 근처에 문서 유지**
4. **관련 문서 링크**
5. **내부 링크에 상대 경로 사용**
```

---

## Frontmatter 전체 참조

```yaml
---
# === 필수 ===
name: skill-name                    # kebab-case, ≤64자
description: |                      # ≤1024자
  스킬이 하는 일.
  트리거 키워드 포함.

# === 실행 환경 (선택) ===
context: fork                       # 서브에이전트에서 실행
agent: Explore                      # context: fork와 함께 사용
model: sonnet                       # 모델 지정

# === 도구 권한 (선택) ===
allowed-tools:
  - Read
  - Grep
  - Bash(npm test:*)

# === UI (선택) ===
user-invocable: true                # 슬래시 메뉴 표시

# === Hooks (선택) ===
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true
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

---

## 문제 해결

### 스킬이 트리거되지 않음
- description에 구체적인 트리거 키워드 포함
- 다른 스킬과 description 차별화

### 스킬이 로드되지 않음
- SKILL.md 경로 및 이름 확인 (대소문자 구분)
- YAML frontmatter 문법 확인
- `/context` 명령으로 로드 상태 확인

### Hook 스크립트 실행 안됨
- 스크립트 실행 권한 확인: `chmod +x scripts/*.sh`
- 스크립트 경로가 상대 경로인지 확인 (`./scripts/...`)
- 스크립트 내 오류 확인

### Fork 컨텍스트 문제
- `context: fork` 설정 확인
- `agent` 값이 유효한지 확인 (Explore, Plan, general-purpose)

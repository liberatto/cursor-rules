# Plan: Claude Code Hooks 가이드 문서 작성

## Context

개발 중 Claude Code hooks를 활용하는 실전 가이드 문서가 필요하다. Hook 생성 방법은 크게 3가지:
1. **`/hooks` 메뉴** — CLI 내장 인터랙티브 메뉴로 GUI 방식 생성
2. **Claude Code에게 자연어 요청** — 대화로 요구사항 전달하여 자동 생성
3. **수동 JSON 편집** — settings.json을 직접 편집

현재 이 저장소에는 hooks 전용 가이드가 없으며, `RESEARCH-CLAUDE-CODE-SETTINGS-REFERENCE`에 약 40줄 분량의 설정 참조만 존재한다.

---

## 생성 파일

- **경로**: `docs/GUIDE-CLAUDE-CODE-HOOKS-2026-02-22-1500.md`
- **분량**: 약 500-550줄
- **Persona**: Engineer (how-to 가이드)

---

## 목차 및 섹션별 계획

### 1. 개요 (~20줄)
- Hook 정의: lifecycle 특정 시점에 자동 실행되는 사용자 정의 명령/프롬프트/에이전트
- CLAUDE.md(지시, LLM 재량) vs Hook(강제, 결정적 실행) 차이점
- Hook 생성 방법 3가지 소개 (이 문서의 핵심 흐름 안내)

### 2. 핵심 개념 Quick Reference (~80줄)

| 서브섹션 | 내용 |
|----------|------|
| 2.1 이벤트 전체 요약표 | 17종 이벤트를 1개 표로: 시점, 차단 가능 여부, Matcher 대상, Handler 지원 |
| 2.2 Handler Type 비교표 | command/prompt/agent 3종: 실행 방식, timeout, 비동기, 적합 상황 |
| 2.3 설정 파일 위치와 스코프 | 6개 위치별 스코프, 공유 가능 여부, 용도 예시 |
| 2.4 설정 구조 | 3-level nesting JSON 예시 + 주석 |

### 3. Hook 생성 방법 (~130줄) -- 핵심 섹션

#### 3.1 `/hooks` 메뉴로 생성하기 (~50줄)

인터랙티브 메뉴를 통한 step-by-step 워크플로우:

| 단계 | 내용 |
|------|------|
| Step 1 | `/hooks` 입력 → 17종 이벤트 목록 표시 → 이벤트 선택 |
| Step 2 | Matcher 설정 → `*` (전체) 또는 특정 패턴 입력 |
| Step 3 | "+ Add new hook..." 선택 → handler type(command/prompt/agent) 선택 → 커맨드/프롬프트 입력 |
| Step 4 | 저장 위치 선택 (User/Project/Local settings) |
| Step 5 | Esc로 CLI 복귀 → 즉시 활성화 |

- 메뉴에서 제공하는 기능: 조회, 추가, 삭제, 전체 비활성화 토글
- 소스 레이블: `[User]`, `[Project]`, `[Local]`, `[Plugin]`
- 장점: 오류 최소화, 즉시 반영, 이벤트/matcher 선택형
- 한계: `async`, `timeout`, `once`, `statusMessage` 등 고급 필드 설정 불가 → 수동 편집 필요

#### 3.2 Claude Code에게 자연어로 요청하기 (~60줄)

**기본 프롬프트 패턴:**
```
[상황/문제] + [원하는 동작] + [적용 범위] + [저장 위치(선택)]
```

**시나리오별 요청 예시 8개:** 프롬프트 + 예상 생성 결과 JSON

1. 파일 편집 후 자동 포맷팅
2. 위험 명령어 차단
3. 데스크톱 알림
4. 작업 완료 전 테스트 게이트
5. 환경변수 로딩
6. 보호 파일 수정 차단
7. MCP 도구 호출 로깅
8. Compact 후 컨텍스트 복원

**효과적인 요청 팁:**
- 이벤트명/handler type을 명시하면 정확도 향상
- 저장 위치 지정
- 구체적 시나리오 설명 > "hook 만들어줘"

#### 3.3 수동 JSON 편집 (~20줄)
- settings.json 직접 편집 시 주의사항
- 세션 중 편집 시 `/hooks`에서 리뷰 필요 (스냅샷 보안 메커니즘)
- 고급 필드(`async`, `timeout`, `once`, `statusMessage`) 설정법

#### 3.4 방법별 비교표

| 항목 | `/hooks` 메뉴 | Claude Code 요청 | 수동 편집 |
|------|---------------|-----------------|-----------|
| 난이도 | 쉬움 | 쉬움 | 중간 |
| 고급 설정 | 제한적 | 가능 | 전부 가능 |
| 즉시 반영 | O | O | 리뷰 필요 |
| 적합 상황 | 단순 hook | 복잡한 로직 | 세밀한 제어 |

### 4. 개발 시나리오별 Use Case (~90줄)

6개 카테고리별 표 형태:

| 카테고리 | 시나리오 수 |
|----------|------------|
| 4.1 코드 품질 & 포맷팅 | 3개 (자동 포맷팅, 린트 피드백, 타입 체크) |
| 4.2 보안 & 접근 제어 | 5개 (위험 명령 차단, 보호 파일, MCP 검증, 설정 감사, 권한 자동처리) |
| 4.3 테스트 & 검증 | 4개 (Stop 게이트, 편집 후 테스트, Task 검증, 서브에이전트 검증) |
| 4.4 알림 & 모니터링 | 3개 (데스크톱 알림, Bash 로깅, 실패 알림) |
| 4.5 세션 관리 & 컨텍스트 | 5개 (env 로딩, compact 복원, 프롬프트 필터, 세션 정리, compact 전 저장) |
| 4.6 팀 협업 & 서브에이전트 | 3개 (idle 게이트, task 검증, 컨텍스트 주입) |

각 시나리오: `이벤트 | Matcher | Handler | 설명` 형태

### 5. 실전 구현 예시 (~80줄)

가장 빈번한 6가지의 복사-붙여넣기 가능한 JSON + 스크립트:

1. **파일 편집 후 자동 포맷팅** (PostToolUse + command)
2. **위험 명령어 차단** (PreToolUse + command + bash script)
3. **보호 파일 편집 방지** (PreToolUse + command + bash script)
4. **데스크톱 알림** (Notification + command + osascript)
5. **Compact 후 컨텍스트 복원** (SessionStart + command)
6. **작업 완료 전 테스트 강제** (Stop + agent hook)

### 6. Matcher 패턴 가이드 (~30줄)
- 정확 매칭, OR 패턴, 와일드카드, MCP 서버 필터링
- 이벤트별 matcher 대상 요약표

### 7. Exit Code와 JSON 출력 (~40줄)
- Exit code 동작 규칙 (0/2/기타)
- 공통 JSON 출력 필드 (`continue`, `stopReason`, `systemMessage`)
- 이벤트별 decision control 요약표

### 8. 디버깅 & 트러블슈팅 (~30줄)
- `claude --debug`, `Ctrl+O`, `/hooks` 메뉴
- 체크리스트: 미실행, 무한루프, JSON 파싱 실패, 스크립트 권한

### 9. 참고 자료 (~10줄)
- 공식 문서 링크, 이 저장소의 관련 문서 상호 참조

---

## 참조 파일

| 파일 | 역할 |
|------|------|
| `docs/GUIDE-CLAUDE-MD-BEST-PRACTICES-2026-02-20-1300.md` | 문서 스타일/포맷 패턴 기준 |
| `docs/RESEARCH-CLAUDE-CODE-SETTINGS-REFERENCE-2026-02-20-1200.md` | hooks 설정 참조, 상호 링크 대상 |
| `ClaudeCode/.claude/skills/skill-creator/SKILL.md` | 스킬 frontmatter hooks 문법 참조 |

---

## 검증 방법

1. 문서 생성 후 마크다운 렌더링 확인 (테이블, 코드 블록, 헤더 계층)
2. JSON 예시의 문법 유효성 확인
3. 기존 문서(`RESEARCH-*`)와의 정보 일관성 검증
4. 시나리오별 프롬프트 예시가 실제 Claude Code에서 동작 가능한지 확인

# CLAUDE.md 작성 가이드 문서 계획

## Context

Claude Code는 세션 간 메모리가 없어 매 세션마다 CLAUDE.md를 자동 로드하여 프로젝트 컨텍스트를 제공한다. 잘 작성된 CLAUDE.md는 Claude의 작업 품질을 크게 높이지만, 잘못 작성하면 오히려 지시사항 무시 현상이 발생한다. 공식 문서, GitHub 커뮤니티 사례, 이 저장소의 기존 커맨드(claude.md-dive/review/update/local)를 종합하여 실용적인 가이드 문서를 작성한다.

## 생성 파일

`docs/GUIDE-CLAUDE-MD-BEST-PRACTICES-2026-02-20-1300.md`

## 문서 구조

### 1. 개요 — CLAUDE.md란 무엇인가
- 정의: 매 세션마다 자동 로드되는 영속적 프로젝트 메모리
- 핵심 역할: 프로젝트 컨텍스트, 코딩 규칙, 워크플로우 전달

### 2. 파일 체계 — 종류와 계층 구조
- 메모리 계층 표 (조직 → 사용자 → 프로젝트 → 로컬 → rules → auto memory)
- 각 파일의 위치, Git 추적 여부, 공유 범위
- 로딩 메커니즘 (상향 탐색 + 하향 지연 로딩)
- 우선순위 규칙 (더 구체적인 것이 우선)

### 3. 작성 원칙 — 효과적인 CLAUDE.md를 위한 5가지 원칙
1. 간결성 우선 (50~100줄 이상적, 300줄 경계)
2. 구체성 (모호한 지시 → 실행 가능한 규칙)
3. 참조 > 복사 (파일 경로 참조, 코드 스니펫 지양)
4. WHY 중심 (아키텍처 결정의 이유)
5. 정기 검토 (1~2주마다 pruning)

### 4. 포함할 것 vs 제외할 것
- 포함: 빌드 명령, 코딩 스타일 예외, 테스트 방식, 아키텍처 결정, 함정/주의사항, Git 워크플로우
- 제외: 린터로 처리할 코드 스타일, 표준 언어 컨벤션, 프레임워크 설명서 전문, API 키, 장문 튜토리얼

### 5. 권장 섹션 구조 — 템플릿
- 프로젝트 루트 CLAUDE.md 템플릿
- 서브디렉토리 CLAUDE.md 템플릿
- 글로벌(~/.claude/CLAUDE.md) 템플릿
- CLAUDE.local.md 템플릿 (Session / Rolling)

### 6. 크기 관리 — 대규모 프로젝트 전략
- 크기별 상태 표 (0~100 이상적 → 500+ 위험)
- `.claude/rules/` 분리 전략
- `paths` frontmatter로 조건부 로딩
- Import(`@`) 문법 활용

### 7. 안티패턴 — 피해야 할 실수들
- Kitchen Sink (과다 작성)
- 코드 스니펫 복사-붙여넣기
- 자동 생성 후 무비판적 사용
- 린팅 규칙 수동 명시
- 대용량 문서 @참조

### 8. 실전 워크플로우
- 초기 생성: `/init` → 수동 정제
- 정기 검토 체크리스트
- 이 저장소 커맨드 활용: `claude.md-dive`, `claude.md-review`, `claude.md-update`, `claude.md-local`

### 9. 참고 자료
- 공식 문서 URL
- 커뮤니티 가이드 URL

## 작성 기준

- 한국어 작성, 기술 용어는 영어 유지
- 실용적 예시 포함 (좋은 예/나쁜 예 대비)
- 목표 분량: 250~350줄 (가이드 문서이므로 리서치 보고서보다 길 수 있음)
- 이 저장소의 기존 커맨드(claude.md-* 4종)와의 연계 언급

## 참조할 소스

- 공식: https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/best-practices
- HumanLayer: https://www.humanlayer.dev/blog/writing-a-good-claude-md
- Builder.io: https://www.builder.io/blog/claude-md-guide
- Tembo: https://www.tembo.io/blog/how-to-write-a-great-claude-md
- 기존 커맨드: `.claude/commands/ssp/claude.md-{dive,review,update,local}.md`

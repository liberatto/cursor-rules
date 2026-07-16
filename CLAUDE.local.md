# Rules Repository — 운영 컨텍스트

> Last updated: 2026-02-08

이 저장소는 다른 실제 프로젝트 진행 중 발견되는 개선점을 지속 반영하는 **상시 운영 프로젝트**이다. 특정 목표 완료 후 리셋하지 않고, rolling 방식으로 관리한다.

---

## Design Decisions (확정된 설계 결정)

> 이 저장소 운영에 관한 결정. 향후 세션에서 동일 질문이 나오면 참조.

- **CLAUDE.local.md는 rolling 운영**: 목표 완료 후 리셋하지 않음. Backlog/Recent Changes/Known Issues를 상시 관리
- **CLAUDE.local.md = "session context manager"**: 복수 대화에 걸친 연속 작업 흐름 관리. 완료 항목도 간략 보존
- **Global CLAUDE.md 자동 수정 제외**: `claude.md-update` 커맨드가 `~/.claude/CLAUDE.md`를 자동 수정하지 않음
- **커밋 그루핑 원칙**: 기능 개선 / 신규 추가 / 설정 유지보수로 논리 분리
- **frontmatter `argument-hint` 따옴표 필수**: YAML 특수문자 포함 시 크래시 방지
- **settings.local.json 동기화 구조**: `ClaudeCode/.claude/`가 마스터 원본, `.claude/`(루트)는 이 프로젝트에서 테스트용으로 복사. 변경은 항상 마스터에서 먼저 수행 후 로컬에 복사

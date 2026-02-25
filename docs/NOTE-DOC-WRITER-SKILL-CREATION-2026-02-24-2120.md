# doc-writer 스킬 생성 메모

## 기능

문서 생성 요청 시 **네이밍 규칙 + Persona + 구조 템플릿**을 자동 적용하여 일관된 문서를 생성하는 스킬.

- 문서 타입 9종: PRD, PLAN, RESEARCH, REPORT, GUIDE, ANALYSIS, ADR, NOTE, DOCUMENTATION
- Persona 5종: PM, Analyst, Researcher, Engineer, Architect
- 타입별 구조 템플릿 (필수/선택 섹션 구분)

## 특징

- **자동 트리거**: "PRD 작성해줘", "ADR 만들어줘" 등 키워드로 자동 감지
- **네이밍 자동화**: `{PREFIX}-{DESCRIPTION}-{YYYY-MM-DD-HHMM}.md` 형식 + `date` 명령 필수
- **Persona 기반 톤 전환**: 문서 타입에 따라 작성 관점이 달라짐 (PM은 비즈니스 관점, Engineer는 재현 가능성 등)
- **CLAUDE.md에서 분리**: 기존 Document Naming Convention 섹션을 스킬로 이전 (CLAUDE.md 간소화)

## 파일 구조

```
ClaudeCode/.claude/skills/doc-writer/
├── SKILL.md                 # 워크플로우, 네이밍 규칙, 타입 테이블 (96줄)
└── references/
    ├── personas.md           # Persona 5종 상세 정의 (103줄)
    └── templates.md          # 타입 9종 구조 템플릿 (237줄)
```

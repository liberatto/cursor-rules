---
name: doc-writer
description: |
  프로젝트 문서 생성 스킬. 문서 타입별 네이밍 규칙, Persona 기반 작성 관점, 구조 템플릿을 적용하여 일관된 문서를 생성한다.
  트리거: "PRD(요구사항) 작성", "PLAN(계획) 만들어줘", "RESEARCH(연구,조사) 문서", "REPORT(상태/진행 보고) 생성", "GUIDE(How-to 가이드) 작성", "ANALYSIS(분석) 문서", "ADR(아키텍처 결정 기록) 만들어줘", "NOTE(메모) 작성", "DOCUMENTATION(일반 문서) 생성", "문서 작성", "문서 만들어줘", "create a document", "write a PRD", "write a guide"
---

# Doc Writer

프로젝트 문서를 타입별 네이밍 규칙, Persona, 구조 템플릿에 따라 일관되게 생성한다.

## 워크플로우

문서 생성 요청 시 아래 순서를 따른다:

```
요청 수신 → 타입 식별 → 타임스탬프 확인 → 파일명 생성 → 경로/중복 검증 → Persona 채택 → 템플릿 적용 → 문서 작성
```

### 1. 타입 식별

사용자 요청에서 문서 타입을 파악한다. 명시적 PREFIX가 없으면 맥락으로 추론하고 사용자에게 확인한다.

| Prefix | 용도 | Persona |
|--------|------|---------|
| `PRD` | 제품 요구사항 | PM |
| `PLAN` | 구현, 실행 계획 | Analyst |
| `RESEARCH` | 리서치 결과 | Researcher |
| `REPORT` | 상태/진행/완료 보고 | PM |
| `GUIDE` | How-to 가이드 | Engineer |
| `ANALYSIS` | 기술,비교,대안 분석 | Analyst |
| `ADR` | 아키텍처 결정 기록 | Architect |
| `NOTE` | 간단 메모 | — (자유형) |
| `DOCUMENTATION` | 일반 문서 | Engineer |

### 2. 타임스탬프 확인

**반드시 `date` 명령으로 현재 시각을 확인한다.** LLM 지식 기준일을 사용하지 않는다.

```bash
date "+%Y-%m-%d %H:%M"
```

### 3. 파일명 생성

**네이밍 규칙:**

- **형식**: `{PREFIX}-{BRIEF-DESCRIPTION}-{YYYY-MM-DD-HHMM}.md`
- **대소문자**: PREFIX와 DESCRIPTION은 **ALL UPPERCASE**
- **구분자**: 하이픈(`-`)으로 단어 구분
- **DESCRIPTION**: 핵심 내용을 2-4단어로 요약

**예시:**

| 요청 | 파일명 |
|------|--------|
| "사용자 인증 PRD 작성해줘" | `PRD-USER-AUTH-FEATURE-2026-02-24-1430.md` |
| "DB 마이그레이션 계획" | `PLAN-DATABASE-MIGRATION-2026-02-24-1430.md` |
| "GraphQL vs REST 비교 조사" | `RESEARCH-GRAPHQL-VS-REST-2026-02-24-1430.md` |

### 4. 경로 및 중복 검증

- **기본 위치**: `docs/` 폴더 (사용자가 다른 경로 지정 시 그대로 사용)
- `docs/` 디렉토리 존재 여부 확인 → 없으면 생성
- 동일 PREFIX + 유사 DESCRIPTION 파일 존재 여부 확인 → 중복 시 사용자에게 알림

### 5. Persona 채택

문서 타입에 지정된 Persona를 작성 관점으로 채택한다:

- Persona의 **톤, 관점, 핵심 질문**을 따른다
- NOTE 타입은 Persona 없이 자유형으로 작성

상세 Persona 정의: [references/personas.md](references/personas.md)

### 6. 템플릿 적용 및 작성

해당 타입의 구조 템플릿을 기반으로 문서를 작성한다:

- `[필수]` 섹션은 반드시 포함
- `[선택]` 섹션은 맥락에 따라 포함/생략
- 사용자가 특정 구조를 요청하면 그것을 우선
- 작성 시 공통 품질 원칙(독자 중심, 명확성, 근거와 예시, 점진적 구조, 훑어읽기)을 적용

타입별 구조 템플릿: [references/templates.md](references/templates.md)
공통 작성 및 품질 원칙: [references/writing-principles.md](references/writing-principles.md)

## 규칙

1. **타임스탬프**: 항상 `date` 명령 실행. 절대 추측하지 않는다.
2. **대소문자**: 파일명 PREFIX와 DESCRIPTION은 전부 대문자.
3. **하이픈**: 공백 대신 하이픈 사용.
4. **경로 확인**: 파일 생성 전 상위 디렉토리 존재 확인.
5. **Persona 충실**: 지정된 Persona의 관점을 일관되게 유지.
6. **구조 준수**: 템플릿의 필수 섹션을 적용한다.
7. **품질 원칙**: 공통 작성 및 품질 원칙을 적용한다.
8. **내용 우선**: 템플릿은 가이드일 뿐, 실질적 내용이 더 중요하고 내용에 따라 템플릿을 변경할 수 있다.

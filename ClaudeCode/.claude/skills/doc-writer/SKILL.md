---
name: doc-writer
description: |
  프로젝트 문서를 타입별로 생성·정리하는 스킬. PRD·PLAN·RESEARCH·ANALYSIS·ADR(사용자↔Claude 협업 문서), REPORT·DOCUMENTATION·GUIDE(외부 독자 문서), NOTE(개인 메모)를 네이밍 규칙·프론트매터·Persona 관점으로 고정 템플릿 없이 작성한다. 저장되는 문서·파일 산출물을 만들거나 갱신하려는 의도가 분명할 때에만 사용한다 — 즉 (a) 문서·자료·가이드·보고서·리포트·기획서·계획서·결정 기록·메모 같은 산출물 명사, 또는 (b) "파일로/문서로/md로/docs에 남겨·정리·저장" 같은 표현이 있고 대체로 작성·만들어·생성 동사가 붙는 경우. 반대로 "분석해줘"·"조사해봐"·"검토해줘"·"계획 짜줘"·"요약해줘"처럼 작업 수행만 요청하면(결과를 대화로 답하면 되는 경우) 문서를 만들지 않는다. 기존 문서 요약·조회, 코드 docstring·커밋 메시지, 데이터 분석·시각화, 순수 문체 교정(→ report-style)에도 쓰지 않는다.
  트리거: "PRD 작성", "PLAN(계획) 문서 만들어줘", "RESEARCH(조사) 문서로 정리", "REPORT(진행 보고서) 작성", "GUIDE(How-to 가이드) 작성", "ANALYSIS(분석) 문서 만들어줘", "ADR(결정 기록) 남겨줘", "NOTE(메모) 작성", "이 내용 문서로 정리해줘", "파일로 남겨줘", "docs에 정리해 저장", "create a document", "write a PRD", "write a guide"
---

# Doc Writer

프로젝트 문서를 타입별 네이밍 규칙과 Persona에 따라, 고정 템플릿 없이 프로젝트 특성·상황에 맞게 유연하게 생성한다.

**적용 조건**: 이 스킬은 **저장되는 문서·파일 산출물을 만들거나 갱신하려는 의도가 분명할 때만** 동작한다. "분석해줘"·"조사해봐"·"검토해줘"·"계획 짜줘"처럼 작업 수행만 요청한 경우(결과를 대화로 답하면 되는 경우)에는 문서를 만들지 말고, 산출물이 필요해 보이면 "문서로 남길까요?"라고 먼저 확인한다.

## 워크플로우

문서 생성 요청 시 아래 순서를 따른다:

```
요청 수신 → 타입 식별 → 타임스탬프 확인 → 파일명 생성 → 경로/중복 검증 → Persona 채택 → 프론트매터 작성 → 페르소나 기반 작성
```

위는 **새 문서 생성** 흐름이다. **기존 문서 갱신** 시에는 타입 식별·파일명 생성·경로 검증을 건너뛰고, 본문을 수정한 뒤 프론트매터의 `updated`(오늘 날짜, `date`로 확인)와 필요 시 `status`만 갱신한다.

### 1. 타입 식별

사용자 요청에서 문서 타입을 파악한다. 명시적 PREFIX가 없으면 맥락으로 추론하고 사용자에게 확인한다.

| Prefix | 용도 | 문서군 | Persona |
|--------|------|--------|---------|
| `PRD` | 제품 요구사항 | 협업 | PM |
| `PLAN` | 구현·실행 계획 | 협업 | Analyst |
| `RESEARCH` | 리서치 결과 | 협업 | Researcher |
| `ANALYSIS` | 기술·비교·대안 분석 | 협업 | Analyst |
| `ADR` | 아키텍처 결정 기록 | 협업 | Architect |
| `REPORT` | 상태·진행·완료 보고 | 외부 독자 | PM |
| `GUIDE` | How-to 가이드 | 외부 독자 | Engineer |
| `DOCUMENTATION` | 일반 문서 | 외부 독자 | Engineer |
| `NOTE` | 간단 메모 | 메모 | — (자유형) |

**문서군**에 따라 독자와 적용 원칙이 다르다 (writing-principles 최상단 참조):
- **협업** (PRD·PLAN·RESEARCH·ANALYSIS·ADR): 독자 = 사용자·Claude. 세션 간 공유 컨텍스트. §1–6 + §7 한국어 문장 스타일.
- **외부 독자** (REPORT·DOCUMENTATION·GUIDE): 독자 = 팀 외부 사람(비전문 독자 포함 가능). 독자 중심, §7 미적용(읽기 쉬운 완결 문장).
- **메모** (NOTE): 개인 임시 기록. 자유 형식, 정해진 가이드 없음.

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
- Persona의 타입별 **핵심 커버리지**를 작성 기준으로 삼는다
- NOTE 타입은 Persona 없이 자유형으로 작성

상세 Persona 정의 및 타입별 핵심 커버리지: [references/personas.md](references/personas.md)

### 6. 프론트매터 작성

모든 문서는 본문 최상단에 YAML 프론트매터를 포함한다. 형식:

```yaml
---
type: adr
audience: 코어 엔진 개발자 · 아키텍처 결정권자
related_docs:
  - docs/STRATEGY-AGENT-STUDIO-CORE-ENGINE-2026-06-29-2152.md (3사상 — 이 결정이 지켜야 할 계약)
  - core/compiler/compile.py (구현 지점)
  - CLAUDE.md (루트 §4 확장 사다리)
created: 2026-06-30 14:30
updated: 2026-07-10
status: active
description: "먼저 결론 한 문장(무엇을 결정·판정했는가). 그다음 배경과 개요 1~2문장."
---
```

**필드 정의:**

| 필드 | 필수 | 설명 |
|------|------|------|
| `type` | 필수 | 문서 타입(소문자): `adr`, `prd`, `plan`, `research`, `report`, `guide`, `analysis`, `note`, `documentation` |
| `audience` | 필수 | 주 독자층. 협업 문서는 `사용자·Claude`, 외부 독자 문서는 실제 외부 독자층 (메모는 생략 가능) |
| `related_docs` | 선택 | 관련 문서·코드 경로. 각 항목 뒤 괄호로 관계를 주석. 없으면 필드 생략 |
| `created` | 필수 | 최초 작성 시각 `YYYY-MM-DD HH:MM`. **`date` 명령으로 확인**(파일명 타임스탬프와 동일) |
| `updated` | 선택 | 최종 수정일 `YYYY-MM-DD`. 기존 문서 갱신 시에만 추가 |
| `status` | 필수 | 문서 상태: `draft` / `active` / `superseded` / `archived` |
| `description` | 필수 | 결론 한 문장을 먼저, 이어서 배경·개요 1~2문장. 따옴표로 감쌈 |

- `related_docs`는 **포인터**일 뿐이다. 본문이 의존하는 핵심 내용은 여전히 본문에 인라인한다(writing-principles §6 Self-Contained).
- `description`은 "결론 먼저" 원칙을 따른다 — 독자가 첫 줄에서 문서의 결론을 파악할 수 있어야 한다.
- **NOTE**(개인 메모)는 프론트매터를 생략할 수 있다 — 필요 시 `type`·`created`만 둔다.

### 7. 페르소나 기반 작성

고정 템플릿을 강제하지 않는다. 채택한 Persona의 관점과 **핵심 커버리지**를 기준으로, 프로젝트 특성·규모·상황에 맞게 구조를 그때그때 구성한다:

- Persona의 "핵심 커버리지"를 기준으로 삼되, 고정 순서가 아니라 취사선택·재배열한다.
- 불필요한 요소는 생략하고, 상황이 요구하면 목록에 없는 요소를 추가한다.
- 사용자가 특정 구조를 요청하면 그것을 최우선한다.
- 작성 시 공통 품질 원칙(독자 중심, 명확성, 근거와 예시, 점진적 구조, 훑어읽기, 자립성)을 적용한다.
- **협업 문서**(PRD·PLAN·RESEARCH·ANALYSIS·ADR)를 한국어로 쓸 때는 명사형 종결 등 한국어 문장 스타일(writing-principles §7)을 함께 적용한다. **외부 독자 문서**(REPORT·DOCUMENTATION·GUIDE)는 §7 대신 독자 중심 완결 문장으로 쓴다.

상세 Persona 정의 및 타입별 핵심 커버리지: [references/personas.md](references/personas.md)
공통 작성 및 품질 원칙: [references/writing-principles.md](references/writing-principles.md)

## 규칙

1. **타임스탬프**: 항상 `date` 명령 실행. 절대 추측하지 않는다.
2. **대소문자**: 파일명 PREFIX와 DESCRIPTION은 전부 대문자.
3. **하이픈**: 공백 대신 하이픈 사용.
4. **경로 확인**: 파일 생성 전 상위 디렉토리 존재 확인.
5. **Persona 충실**: 지정된 Persona의 관점을 일관되게 유지.
6. **핵심 커버리지**: 고정 템플릿 대신 Persona의 핵심 커버리지를 기준으로 필요한 요소를 다룬다.
7. **프론트매터**: 모든 문서 최상단에 YAML 프론트매터를 포함한다. `created`는 `date`로 확인한다.
8. **품질 원칙**: 공통 작성 및 품질 원칙을 적용한다.
9. **내용 우선**: 구조는 가이드일 뿐, 실질적 내용이 더 중요하며 프로젝트 상황에 맞게 구조를 조정한다.

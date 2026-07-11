# Writing Principles

Quality principles applied to all documents, regardless of type or Persona.

**독자와 목적 — 문서군 3분류**: 이 스킬이 만드는 문서는 목적에 따라 세 갈래이며, 적용 원칙이 다르다.

- **협업 문서** — `PRD` · `PLAN` · `RESEARCH` · `ANALYSIS` · `ADR`. 주 독자는 **작성자(사용자)와 이후 세션의 Claude**. 외부 제출용 보고서가 아니라 프로젝트 진행 중 만들어 두고 다시 참고하는 **작업 산출물이자 세션 간 공유 컨텍스트**다. 결정·근거·현재 상태를 남겨 나중에 재개 가능하게 하는 것이 핵심 가치. 사람은 빠르게 스캔하고 Claude는 새 세션에서 모호함 없이 맥락을 복원하도록 쓴다. **§1–6 + §7(한국어 문장 스타일)** 적용.
- **외부 독자 문서** — `REPORT` · `DOCUMENTATION` · `GUIDE`. 주 독자는 **팀 외부의 사람**(비전문 독자 포함 가능). 처음 읽는 사람이 이해하고 활용하도록 **독자 중심**으로 쓴다. **§1–6 적용, §7 미적용** — 명사형 대신 읽기 쉬운 완결 문장. 특히 §1 User-Centered를 강하게 따른다.
- **개인 메모** — `NOTE`. 사용자가 임시로 기억·기록하는 용도. 정해진 가이드 없음 — 목적에 맞게 자유 작성(프론트매터도 생략 가능).

---

## 1. User-Centered

- Lead with the user's goal, not the feature.
- Answer "why should I care?" before "how does it work?"
- Anticipate user questions and pain points.

**Per document type** — for 협업 문서 the consumers are you and Claude, so the "Reader" below is a *content lens* (whose concerns to address); for 외부 독자 문서(REPORT·DOCUMENTATION·GUIDE) the "Reader" is the real external audience to write for:

| Type          | Reader                  | Reader's Core Question             |
|---------------|-------------------------|------------------------------------|
| PRD           | Stakeholders            | "Why are we building this?"        |
| PLAN          | Implementers            | "What do I need to do?"            |
| RESEARCH      | Decision-makers         | "What are the options?"            |
| REPORT        | Managers & stakeholders | "Where do things stand?"           |
| GUIDE         | Practitioners           | "Can I follow this as-is?"         |
| ANALYSIS      | Decision-makers         | "What does the analysis conclude?" |
| ADR           | Future teammates        | "Why was this decided?"            |
| NOTE          | Author & teammates      | "What was captured?"               |
| DOCUMENTATION | Practitioners           | "How does this work?"              |

---

## 2. Clarity First

- Use active voice and present tense.
- Keep sentences under 25 words.
- One main idea per paragraph.
- Define technical terms on first use.

---

## 3. Show, Don't Just Tell

- Include practical examples for every concept.
- Provide complete, runnable code samples.
- Show expected output.
- Include common error cases.

---

## 4. Progressive Disclosure

- Structure from simple to complex.
- Quick start before deep dives.
- Separate must-read content from optional depth explicitly.
- Don't overwhelm — let readers stop at the depth they need.

---

## 5. Scannable Content

- Use descriptive headings.
- Bulleted lists for 3+ items.
- Tables for comparisons.
- Visual hierarchy: headings > bold > body text.

---

## 6. Self-Contained

- Reference only within the document — don't send the reader to another file for context the document needs.
- If external context is essential, inline its substance, not a link.
- A reader should understand the document without opening anything else.
- **Anti-pattern — Leaky Package**: linking out to context the document depends on; reads fine here, breaks when the file is shared or moved.
- The test: Can a reader understand this without opening anything else? If no, inline more.

---

## 7. Korean Sentence Style (한국어 문서)

**적용 대상: 협업 문서(PRD·PLAN·RESEARCH·ANALYSIS·ADR)를 한국어로 쓸 때에만.** 외부 독자 문서(REPORT·DOCUMENTATION·GUIDE)와 메모(NOTE)에는 적용하지 않으며(이들은 독자 중심 완결 문장으로 씀), 협업 문서라도 영어로 쓰면 §1–6만 따른다. 협업 문서는 사용자와 이후 세션의 Claude가 함께 참고하는 작업 산출물이므로, 문체를 구어체가 아닌 일관된 기술 톤으로 통일해 **사람은 빠르게 스캔하고 Claude는 모호함 없이 파싱·복원**하도록 한다. 여기서 "명사형"은 **문장 종결형**만 가리킨다 — 내용을 명사 나열로 줄이라는 뜻이 아니다.

### 7.1 명사형 종결

- 문장 끝 어미는 명사형으로 마무리 — `~함`, `~정리`, `~확정`, `~필요`, `~진행 중`, `~예정`.
- `~합니다 / ~했다 / ~이다 / ~됩니다 / ~드립니다`는 쓰지 않는다.
- 예: "설정을 변경했습니다" → "설정 변경".

### 7.2 어미만 명사형 — 과압축 금지

명사형은 **문장 종결형에만** 적용한다. 조사·주어·목적어·연결어(단/즉/반면)를 통째로 생략하면 독자가 재해석해야 하므로 보존한다.

- 압축 상한 = 이 맥락을 모르는 사람(또는 새 세션의 Claude)이 **1회 읽고 이해**하는 선. 넘으면 글자 수보다 이해를 우선해 한 박자 풀어 쓴다.
- 여러 뜻으로 읽히거나 배경 지식이 있어야 복원되면 과압축 — 주어·맥락어 1개를 복원한다.
- 예: "검증 통과" → "FD 누수 검증 통과" / "도구 다양성. 가드레일 통일." → "도구 다양성 허용, **단** 가드레일은 통일".

### 7.3 구어·감정 표현 회피 (중립 기술 톤)

동작과 측정값을 감정 없이 사실로 서술한다. IT 도메인 구어 동사는 의미는 통하지만 문서·로그·번역에 약하므로 표준 IT 동사로 교체한다.

| 회피 | 권장 |
| --- | --- |
| 깔다 | 설치 / 스캐폴딩 / 구성 |
| 박다 | 고정 / 하드코딩 |
| 잡다 | 지정 / 설정 |
| 건드리다·손대다 | 수정 / 변경 |
| 풀리다·못 푼다 | 해결 |
| 뒤집다 | 반전 |
| 되돌리다 | 롤백(rollback) |
| 무너지다·폭락 | 하락 / 감소 |

판단 기준: "영문 릴리스 노트·API 문서로 번역해도 자연스러운가."

### 7.4 격식 한자어 회피

문어체 한자어는 일상 실무어로 교체한다. 기준: "중급 IT 실무자가 대화에서 쓰는 말인가."

| 회피 | 권장 |
| --- | --- |
| 구동 | 실행 / 동작 |
| 제고 | 향상 / 개선 |
| 강구 | 마련 |
| 도모 | 추진 |
| 모색 | 검토 |
| 관건 | 핵심 |
| 용이 | 쉬움 |
| 지양 | 피함 |
| 지향 | 목표 |

### 7.5 영어 직역체 회피

영문 자료·AI 산출물 기반 작업에서 직역 표현이 자주 섞인다. 한국어로 처음부터 썼다면 고르지 않았을 표현은 자연스러운 한국어로 바꾼다.

| 회피 | 권장 |
| --- | --- |
| 1급 (first-class) | 정식 지원 / 동등 지원 |
| 배타적이지 않다 (mutually exclusive) | 병행 가능 |
| 오버킬 (overkill) | 과함 |
| swap | 교체 |
| ~를 따라감 (follows) | ~ 환경을 그대로 따름 |

- IT 원어 유지가 정당하면(Brownfield·Scale-Adaptive 등) 첫 등장 시 한국어 부연 1회 병기: `Scale-Adaptive(규모별 적응)`.

### 7.6 기술용어·백틱·강조

- 기술용어는 영어 원문 유지(API·Transformer·Backend). 억지 한글화 금지.
- 약어는 첫 등장 시 괄호 병기: `JWT (JSON Web Token)`.
- 파일 경로·명령어·변수명·식별자는 백틱: `docs/`, `npm run build`.
- 굵게 강조는 핵심 결론·수치·제품명에만.

### 7.7 섹션 제목 = 명사구 한 덩어리

- 섹션 제목은 내용을 가리키는 **명사구 한 덩어리**. 동사·의문문·서술문·사설 논조("왜 ~가 필요한가")를 쓰지 않는다.
- 부연 dash(`—`)는 쓰지 않는다. 부연은 제목 안 명사구로 흡수하거나 괄호·콜론으로 처리. `·` `( )` `:` 는 허용.
- 예: "왜 에이전트 분리가 필요한가" → "에이전트 분리의 필요성" / "배경 — 계약 기반 설계" → "배경".

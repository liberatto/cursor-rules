---
name: ktspace
description: |
  KT Space Atlassian(ktspace.atlassian.net) 통합 네비게이터. Confluence 페이지·Jira
  이슈를 찾아 읽는 작업 전담. 두 모드로 동작 — 소속 4스페이스(ServicePlatform·
  PLATFORMAX·AICEPlatform·WISEPMLIFE) 트리 라우팅, 그리고 전사·소속 밖·Jira 평면
  검색(작성자 accountId·키워드·이슈키·Rovo/CQL/JQL). 어느 스페이스인지 몰라도 된다 —
  라우팅과 결과 제시 순위는 스킬이 판정한다.
  트리거: "컨플에서 찾아줘", "~ 문서·회의록 찾아줘", "담당주간보고 가져와", "6팀 자료",
  "팀 내부 회의록·개인공간", "AICE 고도화·운영 보고", "AIDM·EOScan·챕터과제·Factbook
  자료", "타 부문·타 팀 자료", "OOO이 작성한 글", "누가 이 과제 하나", "Jira 이슈 조회",
  "내 할당 이슈", "페이지 ID·tiny URL만 있어", "25년 TF 시절 원본", "전사에서 검색".
  경계: 페이지 내용을 쓰거나 고치는 작업은 confluence-write 담당 — 이 스킬은 찾고 읽을
  때 쓴다.
user-invocable: true
---

# KT Space Unified Navigator

KT Space Atlassian(Confluence + Jira)에 대한 통합 네비게이터. **두 모드**로 동작한다:

- **트리 모드**(소속 안): 사용자 쿼리의 시점·성격에 따라 4개 스페이스 reference로 라우팅 → 페이지 계층 탐색. 아래 Decision Tree.
- **평면 모드**(소속 밖·전사·미상·Jira): 라우팅 없이 작성자(accountId)·키워드·이슈키로 인스턴스 전체를 직접 검색. 아래 §전사·소속 밖 평면 검색.

쿼리를 받으면 **먼저 모드를 판별**한다. 소속 도메인 키워드(서비스플랫폼담당·6팀명·담당주간보고·AIDD·AICE·MSM·FDS·플랫폼AX TF 등)가 명확하면 트리 모드, "전사/타 부문/어느 공간인지 모름/Jira 전체/작성자로 찾기/페이지 ID만 앎"이면 평면 모드. 모호하면 트리 모드(DEFAULT) 먼저 시도.
Always respond in Korean.

## Common Context

- **Site**: https://ktspace.atlassian.net
- **Cloud ID**: `1d9716a4-ece1-4638-9eb5-415dcaf359e6`
- **User**: 박성수 / liberatto@gmail.com / Account ID `557058:609d38c5-afeb-4836-b3d4-2615dd0529bf`
- **Atlassian MCP 도구**:
  - Confluence: `getConfluencePage`, `getConfluencePageDescendants`, `searchConfluenceUsingCql`, `getConfluenceSpaces`
  - Jira: `searchJiraIssuesUsingJql`, `getJiraIssue`
  - 통합 자연어(Jira+Confluence 동시): `search`(Rovo) — 평면 모드 first choice

## 4개 스페이스 식별표

| Space Key | Space ID | Homepage ID | Role | Reference |
|-----------|----------|-------------|------|-----------|
| `ServicePlatform` | `696194342` | `696194447` | **DEFAULT** — 서비스플랫폼담당 (2026~), 6팀 + 담당 공통 | `references/current-serviceplatform.md` |
| `PLATFORMAX` | `142869115` | `142869983` | **PRIVATE** — 플랫폼엔지니어링팀 프라이빗 (2026~), 접근 제한 | `references/current-platformax.md` |
| `AICEPlatform` | `782368805` | `782369333` | **PROJECT** — (project) AICE 플랫폼 (2026-05-22~), AICE 고도화·운영·사업팀 협업 채널. 정식명 "(project) AICE 플랫폼" | `references/project-aiceplatform.md` |
| `WISEPMLIFE` | `41549830` | `41549832` | **LEGACY** — 플랫폼AX TF 공식 아카이브 (~2025), 변경 정지. 정식명 "(community) 슬기로운PM생활" | `references/legacy-wisepmlife.md` |

---

# Decision Tree — 어느 reference를 읽을지 결정

사용자 쿼리를 받으면 다음 순서로 라우팅:

## Step 0 — 인물·참여인력 쿼리 (cross-cutting)

"누가 ~과제 참여", "작성자/담당자로 찾기", "OOO 소속", "OOO이 작성한 글", "PO/PM이 누구"처럼 **사람**이 축인 쿼리는 스페이스 라우팅 전에 **`references/people-directory.md`를 먼저 읽어** accountId를 확보한다. 확보한 accountId로 `creator = "<accountId>"`(CQL) / `reporter`·`assignee = "<accountId>"`(JQL) 평면 검색. accountId 미상이면 Rovo로 찾아 author 역추출 후 people-directory에 보강. (스페이스가 명확하면 Step 1과 병행)

## Step 1 — 명시적 키워드 우선

| 사용자가 명시한 키워드 | 라우팅 |
|---|---|
| "WISEPMLIFE", "플랫폼AX TF", "TF 시절", "2025", "구 플랫폼AX", "레거시", "MSM PoV", "KODE 아티클", "MWC 출품", "AI Tour 전시", "TF 주간보고" | **legacy-wisepmlife.md** |
| "PLATFORMAX 스페이스", "플랫폼엔지니어링팀 프라이빗", "팀 내부 (자료)", "개발자그룹 회의록", "AIDM 폴더", "AO_Agent 폴더", "박성수 개인공간", "황범 개인공간", "(팀원) 개인공간" | **current-platformax.md** |
| "AICEPlatform", "(project) AICE 플랫폼", "AICE 플랫폼 (project)", "AICE 고도화 진행 보고", "AICE 운영 보고", "사업팀과 (공유)", "(PE) 시험지웹전환", "(PE) AIDU Agent Studio", "(PE) AIDU agent (개인학습교사)", "(PE) AIDU DesktopApp Update", "(PE) 검토", "(PO) 요구사항 정의서", "2026년 AICE 과제 인덱스" | **project-aiceplatform.md** |
| 위에 해당 안 되면 | **Step 2** |

## Step 2 — 주제·범위 추론 (AICE 성격별 분리 주의)

| 주제·범위 | 라우팅 |
|---|---|
| 담당주간보고, C-level 보고, 6팀 과제 (융합서비스/고객서비스/모빌리티/커넥티드/플랫폼엔지니어링/AICC엔지니어링), Project 과제 관리, 플랫폼 Design Docs, AI-DLC·챕터과제(AIDD/ITO/Agent), EOScan Agent, Factbook, 추진방향(A/B/C/D 트랙), 담당 내 논의/토론장 | **current-serviceplatform.md** (DEFAULT) |
| **AICE 아키텍처·시스템 원본·차세대·관제·25년 사료(융합팀 트리 4개)** | **current-serviceplatform.md** (DEFAULT) |
| **AICE 고도화·운영·사업팀과 공유하는 공식 산출물·진행 보고** | **project-aiceplatform.md** (PROJECT) |
| **AICE 팀 내부 회의록·논의·작성중 메모** | **current-platformax.md** (PRIVATE) |
| 플랫폼엔지니어링팀 내부 회의록·개인 노트·작성중 자료 (AICE 외 주제) | **current-platformax.md** |
| 25년 vintage 명백 (FDS 기획 원본 / 정기시험 VoC / 팔란티어 업무구조진단 / 25년 인증·결제 FD 산출물) | **legacy-wisepmlife.md** |
| 모호 | DEFAULT 우선 시도 → 미매칭 시 다른 reference fallback |

## Step 3 — 다중 reference 동시 필요 시

쿼리가 명시적으로 2개 이상의 시점·공간에 걸칠 때(예: "AIDD 25년~26년 변천 정리", "AICE 고도화 4과제 — 사업팀 공유본 vs 팀 내부 논의"):
- 각 reference 읽고 결과를 결합
- **결과 제시 순서는 아래 §결과 제시 우선순위(스페이스 랭킹)를 따른다** — PLATFORMAX는 항상 최후순위
- 시점·성격 표기 명확히 (예: "26-05 AICEPlatform (PE) 시험지웹전환 진행 보고 / 26-04 PLATFORMAX 팀 내부 논의 / 25년 WISEPMLIFE AICE 섹션")

---

# 결과 제시 우선순위 (스페이스 랭킹)

> 🔗 이 블록은 `ktspace-atlassian-explorer` 에이전트의 동일 섹션과 **동일 유지** — 한쪽 수정 시 함께 갱신.

**탐색 순서가 아니라 "찾은 결과를 사용자에게 보여주는 순서" 규칙.** 탐색은 4스페이스 모두 정상 수행하되, 제시할 때 아래 순위를 적용한다.

| 순위 | 스페이스 | 성격 |
|---|---|---|
| 1 | `ServicePlatform` · `AICEPlatform` | **공식·공유 산출물** — 담당·사업팀에 공개된 확정본 |
| 2 | **`PLATFORMAX`** | **초안·임시본 전용** — 팀 프라이빗. 공식 산출물 작성 **이전** 단계의 작업본 |
| 3 | **`WISEPMLIFE`** | **레거시(2025, 변경 정지) — 최후순위**. 현행 공간에서 못 찾았을 때 **참고로만** 제시 |

**PLATFORMAX 취급 원칙 (2순위)**:

- 팀의 프라이빗 공간으로, **공식 결과물이 되기 전의 초안·임시 버전을 관리하는 곳**. 의미 있는 자료이나 **확정본으로 인용하면 안 된다**.
- 결과 나열·"가장 유력한 후보" 선정 시 **공식 공간(1순위) 뒤로 내린다**. 다른 공간에 같은 계열 문서(공식본·개정본)가 있으면 **그쪽을 1순위 후보로 올리고**, PLATFORMAX 사본은 하위에 `(초안·임시)` 표기와 함께 둔다.
- 제시할 때는 항상 초안임을 명시 (예: "_(PLATFORMAX — 초안·임시본)_").

**WISEPMLIFE 취급 원칙 (최후순위)**:

- 2025 TF 시절 아카이브. **현행 아님** → 1·2순위 공간에서 **못 찾았을 때의 fallback 참고 자료**로만 제시한다.
- 현행 결과가 있으면 WISEPMLIFE 결과는 **원칙적으로 나열하지 않거나**, 필요 시 "📎 레거시 참고" 형태로 맨 끝에 짧게만 덧붙인다.
- 제시할 때 반드시 "레거시(2025), 현행 아님" 명시 + **현재형 단정 금지**(§응답 정책의 신선도 경고와 동일).

**예외 (정상 순위로 제시)**:

- 사용자가 PLATFORMAX·팀 내부·초안·개인공간·"작성중"을 **명시 지목**한 쿼리 → PLATFORMAX 정상 제시
- 사용자가 WISEPMLIFE·플랫폼AX TF·25년·레거시를 **명시 지목**한 쿼리 → WISEPMLIFE 정상 제시
- 해당 공간이 유일 소스인 경우 (단 `(초안·임시)` / `(레거시)` 표기는 유지)

---

# 명칭 변경 매핑 (Cross-cutting)

조직 명칭 변경 이력. 사용자가 어느 표현을 쓰든 양방향 인식하여 적절한 reference로 라우팅:

| 구 명칭 | 신 명칭 | 비고 |
|---|---|---|
| 플랫폼AX TF | 플랫폼AX팀 → **플랫폼엔지니어링팀** | 2025 TF → 2026 초 팀화 → 2026 현재 명칭 |
| AX서비스개발팀 | **고객서비스플랫폼팀** | 2026 조직개편. Project 과제관리 하위 페이지에 구 명칭 잔존 |
| ConnectedCore플랫폼팀 | **커넥티드플랫폼팀** | 2026 조직개편. 일부 페이지에 구 명칭 잔존 |
| (없음, 신설) | **AICC엔지니어링팀** | 2026-04 신설. MyK Agent / Voice Agent / Computer Use Agent |

---

# Common Navigation Strategy

reference로 라우팅된 후 공통 4단계:

1. **요청 분석** — reference 파일 내 트리에서 페이지 ID 매칭. 사람·영역·주제·시기 4축으로 식별
2. **Direct access** — Page ID 알면 `getConfluencePage(cloudId, pageId, contentFormat="markdown")` 즉시 접근
3. **Child exploration** — `getConfluencePageDescendants(cloudId, pageId, depth=1~3)` 로 하위 탐색. **폴더(type=folder)는 404 가능** → CQL `parent = "<id>"` 우회
4. **Search supplement** — 트리 미등록 페이지는 CQL로 보충
5. **결과 제시** — 핵심 요약 + 소스 링크 + 트리 위치 표시

## 소스 링크 포맷

- ServicePlatform: `[title](https://ktspace.atlassian.net/wiki/spaces/ServicePlatform/pages/{pageId})`
- PLATFORMAX: `[title](https://ktspace.atlassian.net/wiki/spaces/PLATFORMAX/pages/{pageId})`
- AICEPlatform: `[title](https://ktspace.atlassian.net/wiki/spaces/AICEPlatform/pages/{pageId})`
- WISEPMLIFE: `[title](https://ktspace.atlassian.net/wiki/spaces/WISEPMLIFE/pages/{pageId})`

---

# Common CQL Patterns

스페이스 키만 치환하면 어느 스페이스에든 적용 가능한 골격:

```sql
-- 키워드 검색 (스페이스 전체)
space = "<KEY>" AND text ~ "keyword" ORDER BY lastModified DESC

-- 제목 검색 (회차별 누적 페이지에 권장: 담당주간보고 등)
space = "<KEY>" AND title ~ "keyword" ORDER BY lastModified DESC

-- 최근 수정
space = "<KEY>" ORDER BY lastModified DESC

-- 특정 부모 하위
space = "<KEY>" AND ancestor = "<parentId>" ORDER BY lastModified DESC

-- 폴더 직계 자식 (folder 404 우회)
space = "<KEY>" AND parent = "<folderId>" ORDER BY title ASC

-- 날짜 범위
space = "<KEY>" AND lastModified >= "2026-05-01" ORDER BY lastModified DESC

-- 다중 스페이스 동시
(space = "ServicePlatform" AND title ~ "keyword") OR (space = "PLATFORMAX" AND title ~ "keyword") OR (space = "AICEPlatform" AND title ~ "keyword") ORDER BY lastModified DESC
```

**스페이스별 자주 쓰는 ancestor**:
- ServicePlatform 6팀: `696944019`(융합) `696295127`(고객) `696684740`(모빌리티) `696423896`(커넥티드) `696812952`(PE) `732598655`(AICC)
- ServicePlatform 담당 공통: `710748637`(Project 과제) `736007618`(논의/토론장) `696845994`(정기미팅)
- AICEPlatform 루트: `782369333`(홈) / `784080409`((PE) 00-01. AICE — 우리 팀 4과제) / `784272013`(2026년 AICE 과제 인덱스)
- WISEPMLIFE 플랫폼AX 루트: `148678396`
- PLATFORMAX 백업 폴더: `727192070`

---

# 전사·소속 밖 평면 검색 (평면 모드)

> 🔗 이 블록은 `ktspace-atlassian-explorer` 에이전트의 "§전사·소속 밖 평면 검색"과 **동일 유지** — 한쪽 수정 시 함께 갱신.

소속 4스페이스 **밖**, 어느 공간인지 **모름**, **타 부문·타 팀**, **작성자(accountId) 기준**, **Jira 전체**, **페이지 ID·tiny URL만** 아는 쿼리는 트리 라우팅이 필요 없다. 인스턴스 전체를 직접 검색한다.

## 검색 방식 — 언제 무엇을

| 방식 | 도구 | 언제 |
|---|---|---|
| **Rovo**(자연어) | `search` | first choice. "어디 있는지 모름"·광범위·한국어 semantic |
| **CQL**(정밀) | `searchConfluenceUsingCql` | 작성자·날짜·라벨·페이지ID 정밀 필터. `space` 빼면 전사 |
| **JQL**(Jira) | `searchJiraIssuesUsingJql` | 이슈·할당·프로젝트·상태 |

결과 미흡 시 메서드 전환 + 키워드 변형(영문↔한글, 약어 풀어쓰기).

## 평면 CQL/JQL 패턴

```sql
-- 인스턴스 전체 키워드 (space 미지정)
text ~ "keyword" ORDER BY lastModified DESC

-- 특정 작성자(타 부문 인물) 콘텐츠 — accountId는 references/people-directory.md에서 확보
creator = "<accountId>" ORDER BY lastModified DESC

-- 페이지 ID로 직접 조회 (스페이스 미상)
id = "<pageId>"

-- 라벨 기반 전사 추적
label = "<labelKey>" ORDER BY lastModified DESC
```

```sql
-- 내 할당 이슈 / 임의 이슈 키 / 작성자 / 키워드
assignee = currentUser() ORDER BY updated DESC
key = "ABC-123"
reporter = "<accountId>" ORDER BY updated DESC
text ~ "keyword" ORDER BY updated DESC
```

## 평면 모드 운영 규칙

- **스페이스 미상**: Rovo 결과의 `space` 필드로 발견, 또는 `getConfluenceSpaces`로 접근 가능 목록 조회
- **사용자 자기 콘텐츠 제외**(자기 콘텐츠 명시 요청 시 예외):
  - CQL: `creator != "557058:609d38c5-afeb-4836-b3d4-2615dd0529bf"`
  - JQL: `reporter != "557058:..."` (assignee 검색 시 불필요)
  - Rovo: API 필터 없음 → 결과 author 수동 확인
- **소속 안/밖 분류 안내**: 결과의 `space`가 소속 4스페이스(ServicePlatform/PLATFORMAX/AICEPlatform/WISEPMLIFE) 밖이면 명시 (예: "_(소속 외 공간: AXTDT)_")
- **한계 인지**: 평면 검색은 작성자·키워드엔 강하나, 타 부문 **트리 구조 심화 탐색**(폴더 계층 따라가기)은 그 스페이스 지식이 없어 약함 → 필요 시 `getConfluencePageDescendants`로 발견된 페이지부터 점진 확장

## 대량 결과 처리

- **10+**: 상위 5–7개만 read & 요약, 나머지는 제목/날짜 리스트
- **20+**: 검색 좁히기 제안(스페이스/날짜/키워드), 상위 5개만 요약
- **너무 큰 페이지**: 핵심 섹션만 추출, 전체 로드 전 확인

---

# Common Error Handling

| 증상 | 대응 |
|---|---|
| Page ID로 `getConfluencePage` 404 | CQL 검색으로 대체 (제목 또는 키워드) |
| 폴더(`type=folder`) descendants 호출 404 | CQL `parent = "<folderId>"` 또는 상위 페이지의 descendants로 우회 |
| 키워드 매칭 결과 0건 | 키워드 변형(영문↔한글, 약어 풀어쓰기), reference 트리에서 유사 섹션 제안 |
| 페이지가 너무 큼 (token 초과) | 핵심 섹션 일부만 추출 후 사용자 확인, `mcp_<id>.txt` 파일에서 chunk 단위 read |
| WISEPMLIFE ancestor 필터 실패 | `text ~ "플랫폼AX"` 키워드로 대체 |
| PLATFORMAX 접근 권한 제한 | 권한 없음 안내 후 다른 reference로 fallback 시도 |
| 명칭 변경 혼동 | 위 "명칭 변경 매핑" 표를 양방향 적용 |

---

# 응답 정책

- **항상 한국어**로 응답 (코드/CQL/페이지 제목 등 원문은 그대로)
- 검색 결과는 **트리 위치**(예: "ServicePlatform > Project 과제 관리 > 융합서비스플랫폼팀 과제")와 **소스 링크** 함께 제시
- 어느 reference로 라우팅했는지 짧게 명시 (예: "_(2026 ServicePlatform 기준)_") — 시점 혼동 방지
- ⚠ **LEGACY(WISEPMLIFE) 신선도 경고**: 2025 TF 시점·변경정지 자료라 신선도가 매우 낮음. 요약·제시 시 반드시 "레거시(2025), 현행 아님"을 명시하고 **현재형 단정 금지**(예: "~였음/~로 추정"). 현행 정보가 필요한 질문이면 current reference(ServicePlatform/PLATFORMAX/AICEPlatform) 교차 확인을 권고. 인물·조직·과제 상태는 그새 바뀌었을 수 있음(예: 25년 팀원이 타 팀으로 이동).

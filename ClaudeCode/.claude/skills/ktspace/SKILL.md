---
name: ktspace
description: |
  Unified navigator for KT Space Confluence (ktspace.atlassian.net). 3개 스페이스를 시점·성격에 따라 내부 라우팅합니다. KT Space의 팀·과제·보고·문서 관련 모든 쿼리에 이 스킬을 사용하세요.

  [DEFAULT] ServicePlatform (2026~) — 서비스플랫폼담당 6팀 + 담당 공통.
  Triggers: 서비스플랫폼, 담당주간보고, 6팀, AI-DLC, Factbook, 마이K, MCP사업화, MyK Agent,
  보이스봇, AICE 고도화, AIDM, IVI/GIS/XENLINK, IoT 통합플랫폼, AI케어, 펫케어, AICC엔지니어링,
  추진방향, A/B/C/D 트랙, Project 과제 관리, Design Docs, 담당 내 논의/토론장.
  → references/current-serviceplatform.md

  [PRIVATE] PLATFORMAX (2026~) — 플랫폼엔지니어링팀 프라이빗 공간 (팀 내부 전용, 접근 제한).
  Triggers: 플랫폼엔지니어링팀 내부, 개발자그룹 회의록, AIDM 폴더, AO_Agent, 대고객 행동 분석,
  분석가그룹, 개인공간(유정아·김영진·박대흠·임창용·박성수·황범), 팀 업무분장, Ground Rules,
  필수 보유 역량, AICE 추진방향 회의, kode:crew, AIDD 방향성, 박성수 개인공간.
  → references/current-platformax.md

  [LEGACY] WISEPMLIFE (~2025) — 플랫폼AX TF 시절 공식 자료 아카이브 (변경 정지).
  Triggers: WISEPMLIFE 명시, 플랫폼AX TF, 2025 TF, MSM PoV, KODE 아티클, MWC 출품, AI Tour,
  팔란티어 업무구조진단, 정기시험 VoC, FDS 기획 원본, AIDUez 3-Layer 원본, TF 주간보고
  (250519~260323), TF 정기/수시 보고, 25년 인증·결제·ITOA·트래픽 과제 원본.
  → references/legacy-wisepmlife.md

  Use this skill for ANY query targeting KT Space Confluence — current state, team-private,
  or legacy archive. Internal routing handles space selection based on keywords above.
user-invocable: true
---

# KT Space Unified Navigator

KT Space Atlassian Confluence(3개 스페이스)에 대한 통합 네비게이터. 사용자 쿼리의 시점·성격에 따라 적절한 reference로 내부 라우팅한다.
Always respond in Korean.

## Common Context

- **Site**: https://ktspace.atlassian.net
- **Cloud ID**: `1d9716a4-ece1-4638-9eb5-415dcaf359e6`
- **Atlassian MCP 도구**: `getConfluencePage`, `getConfluencePageDescendants`, `searchConfluenceUsingCql` 사용

## 3개 스페이스 식별표

| Space Key | Space ID | Homepage ID | Role | Reference |
|-----------|----------|-------------|------|-----------|
| `ServicePlatform` | `696194342` | `696194447` | **DEFAULT** — 서비스플랫폼담당 (2026~), 6팀 + 담당 공통 | `references/current-serviceplatform.md` |
| `PLATFORMAX` | `142869115` | `142869983` | **PRIVATE** — 플랫폼엔지니어링팀 프라이빗 (2026~), 접근 제한 | `references/current-platformax.md` |
| `WISEPMLIFE` | `41549830` | `41549832` | **LEGACY** — 플랫폼AX TF 공식 아카이브 (~2025), 변경 정지. 정식명 "(community) 슬기로운PM생활" | `references/legacy-wisepmlife.md` |

---

# Decision Tree — 어느 reference를 읽을지 결정

사용자 쿼리를 받으면 다음 순서로 라우팅:

## Step 1 — 명시적 키워드 우선

| 사용자가 명시한 키워드 | 라우팅 |
|---|---|
| "WISEPMLIFE", "플랫폼AX TF", "TF 시절", "2025", "구 플랫폼AX", "레거시", "MSM PoV", "KODE 아티클", "MWC 출품", "AI Tour 전시", "TF 주간보고" | **legacy-wisepmlife.md** |
| "PLATFORMAX 스페이스", "플랫폼엔지니어링팀 프라이빗", "팀 내부 (자료)", "개발자그룹 회의록", "AIDM 폴더", "AO_Agent 폴더", "박성수 개인공간", "황범 개인공간", "(팀원) 개인공간" | **current-platformax.md** |
| 위에 해당 안 되면 | **Step 2** |

## Step 2 — 주제·범위 추론

| 주제·범위 | 라우팅 |
|---|---|
| 담당주간보고, C-level 보고, 6팀 과제 (융합서비스/고객서비스/모빌리티/커넥티드/플랫폼엔지니어링/AICC엔지니어링), Project 과제 관리, 플랫폼 Design Docs, AI-DLC, Factbook, 추진방향(A/B/C/D 트랙), 담당 내 논의/토론장 | **current-serviceplatform.md** (DEFAULT) |
| 플랫폼엔지니어링팀 내부 회의록·개인 노트·작성중 자료 | **current-platformax.md** |
| 25년 vintage 명백 (FDS 기획 원본 / 정기시험 VoC / 팔란티어 업무구조진단 / 25년 인증·결제 FD 산출물) | **legacy-wisepmlife.md** |
| 모호 | DEFAULT 우선 시도 → 미매칭 시 다른 reference fallback |

## Step 3 — 다중 reference 동시 필요 시

쿼리가 명시적으로 2개 이상의 시점·공간에 걸칠 때(예: "AIDD 25년~26년 변천 정리"):
- 우선순위: **CURRENT(ServicePlatform/PLATFORMAX) > LEGACY**
- 각 reference 읽고 결과를 결합
- 시점 표기 명확히 (예: "26년 ServicePlatform AI-DLC 폴더 / 25년 WISEPMLIFE AICE 섹션")

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
(space = "ServicePlatform" AND title ~ "keyword") OR (space = "PLATFORMAX" AND title ~ "keyword") ORDER BY lastModified DESC
```

**스페이스별 자주 쓰는 ancestor**:
- ServicePlatform 6팀: `696944019`(융합) `696295127`(고객) `696684740`(모빌리티) `696423896`(커넥티드) `696812952`(PE) `732598655`(AICC)
- ServicePlatform 담당 공통: `710748637`(Project 과제) `736007618`(논의/토론장) `696845994`(정기미팅)
- WISEPMLIFE 플랫폼AX 루트: `148678396`
- PLATFORMAX 백업 폴더: `727192070`

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

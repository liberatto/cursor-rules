# [PROJECT/CURRENT] AICEPlatform Space — (project) AICE 플랫폼 (2026-05-22~)

AICE 고도화·운영·사업팀 협업을 위한 신규 프로젝트 스페이스. **우리 팀이 깊게 소속** — 공식 산출물·진행 보고를 사업팀과 공유하는 채널. 단순 협업 참여가 아니라 우리 팀 5과제(시험지웹전환·AIDU Agent Studio·AIDU agent 개인학습교사·AIDU DesktopApp Update·검토 자료(공통))가 `(PE)` prefix로 직접 게시됨.

> 2026-05-22 DevOps엔지니어링팀 장수림 책임이 스페이스 생성. 트리 초기 단계 — 페이지 수가 늘면 본 reference 정밀화 필요.

## Context

- **Space Key**: `AICEPlatform`
- **Space ID**: `782368805`
- **Homepage ID**: `782369333` ("(project) AICE 플랫폼")
- **Created**: 2026-05-22
- **Space Owner**: `712020:bf517513-2fc7-47af-94a1-98c3c33d6f11`
- **First Author**: 장수림 (DevOps엔지니어링팀)
- **Last verified**: 2026-06-28 (descendants depth=3 + 최근 CQL 재확인)

---

# 트리 구조 (2026-06-28, 32+페이지)

```
(project) AICE 플랫폼 [home] (782369333)
├── 2026년 AICE 과제 (784272013)                      ← 사업/과제 종합 인덱스
├── 백업 [folder] (836245315)                         ← 임창용 생성, 기획서·요구사항 정의서 백업
└── (PE)00-01. AICE (784080409)                       ← 우리 팀(플랫폼엔지니어링) 작업물
    ├── (PE)00-01-00. 현황 [folder] (784080425)
    │   ├── (PE) AICE 플랫폼 개요/현황/담당부서 (784080430)
    │   ├── (PE) AICE 시스템 구성도 (784080501)
    │   └── (PE) AIDU 내부 구조 (784080520)            ← 최근 활발(6/24)
    ├── (PE)00-01-01. 시험지웹전환 (784080537)
    ├── (PE)00-01-02. AIDU Agent Studio (Gen1급) (784080592)
    ├── (PE)00-01-03. AIDU agent (개인학습교사) (784081094)
    ├── (PE)00-01-04. AIDU DesktopApp Update (833291198)   ← 신규 5번째 과제, AWS/Azure 검토 활발
    └── (PE)00-01-99. 검토 자료 (공통) (784081521)         ← 날짜별 검토자료 누적
```

## 페이지 인벤토리

| Page | Page ID | Type | 비고 |
|------|---------|------|------|
| (project) AICE 플랫폼 [home] | `782369333` | page | 스페이스 홈 — 현재 기본 템플릿 |
| 2026년 AICE 과제 | `784272013` | page | depth 1 — 사업·운영 측 과제 종합 인덱스로 추정 |
| 백업 | `836245315` | **folder** | depth 1 — **신규**. 임창용 생성. 기획서·PO 요구사항 정의서(Gen1급) 백업 |
| (PE)00-01. AICE | `784080409` | page | depth 1 — 우리 팀 AICE 5과제 부모 |
| (PE)00-01-00. 현황 | `784080425` | **folder** | depth 2 — 현황 폴더 |
| ㄴ (PE) AICE 플랫폼 개요/현황/담당부서 | `784080430` | page | depth 3 |
| ㄴ (PE) AICE 시스템 구성도 | `784080501` | page | depth 3 |
| ㄴ (PE) AIDU 내부 구조 | `784080520` | page | depth 3 — 최근 활발(6/24) |
| (PE)00-01-01. 시험지웹전환 | `784080537` | page | depth 2 |
| (PE)00-01-02. AIDU Agent Studio (Gen1급) | `784080592` | page | depth 2 — Jira 프로젝트 `AIDUAGTSTD` 매핑 |
| (PE)00-01-03. AIDU agent (개인학습교사) | `784081094` | page | depth 2 — Jira 프로젝트 `AIDUAGT` 매핑 |
| (PE)00-01-04. AIDU DesktopApp Update | `833291198` | page | depth 2 — **신규 5번째 과제**. AWS/Azure 앱 업데이터 개발 |
| (PE)00-01-99. 검토 자료 (공통) | `784081521` | page | depth 2 — 날짜별 검토자료 5건+ 누적 |

---

# 6팀 매핑

| Prefix | 팀 | 현황 |
|--------|------|------|
| `(PE)` | **플랫폼엔지니어링팀 (우리 팀)** | 5과제 게시 중 |
| `(PO)` | 인재실/AICE기획팀 (PO 측) | **신규 등장** — PO 요구사항 정의서·기획자료가 PE 과제 트리·백업 폴더에 직접 게시 |
| (없음) | 공통 (사업·운영 측) | "2026년 AICE 과제" 인덱스 |
| 향후 추가 가능 | AICC엔지니어링·사업·운영 등 | 현재 미게시 |

**향후 prefix 확장 운영**: (PE) 위주 + 일부 공통 인덱스 유지. AICC·사업·운영팀 합류 시 별도 prefix(`(AICC)`·`(사업)`·`(운영)`)로 게시 가능 — 운영 합의 미완.

## Jira 프로젝트 연계 (메모리 `reference_aice_2026_jira_projects` 기준)

- **(PE)00-01-02. AIDU Agent Studio (Gen1급)** ↔ Jira `AIDUAGTSTD` (AIDU Agent Studio, 2026-05-11 신설)
- **(PE)00-01-03. AIDU agent (개인학습교사)** ↔ Jira `AIDUAGT` (AIDU Agent, 2026-05-11 신설)
- **(PE)00-01-01. 시험지웹전환** ↔ Jira 매핑 미확인 (필요 시 별도 조회)

---

# Routing Hints (PROJECT 카테고리 전용)

본 reference로 라우팅됐을 때 우선 탐색 매트릭스:

| 요청 유형 | 탐색 위치 |
|-----------|----------|
| 스페이스 홈 / 전체 소개 | `782369333` |
| 2026년 AICE 과제 종합 인덱스 (사업·운영 시각) | `784272013` |
| **우리 팀 AICE 과제 부모 (5과제)** | `784080409` ((PE)00-01. AICE) |
| (PE) 시험지웹전환 진행 보고 | `784080537` |
| (PE) AIDU Agent Studio (Gen1급) 진행 보고 | `784080592` (Jira `AIDUAGTSTD` 연동) |
| (PE) AIDU agent (개인학습교사) 진행 보고 | `784081094` (Jira `AIDUAGT` 연동) |
| **(PE) AIDU DesktopApp Update (AWS/Azure 앱 업데이터)** | **`833291198` (신규 5번째 과제)** |
| (PE) 검토 자료 (공통) — 날짜별 검토 누적 | `784081521` |
| (PE) 현황 (개요·시스템 구성도·AIDU 내부구조) | 현황 폴더 `784080425` → CQL `parent = "784080425"` |
| (PO) 요구사항 정의서·기획자료 | 백업 폴더 `836245315` 또는 과제 트리 내 `(PO)` prefix 페이지 |

**소스 링크 포맷**: `[title](https://ktspace.atlassian.net/wiki/spaces/AICEPlatform/pages/{pageId})`

---

# 다른 reference와의 라우팅 경계 (중요)

AICE 자료는 4개 스페이스에 **성격별로 분산**되어 있다. 사용자 쿼리의 성격을 식별해 정확한 reference로 라우팅:

| 사용자 쿼리 성격 | 라우팅 | 이유 |
|---|---|---|
| **공식 산출물·사업팀 공유·진행 보고** ((PE) 5과제, (PO) 요구사항 정의서, 2026년 AICE 과제 인덱스) | **본 reference (project-aiceplatform.md)** | AICE 고도화·운영·사업팀 협업 공식 채널 |
| **팀 내부 회의록·논의·작성중 메모·개인공간 AICE 노트** | `current-platformax.md` (PRIVATE) | 내부 운영·미공개 단계 |
| **AICE 아키텍처·시스템 원본·차세대·관제·25년 사료** | `current-serviceplatform.md` (DEFAULT, 융합팀 트리 `696944019`) | 기술 원본·아키텍처 문서 |
| **25년 AIDUez Flex·정기시험 VoC·FDS 기획 원본** | `legacy-wisepmlife.md` (LEGACY) | TF 시절 historic |

**다중 reference 동시 필요 시** (예: "AICE 시험지웹전환 — 사업팀 보고본 vs 팀 내부 논의 vs 25년 원본"):
- PROJECT(공식 산출물) → PRIVATE(팀 내부) → DEFAULT(아키텍처 원본) → LEGACY(25년 사료) 순으로 결합
- 결과 표기 시 성격·시점 명시 (예: "26-05 AICEPlatform (PE) 시험지웹전환 진행 보고 / 26-04 PLATFORMAX 팀 내부 논의 / 25년 WISEPMLIFE AICE 섹션")

---

# 주의사항

- **트리 확장 중** (2026-06-28 기준 32+페이지, 2026-05-22 생성). depth-3 기획/구현준비 페이지는 본 reference에 부분만 기재 — 세부는 `getConfluencePageDescendants(782369333, depth=3)`로 실시간 확인
- **홈 페이지는 기본 템플릿** — 현재 실질 콘텐츠 없음. 사용자 안내 시 트리 구조 위주로 응답
- **(PE) prefix 외 다른 팀 prefix**는 현재 미존재. 운영 합의 진행 중 — 페이지 prefix가 늘면 6팀 매핑표 갱신
- **폴더(`type=folder`) 페이지**는 `getConfluencePageDescendants` 직접 호출 시 404 가능 → CQL `parent = "<folderId>"` 우회 ((PE)00-01-00 현황 폴더 `784080425` 해당)
- **사업팀 시각의 페이지**(`(PE)` prefix 없는 페이지)는 다른 부서 작성물 — 인용 시 작성자·부서 명시 권장
- **본 스페이스는 PROJECT 협업 공간** — 우리 팀이 깊게 소속이지만 소유 부서 아님. 페이지 게시·수정 정책은 스페이스 소유자(장수림·DevOps엔지니어링팀)와의 합의 필요

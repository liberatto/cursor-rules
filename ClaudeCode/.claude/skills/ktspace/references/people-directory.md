# KT Space 인물·참여인력 디렉토리 (Cross-cutting)

> 프로젝트·팀별 참여인력 + **accountId 매핑 SoT**. 평면 모드의 작성자 검색(`creator=`/`reporter=`)이 이 표를 키로 쓴다.
> 트리거: "누가 ~과제 참여", "작성자/담당자로 찾기", "OOO 소속", "OOO이 작성한 글", "PO/PM이 누구" → 이 파일에서 accountId 확보 후 `creator = "<accountId>"` CQL / `reporter = "<accountId>"` JQL 실행.
> ⚠ accountId 미상 인물은 이름으로 검색하되 **동명이인 주의** — 확보되는 대로 본 표에 채워 SoT화.
> Last-verified: 2026-06-28

---

## 사용방법 (accountId → 검색)

```sql
-- Confluence: 특정 인물 작성물 (전사 또는 스페이스 한정)
creator = "<accountId>" ORDER BY lastModified DESC
space = "<KEY>" AND creator = "<accountId>" ORDER BY lastModified DESC

-- Jira: 특정 인물 보고/할당 이슈
reporter = "<accountId>" ORDER BY updated DESC
assignee = "<accountId>" ORDER BY updated DESC
```

accountId 없으면: Rovo 자연어 검색 → 결과 author로 accountId 역추출 → 본 표에 보강.

---

## 1. 우리 팀 — 플랫폼엔지니어링팀 (8명)

조직: KT > IT부문 > IT플랫폼본부 > 서비스플랫폼담당 > 플랫폼엔지니어링팀. 담당 상무 = 박기철 상무님.

| 이름 | accountId | 역할/그룹 | 주요 참여 과제 |
|------|-----------|----------|---------------|
| **박성수** (팀장=본인) | `557058:609d38c5-afeb-4836-b3d4-2615dd0529bf` | 팀장 | (전역) · AIDD 챕터총괄 · AICE PRD |
| 박대흠 | `712020:90005aef-1f97-4a01-923d-da8d425bef2d` | DA | DA 과제 · park.deaheum@kt.com |
| 김영진 | `712020:521fc391-2f63-432b-9241-39ade70cd371` | DA | DA 과제 · yjin99.kim@kt.com ⚠ 동명이인 17명(인프라소싱구매팀 등 배제) |
| 유정아 | `712020:358a0044-c5e7-49c4-aba2-4c08f9664e42` | DA | DA 과제 · STL 이관(융합팀 연관) · ja.ryu@kt.com ⚠ 동명이인 2명(대구전송망기술팀 `d19fa010-...` 배제) |
| 이근모 | `712020:46816c53-2025-4f3d-bb50-c937ab9c325e` | DA | DA 과제 · STL 이관(융합팀 연관) · yi.geunmo@kt.com |
| 한준상 | `712020:a3e6c497-94fc-4785-8363-02cd2aee6a4c` | AICE | Agent Studio 일정·인프라 · AIDD 운영지원 · joonsang.han@kt.com |
| 황범 | `712020:db577877-59b6-4347-a2aa-127dbb3b2f46` | AICE | Agent Studio Agent Spec · **AIDD 챕터리드** · beom.hwang@kt.com |
| 임창용 | `712020:442d4d41-aff5-439a-bc41-80b8f505923a` | AICE | Agent Studio 기획·설계(PM) · AICE 요구사항 정리 · AIDD 운영지원 · cy.lim@kt.com |

> 개인공간(PLATFORMAX): 유정아·김영진·박대흠·임창용·박성수·황범.

---

## 2. AIDU Agent Studio (Gen시험) — 과제별 역할 분담

AICE 생성형(Gen) 등급 신설 시험도구. 1차 Console형(Gen2급, 상용 9/25)·2차 Web형(Gen1급, '27.2월).

| 역할 | 이름 | 소속 | accountId | 비고 |
|------|------|------|-----------|------|
| **사업 PO (총괄)** | 박효진 부장 | AICE기획팀(인재실) | `712020:3ad5b7c6-4f1d-4fe4-ba88-936df0233a75` | 시험기획·문항·채점기준·exam_venue 운영 · hyojin.park@kt.com |
| 사업 PO | 유지영 | AICE기획팀(인재실) | `712020:bddb8f3b-bc28-49f0-9efa-c9066e5a99e5` | jiyoung.yu@kt.com ⚠ 동명이인 2명(소속없는 `17ad77cd-...` 배제) |
| 사업 PO | 최용배 차장 | AICE기획팀(인재실) | `712020:fc7ebf9c-2060-4c96-9fb8-0dda53dd0318` | yb.choi@kt.com |
| **PO (요구사항 작성)** | 정상훈 과장 | AICE기획팀(인재실) | `712020:97f2c440-6e5d-4453-9586-f46e2b34b7c9` ✅ 확인 | 인재실 기획사항 v2·요구사항 정의서 v2.2 직접 작성 · louis.jung@kt.com ⚠ 동명이인 4명(지능망통화플랫폼팀·법인사업이행2팀·시너지영업3팀 배제) |
| **PM (개발↔사업 조율)** | 윤종원 책임 | 융합서비스플랫폼팀 | `712020:bf517513-2fc7-47af-94a1-98c3c33d6f11` | jongwon.youn@kt.com |
| 개발 (기획·설계) | 임창용 | 플랫폼엔지니어링팀 | → §1 | → §1 |
| 개발 (Agent Spec) | 황범 | 플랫폼엔지니어링팀 | → §1 | → §1 |
| 개발 (일정·인프라) | 한준상 | 플랫폼엔지니어링팀 | → §1 | → §1 |
| 포탈연동 | KTDS 인력 | KTDS | _미확인_ | 투입 검토 중(미확정) |

관련 메모리: `project_aice_agent_studio_gen_exam`. Jira: `AIDUAGTSTD`(Agent Studio)·`AIDUAGT`(개인학습교사 Agent, 별개 과제) — ktdevspace 인스턴스.

---

## 2-1. AICE 플랫폼 담당 — 융합서비스플랫폼팀

AICE 플랫폼(고도화·운영) 담당. 윤종원은 AIDU Agent Studio PM(§2)을 겸함.

| 이름 | 소속 | accountId | 이메일 | 비고 |
|------|------|-----------|--------|------|
| 윤종원 책임 | 융합서비스플랫폼팀 | `712020:bf517513-2fc7-47af-94a1-98c3c33d6f11` | jongwon.youn@kt.com | AIDU Agent Studio PM 겸(§2) |
| 조건 | 융합서비스플랫폼팀 | `712020:6da2835a-3e2c-4e42-af75-f3831ebb2637` | kun.joe@kt.com | 동명이인 없음 |
| 전상윤 | 융합서비스플랫폼팀 | `712020:cfae4e32-f7a3-4515-95f6-00a6096d3005` | sangyoon.jun@kt.com | 동명이인 없음 |

---

## 3. AIDD 챕터과제 — 6팀 대표·운영진

서비스플랫폼담당 6팀 × 1과제. 추진 2026-05~09. 챕터총괄 박성수 / 챕터리드 황범 / 운영지원 한준상·임창용.

| 팀 | 과제 | 대표 | accountId |
|----|------|------|-----------|
| 플랫폼엔지니어링 | AIDU Agent(개인 맞춤 학습) | 임창용 책임/PM | `712020:442d4d41-aff5-439a-bc41-80b8f505923a` |
| 융합서비스플랫폼 | 발전량 예측 소스 리팩토링 | 안서연 선임/Dev | `712020:3b786d04-ef55-4794-bde8-791d961a8f08` |
| 고객서비스플랫폼 | Voice Agent E2E PoC | 임윤재 책임/PM | `712020:d6081ee3-0107-442e-bf33-ab44b5efc898` |
| 커넥티드플랫폼 | AI Glasses Agent MVP | 남우진 책임/PM | `712020:9c2478d7-eb5c-4db9-9847-30d359ef64ec` |
| 모빌리티플랫폼 | GIS 검색 API AIDD 내재화 | 조홍범 책임/PM | `712020:2906230d-14e1-4688-bb91-f7ad821b806d` |
| AICC엔지니어링 | Voice Agent Platform OSS PoC | 윤금성 책임/Dev | `712020:2bf90c26-36e6-4db7-87ed-e35b8b08b72d` |

관련 메모리: `project_aidd_chapter_mission`.

---

## 4. 서비스플랫폼담당 조직 (6팀)

담당 상무 = **박기철 상무님**.

| # | 팀 | 핵심 인물 | accountId | 이메일 |
|---|----|----------|-----------|--------|
| 1 | 융합서비스플랫폼팀 | **이승진 팀장** | `712020:5d126f19-fea9-4603-bd5b-79fc10b42a46` | jinny.lee@kt.com ⚠ 동명이인 3명(AX신사업개발팀·부산IP망 배제) |
| 1 | 융합서비스플랫폼팀 | **박강구** 책임(SPOT·에너지·태양광 발전량 예측) | `712020:7155f773-69e4-43b6-a616-efec83295d52` | kanggu.park@kt.com · 재생E(태양광) 발전량 예측 PoC·SPOT/TimesFM, 우리 팀과 공동 PoC 합의(`project_renewable_energy_forecast_park_kanggu`) |
| 1 | 융합서비스플랫폼팀 | **안서연** 선임 | `712020:3b786d04-ef55-4794-bde8-791d961a8f08` | seoyeon.ahn@kt.com |
| 2 | 고객서비스플랫폼팀 | **임윤재** 책임 | `712020:d6081ee3-0107-442e-bf33-ab44b5efc898` | yoonjae.lim@kt.com |
| 3 | AICC엔지니어링팀 | **김민우** | `712020:3eafa2ae-6df3-402d-98dd-6b66ab4d7645` | kim.minwoo@kt.com ⚠ 동명이인 4명(IT역량팀·무선요금기획팀·휴직&기타 배제) |
| 3 | AICC엔지니어링팀 | **윤금성** 책임 | `712020:2bf90c26-36e6-4db7-87ed-e35b8b08b72d` | geumseong.yoon@kt.com |
| 4 | 모빌리티플랫폼팀 | **조홍범** 책임 | `712020:2906230d-14e1-4688-bb91-f7ad821b806d` | hongbeom.cho@kt.com |
| 5 | 커넥티드플랫폼팀 | **남우진** 책임 | `712020:9c2478d7-eb5c-4db9-9847-30d359ef64ec` | wj.nam@kt.com ⚠ 동명이인 2명(수원엔지니어링팀 `855dc3e9-...` 배제) |
| 6 | **플랫폼엔지니어링팀** (우리 팀) | 박성수 외 7명 → §1 | → §1 | |
| 담당 상무 | 서비스플랫폼담당 | **박기철 상무님** | `712020:1cca59a6-99e9-4d25-bfcd-eb90e8ff466c` | ray.park@kt.com ⚠ 동명이인 4명(남부산운용팀·고객경영담당·수원IP망 배제) |

관련 메모리: `reference_service_platform_org`. 명칭 변경 매핑은 SKILL.md "명칭 변경 매핑" 표 참조.

---

## 5. DA 7개 과제 — 협업 수요부서

모델 개발=플랫폼엔지니어링(DA), 상용 판단·운영=수요부서.

| 과제 | 협업 수요부서 |
|------|--------------|
| [ITOA] GMMSC 통계 이상탐지 / Communis 로그 이상탐지 | 커뮤니케이션코어플랫폼팀 |
| 인증 FD / 결제 FD / 리스크등급 | **인증금융플랫폼팀** (FD 계열 키 홀더) |
| 트래픽 예측 | 통화지능망플랫폼팀 (이관 완료) |
| ANO 벤치마킹 | — (내부 기술조사) |

관련 메모리: `reference_da_collaboration_teams`. ⚠ 수요부서 인물 accountId 미확보.

---

## 6. 외부 팀 (소속 4스페이스 밖)

### Agentic AICC기술팀 (스페이스 `AXTDT`)

> ⚠ **동명이인 다수 — 반드시 아래 accountId로 필터.**

| 이름 | accountId | 이메일 |
|------|-----------|--------|
| 최수용 | `712020:2354bb54-dff6-4895-96a0-dd928160c9b0` | suyong.choi@kt.com |
| 지관욱 | `712020:5bb47ff9-5b0f-4d20-a4b2-76c721ede0dd` | ji.ku@kt.com |
| 서치원 | `712020:2eef1072-335d-407c-8980-36c83a59e758` | search.one@kt.com |
| 김정택 | `712020:156ace54-f243-4fb8-9e06-86b9b1ace684` | jungtech.kim@kt.com |

관련 메모리: `reference_agentic_aicc_team_members`.

### 기타

| 이름 | 소속 | 비고 | accountId |
|------|------|------|-----------|
| 장수림 | DevOps엔지니어링팀 | AICEPlatform 스페이스 생성자·owner | `712020:316069a2-4d47-42af-bd42-7c9ae4297514` · surim.jang@kt.com _(구 기록 오기 수정: 이전 `bf517513-...`는 윤종원 accountId였음)_ |
| 최지훈 | (미확인) | **전임 팀장** (PO 아님 — 구 오기 주의) | GitHub `jk-choi_ktdev` _(추정)_ |

---

## 갱신 규칙

- accountId를 새로 확보하면(평면 검색·Rovo author 역추출) **즉시 본 표 `_미확인_` 칸을 채운다.**
- 인물 소속·역할 변경 시 본 표 + 해당 메모리 동기화.
- 동명이인 발견 시 반드시 배제 대상 accountId까지 병기.

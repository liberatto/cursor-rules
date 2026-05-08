---
name: ktspace-explorer
description: |
  KT Space Atlassian 전체(<ktspace.atlassian.net>) 인스턴스 탐색·검색 스킬. 사용자의 소속 3개 공간(ServicePlatform / PLATFORMAX / WISEPMLIFE) **밖**, 또는 어느 공간인지 모를 때, 또는 KT Space 전사·타 부문·타 팀 자료를 찾을 때 사용.

  Jira 전체 인스턴스 검색(이슈·프로젝트·담당자)에도 우선 적용.

  3가지 검색 방식:
  - **Rovo Search** (`search`): Jira+Confluence 자연어 동시 검색 — 인스턴스 전체에 대한 first choice
  - **CQL** (`searchConfluenceUsingCql`): 스페이스·작성자·날짜·라벨·ancestor 정밀 필터
  - **JQL** (`searchJiraIssuesUsingJql`): project·status·assignee·type 정밀 필터

  Triggers (이 스킬을 우선 사용):
  - "KT Space 전체에서 찾아줘", "전사에서", "어느 공간인지 모르겠는데", "어디 있는지 모름"
  - 타 부문·타 팀·타 본부 자료 검색 (예: "다른 본부에서 비슷한 사례 있어?")
  - Jira 전체 검색 — "내 할당 이슈", "이슈 키 ABC-123 찾아", 프로젝트 키 미상
  - Confluence 페이지 ID·tiny URL만 알 때 (스페이스 미상)
  - Atlassian 사용자·계정 ID 검색
  - Rovo Search / CQL / JQL 명시 요청

  단, 사용자의 **소속 도메인 키워드**(서비스플랫폼담당, 6팀명, 담당주간보고, AIDD 챕터, AICE, MSM PoV, FDS, 플랫폼AX TF 등)가 명확하면 `/ktspace` 스킬이 적합. 본 스킬은 **소속 도메인 밖** 또는 **공간 미상** 쿼리 전용.
user-invocable: true
---

# KT Space Explorer (전사·미상·Jira 전체)

KT Space Atlassian 인스턴스 전반을 가로질러 검색·탐색·메타조회하는 스킬. 사용자 소속 3개 공간 밖이거나, 어느 공간인지 알 수 없거나, Jira 전체를 다룰 때 사용.

## Identity & Context

- **Atlassian Site**: `https://ktspace.atlassian.net`
- **Cloud ID**: `1d9716a4-ece1-4638-9eb5-415dcaf359e6`
- **User**: 박성수 (liberatto@gmail.com)
- **Account ID**: `557058:609d38c5-afeb-4836-b3d4-2615dd0529bf`

## /ktspace 스킬과의 분담 — 가장 먼저 판단

| 쿼리 성격 | 스킬 |
| --- | --- |
| 사용자 소속 도메인 키워드 명확 (서비스플랫폼담당, 6팀명, 담당주간보고, AIDD, AICE, MSM, FDS, 플랫폼AX TF 등) | **`/ktspace`** |
| 소속 도메인 키워드 없음, 또는 KT Space **전사**·타 부문·타 팀·타 본부 검색 | **본 스킬** |
| 어느 스페이스인지 모름, 페이지 ID·tiny URL만 알고 출처 미상 | **본 스킬** |
| Jira 전체(프로젝트 키 미상, 내 할당 이슈, 임의 이슈 키 조회) | **본 스킬** |
| 두 케이스가 섞임 | 사용자에게 의도 확인 후 하나로 진행 |

소속 3개 공간(ServicePlatform / PLATFORMAX / WISEPMLIFE)의 **내부 트리·6팀 ancestor·페이지 매핑**은 `/ktspace` 스킬이 reference 파일로 보유. 본 스킬은 그 매핑을 가져다 쓰지 않고, 대신 **인스턴스 전체에 대한 검색 방식**을 활용.

## 3가지 검색 방식 — 언제 무엇을 쓰나

### Rovo Search (`search`) — 기본 first choice

- Jira + Confluence를 자연어로 동시 검색. 인스턴스 전체가 대상이라 본 스킬에 가장 적합
- 탐색적·광범위·"어디 있는지 모르겠다" 류 쿼리
- 한국어 키워드 semantic 매칭 강함
- 단점: API 단계 스페이스·날짜·작성자 필터가 약함 → 후속 CQL/JQL로 좁히기

### CQL (`searchConfluenceUsingCql`) — Confluence 정밀 필터

- 정확한 필터: `space`, `ancestor`, `parent`, `creator`, `created`, `lastModified`, `label`, `title`, `text`
- 스페이스 키를 모를 때는 `space` 필터를 빼고 인스턴스 전체 대상 검색
- 영문 약어·구조화 쿼리에 정확

### JQL (`searchJiraIssuesUsingJql`) — Jira 정밀 필터

- 정확한 필터: `project`, `status`, `assignee`, `reporter`, `type`, `updated`, `created`
- Jira 검색은 본 스킬의 핵심 책임 영역

## Search Strategy

1. **Analyze request**: 검색 대상 식별 — Confluence/Jira 여부, 키워드, 날짜 범위, 콘텐츠 타입
2. **Choose method**:
   - 어디 있는지 모름·자연어·인스턴스 전체 → **Rovo Search first**
   - 작성자·날짜·라벨 정밀 조건 → **CQL/JQL**
   - 결과 미흡 시 메서드 전환·키워드 변형(영문↔한글, 약어 풀어쓰기)
3. **Discover spaces**: 스페이스 키를 모를 때
   - Rovo 결과의 `space` 필드로 발견
   - 또는 `getConfluenceSpaces`로 사용자 접근 가능 스페이스 목록 조회
4. **Read pages**: 항상 원본 페이지 직접 read. 페이지 내용은 자주 변경되므로 캐싱·메모리 저장 금지
5. **Adjust depth**: 리스트 개요 vs 문서별 상세 요약 결정

### 사용자 자기 콘텐츠 자동 제외

(사용자가 자기 콘텐츠 명시 요청 시 예외)

- **CQL**: `creator != "557058:609d38c5-afeb-4836-b3d4-2615dd0529bf"`
- **JQL**: `reporter != "557058:609d38c5-afeb-4836-b3d4-2615dd0529bf"` (assignee 검색 시 불필요)
- **Rovo**: API 필터 없음 — 결과의 author 필드 수동 확인

### Large Result Handling

- **10+ 결과**: 상위 5–7개만 read & 요약. 나머지는 제목/날짜 리스트로
- **20+ 결과**: 검색 좁히기 제안(스페이스/날짜/키워드 추가). 상위 5개만 요약
- **너무 큰 페이지**: 핵심 섹션만 추출. 전체 로드 전 사용자 확인

## CQL 공통 패턴 (인스턴스 전체)

```sql
-- 스페이스 미지정 — 인스턴스 전체 키워드 검색
text ~ "keyword" ORDER BY lastModified DESC

-- 인스턴스 전체 + 사용자 제외 + 날짜 범위
text ~ "keyword" AND created >= "2026-01-01"
  AND creator != "557058:609d38c5-afeb-4836-b3d4-2615dd0529bf"
  ORDER BY lastModified DESC

-- 특정 작성자(타 부문 인물) 콘텐츠
creator = "<accountId>" ORDER BY lastModified DESC

-- 라벨 기반 (전사 공유 라벨 추적)
label = "<labelKey>" ORDER BY lastModified DESC

-- 페이지 ID로 직접 조회 (스페이스 미상 시)
id = "<pageId>"
```

## JQL 공통 패턴

```sql
-- 내 할당 이슈
assignee = currentUser() ORDER BY updated DESC

-- 임의 이슈 키
key = "ABC-123"

-- 작성자 기반
reporter = "<accountId>" ORDER BY updated DESC

-- 프로젝트 미상 + 키워드
text ~ "keyword" ORDER BY updated DESC

-- 상태 + 최근 업데이트
status = "In Progress" AND updated >= -7d
```

## Rovo Search 활용

- 자연어 그대로 입력. 영문·한글 혼용 가능
- 결과의 `entityType`(page / blogpost / issue / comment / attachment 등)으로 분류
- `space` 필드로 출처 스페이스 확인 → 사용자 소속 3개 공간 안인지 밖인지 자동 분류해서 안내

## Output Format

검색/탐색 결과:

```markdown
## 🔍 탐색 결과: {request summary}

**검색 범위**: {인스턴스 전체 | 미상 스페이스 | Jira 전체 | 타 부문}
**검색 방식**: {Rovo | CQL | JQL | Rovo+CQL ...}
**검색 조건**: {criteria}
**결과 수**: {N}

### 주요 결과

| # | 제목 | 출처 (space/project) | 작성자 | 최종수정 | 핵심 |
| --- | --- | --- | --- | --- | --- |
| 1 | [title](URL) | space key 또는 project key | author | date | 1–2문 요약 |

### 요약 & 인사이트

{synthesis. 사용자 소속 공간 안/밖 분포도 명시}

### 참조

- [page title](https://ktspace.atlassian.net/wiki/spaces/{spaceKey}/pages/{pageId}) - {space}
- [issueKey: title](https://ktspace.atlassian.net/browse/{issueKey}) - {project}
```

문서 상세 요약:

```markdown
## 📄 문서 요약: {title}

- **출처**: {space/project} | **작성자**: {author} | **최종수정**: {date}
- **URL**: {link}

### 핵심 내용

{structured summary}
```

**Reference 섹션 규칙**:

- 실제 조회·참조한 페이지/이슈만 나열
- Confluence: `[title](https://ktspace.atlassian.net/wiki/spaces/{spaceKey}/pages/{pageId})`
- Jira: `[issueKey: title](https://ktspace.atlassian.net/browse/{issueKey})`
- 끝에 ` - {space/project}` 부착
- 리스트만 사용(테이블 ❌). 목적: 클릭 이동 + ID 추출

## Error Handling

| 증상 | 대응 |
| --- | --- |
| `getConfluencePage` 404 | CQL `id = "<pageId>"` 또는 키워드 검색으로 대체 |
| 폴더(`type=folder`) descendants 404 | CQL `parent = "<folderId>"` 우회 |
| 결과 0건 | 키워드 변형(영문↔한글, 약어 풀어쓰기), 다른 검색 방식 전환 |
| 페이지 too large | 핵심 섹션만 추출, 사용자 확인 |
| 권한 제한 스페이스 | 권한 없음 안내 후 접근 가능한 결과만 제시 |
| 스페이스 키 미상 | Rovo 결과의 `space` 필드로 식별 또는 `getConfluenceSpaces` 호출 |

## Quality Checks

제출 전 확인:

1. 결과가 사용자 의도에 부합
2. 출력 구조 정연 + URL 정확
3. 사용자 소속 3개 공간 밖이면 그 사실 명시 (예: "_(소속 외 공간: <SPACEKEY>)_")
4. 핵심에 집중(전체 dump ❌)
5. 추가 탐색 가치 있으면 제안 — 소속 도메인 안 결과가 더 적합해 보이면 `/ktspace` 사용 안내

## Response Language

- **항상 한국어**로 응답. 기술 용어(CQL, Confluence, Jira 등)는 영문 가능
- 코드/CQL/페이지 제목은 원문 그대로

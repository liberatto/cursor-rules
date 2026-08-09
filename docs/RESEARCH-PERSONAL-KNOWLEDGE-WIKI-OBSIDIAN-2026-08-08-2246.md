---
type: research
audience: 사용자·Claude
related_docs:
  - docs/RESEARCH-GRAPH-ENGINEERING-2026-08-08-2220.md (이름이 겹치는 다른 계통 — 에이전트 오케스트레이션 그래프이며 이 문서의 주제가 아니다)
created: 2026-08-08 22:46
measured: 2026-08-08
status: active
description: "권고는 새 도구 도입이 아니라 기존 자산의 가로 연결이다. 사용자가 본 '지식그래프'는 Karpathy가 2026-04-04에 공개한 LLM Wiki 패턴이며, 사용자는 이를 이미 두 번(2026-04-05 Incubation, 2026-05-17 rules) 도입해 두 번 다 하루 만에 멈췄다. 이 문서는 그 패턴의 정체, 현재 도구체인, 반대 증거, 대안을 4개 병렬 조사 트랙으로 확인하고 로컬 도입 이력과 대조해 재도입 타당성을 판정한다."
---

# 개인 지식 위키(LLM Wiki) 도입 타당성 조사

## 1. 결론

**새 도구를 들일 이유는 확인되지 않았다. 결핍은 저장소가 아니라 프로젝트를 가로지르는 연결에 있다.**

조사가 밝힌 것은 세 가지다.

**첫째, 찾던 것의 정체는 특정된다.** "Claude Code와 Obsidian을 결합해 나만의 지식저장소이자 그래프를 만든다"는 내용은 Andrej Karpathy가 2026-04-04 16:25에 GitHub Gist로 공개한 **LLM Wiki** 패턴이다. gist 원문은 *"In practice, I have the LLM agent open on one side and Obsidian open on the other"*라고 적고, 에이전트로 *"OpenAI Codex, Claude Code, OpenCode / Pi"*를 예시로 든다. 별과 포크가 각각 5천 건을 넘겼고 재구현체와 2차 콘텐츠가 4월 이후 쏟아졌다.

**둘째, 이 저장소는 그 패턴을 이미 두 번 실행했고 두 번 다 하루 만에 멈췄다.** `rules/.wiki/`의 골격(`raw/` · `wiki/` · `_index.md` · `log.md`)은 gist가 제안한 구조와 같다. 그리고 Incubation 컴파일 날짜는 gist 공개 **다음 날**이다. 멈춘 이유는 산출물 품질이 아니었다 — 생성된 아티클은 프론트매터에 `confidence`·`volatility`·`verified`를 달고 백링크와 Sources 섹션까지 갖춘 상태였다.

**셋째, 멈춘 진짜 이유는 중복이다.** 이 환경에는 이미 작동하는 지식 시스템이 있다 — 프로젝트 `docs/` 20곳에 문서 261개, auto-memory 139개, `.remember` 세션 히스토리. 위키는 이것들을 **한 번 더 베낀 층**이었고, 원본이 계속 움직이는 한 베낀 층은 즉시 낡는다. 갱신할 이유가 없는 층은 갱신되지 않는다.

따라서 판정은 이렇다. **Obsidian 재도입은 권하지 않는다.** 대신 실제로 아픈 곳 — 프로젝트마다 갈려 서로를 모르는 261개 문서 — 만 겨냥한 최소 개입(§9 옵션 B)을 권한다. 그 개입은 Obsidian도 MCP 서버도 필요로 하지 않는다.

한 가지 사실은 반대 방향을 가리키므로 함께 적는다. 사용자가 쓰던 플러그인 `nvk/llm-wiki`는 **v0.9.0에서 v0.16.0으로 자랐고**(별 935개), 지금은 병렬 다중 에이전트 리서치를 기능으로 내건다. "3개월 전에 써보고 접었다"와 "지금 것은 다른 물건이다"는 동시에 참이다. 그럼에도 판정이 바뀌지 않는 이유는 §4에서 다룬다 — 두 번의 중단은 도구 성능이 아니라 **위키를 읽을 이유의 부재**에서 왔고, 그 이유는 v0.16.0도 만들어 주지 않는다.

---

## 2. 조사 범위와 방법

조사는 2026-08-08에 4개 트랙을 병렬로 수행하고, 여기에 로컬 도입 이력 조사를 더했다.

| 트랙 | 조사 대상 | 주요 산출 |
|---|---|---|
| 1 | 용어·계보·최근 담론 | Karpathy gist를 담론의 기폭점으로 특정, 학술 KG와 Obsidian 그래프뷰의 구분 |
| 2 | Claude Code·Obsidian 실제 도구체인 | MCP 서버 9종 실측(star·최종 push), MCP 없는 접근 3종, AI 플러그인 3종 |
| 3 | 대안·경쟁 접근 | 에이전트 메모리 4종, 노트앱 6종, 로컬 GraphRAG 4종 비교 |
| 4 | 반대 증거 전담 | PKM 비판, AI 오염, 그래프 무용론, 유지비, 보안 CVE |
| 로컬 | 이 환경의 도입 이력 | 두 차례 시도의 시점·규모·중단 지점, 현존 지식 자산 규모 |

트랙 4는 **장점을 찾지 말고 반대 근거만 모으라**는 지시로 운영했다. 결론이 조사 설계 단계에서 한쪽으로 기울지 않게 하기 위해서다.

결론을 떠받치는 수치는 트랙 보고를 그대로 싣지 않고 직접 재확인했다.

- Karpathy gist의 공개 시각·별·포크 수, gist 원문의 Obsidian 언급 — gist 페이지 직접 열람.
- `nvk/llm-wiki`의 현재 버전과 별 수 — 저장소 페이지 직접 열람.
- Viget 사례의 토큰·비용 수치 — 원문 직접 열람으로 인용 확인.
- CVE-2025-52882의 점수·영향 버전·수정 버전 — NVD 페이지 직접 열람.
- 로컬 문서·메모리 개수 — 두 가지 다른 방법으로 세어 대조(§4).

---

## 3. 찾던 것의 정체 — Karpathy LLM Wiki

### 3.1 패턴

gist가 제안하는 것은 RAG의 대안이다. 질의 때마다 원문을 검색해 던지는 대신, **LLM이 마크다운 위키를 지속 편찬해 누적 자산으로 만든다.**

```
    수집                 편찬                   조회
 ┌──────────┐       ┌──────────┐         ┌──────────────┐
 │  raw/    │──────▶│  wiki/   │◀───────▶│  LLM 에이전트 │
 │ 원본     │ 컴파일 │ 개체 페이지│  질의   │ (Claude Code)│
 │ (불변)   │       │[[위키링크]]│         └──────────────┘
 └──────────┘       └────┬─────┘
                         │ 시각화·편집
                    ┌────▼─────┐
                    │ Obsidian │  ← IDE 역할. 저장 형식이 아니다
                    └──────────┘
   index.md — 목차       log.md — 연대기
```

여기서 Obsidian의 자리를 정확히 볼 필요가 있다. **Obsidian은 저장 형식이 아니라 편집기다.** 위키의 실체는 평범한 마크다운 파일 폴더이고, Obsidian은 그것을 그래프로 그려 보여줄 뿐이다. Obsidian 없이도 패턴은 성립한다.

### 3.2 용어 정정 — 이것은 지식그래프가 아니다

찾던 단어가 "지식그래프"였으므로 짚어야 한다. 학술·엔터프라이즈의 지식그래프(Knowledge Graph)는 RDF 트리플과 온톨로지(OWL)로 개체와 **관계에 타입과 의미를 부여**하고, 그 위에서 추론과 SPARQL 질의를 돌리는 구조다. Obsidian 그래프뷰는 `[[위키링크]]`를 노드와 엣지로 그린 것으로 **링크에 타입이 없다** — A와 B가 이어졌다는 사실만 있고, 어떤 관계인지는 기록되지 않는다.

이 구분은 실무자들도 인정한다. Obsidian을 개인 지식그래프로 만들려면 빠진 한 가지가 **타입화된 링크(typed links)**라는 지적이 대표적이다. 그럼에도 커뮤니티와 마케팅 언어에서는 둘이 자유롭게 섞여 쓰인다 — 예컨대 `AgriciDaniel/claude-obsidian`은 스스로를 "connected knowledge graph of plain Markdown"이라 부르지만 실질은 위키링크 마크다운 모음이다.

같은 이름을 쓰는 세 번째 계통도 있다. 며칠 전 조사한 **그래프 엔지니어링**(→ `docs/RESEARCH-GRAPH-ENGINEERING-2026-08-08-2220.md`)은 에이전트 실행 흐름을 명시적 그래프로 설계하는 관행이며, 이 문서의 주제와 무관하다. 세 계통을 한 단어로 부르는 관행이 혼동의 원인이다.

---

## 4. 이 저장소의 도입 이력 — 두 번 시작해 두 번 멈췄다

로컬 파일시스템에서 확인한 사실이다.

| 시도 | 착수 | 도구 | 규모 | 마지막 활동 | 현재 |
|---|---|---|---|---|---|
| 1차 | 2026-04-05 | `llm-wiki-compiler` v1.0.0 (로컬 마켓플레이스) | 소스 60개 → 토픽 9개 | 2026-04-05 | `Incubation/docs/wiki/` 그대로 정지, 재컴파일 0회 |
| 2차 | 2026-05-17 | `wiki@llm-wiki` v0.9.0 | 소스 11개 → 아티클 9개 | 2026-05-17 | 2026-05-23 커밋 `9684191`에서 `.gitignore` 처리 |

```
2026-04-04  Karpathy gist 공개 (16:25)
    │  하루
2026-04-05  1차 도입 — Incubation, 60소스→9토픽 ──▶ 이후 활동 없음
    │  6주
2026-05-17  2차 도입 — rules/.wiki, 11소스→9아티클 ──▶ 이후 활동 없음
    │  6일
2026-05-23  .gitignore 등록 (사실상 폐기)
    │  11주
2026-08-08  현재 — 재검토
```

**중단 원인은 산출물 품질이 아니다.** `.wiki/wiki/concepts/claude-md-context-engineering.md`를 열어 확인한 결과, 프론트매터에 `confidence: high`·`volatility: warm`·`verified` 필드를 갖추고, 본문에 See Also 백링크 7개와 Sources 3건을 단, 그대로 읽을 만한 아티클이었다. 컴파일러는 제 일을 했다.

**중단 원인은 중복이다.** `.wiki/raw/` 11개 소스의 `source` 필드를 전수 확인하면 드러난다.

| 소스의 출처 | 건수 | 이 저장소에 이미 있던 내용인가 |
|---|---|---|
| `docs/` 문서를 직접 지목 | 5 | 그렇다 |
| 저장소 파일(`ClaudeCode/CLAUDE.v.2.3.md`)·수동 작성 매니페스트 | 2 | 그렇다 |
| 외부 웹(블로그·공식 문서·트위터) | 3 | 그렇다 — 같은 주제가 이미 `docs/`에 GUIDE로 정리돼 있었다 |
| 외부 웹(Reddit 치트시트) | 1 | 아니다 |

즉 11개 중 **10개는 이미 저장소가 갖고 있던 내용**이었고, 순수하게 새로 들어온 것은 1개뿐이다. 위키는 원본 위에 얹힌 두 번째 사본이었고, 원본이 계속 움직이는 이상 사본은 쓰는 즉시 낡기 시작했다. 이 구조에서 위키를 읽을 이유는 생기지 않는다.

`log.md`가 이를 그대로 증언한다. 기록된 활동은 init 1회, ingest 2회, compile 2회, **query 2회**다. 만들기는 다섯 번 했고 쓰기는 두 번 했다.

### 4.1 실제로 지식이 쌓여 있는 곳

| 자산 | 규모 | 성격 |
|---|---|---|
| 프로젝트 `docs/` | 디렉토리 20곳 · 문서 261개 | 프로젝트별 정식 산출물, git 추적 |
| auto-memory | 프로젝트 15곳 · 파일 139개 | 세션 간 사실 기억, 머신 로컬 |
| `.remember` | now/today/recent/archive 계층 | 세션 활동 히스토리 |
| `.wiki` | 아티클 9개 | 정지 상태 |

문서 261개는 두 가지 방법으로 세어 대조했다. 디렉토리별 집계 합은 261, 경로 패턴 전수 검색은 263이었고, 차이 2건은 `Incubation/docs/wiki/`의 `INDEX.md`와 `compile-log.md` — 다름 아닌 1차 시도의 잔해였다. 위키 산출물을 제외한 실제 문서 수는 **261개**다.

이 표가 결론의 근거다. **저장소가 없어서 겪는 불편이 아니다.** 겪는 불편이 있다면 261개 문서가 프로젝트 경계로 갈려 서로를 모른다는 것이고, 이것은 새 vault를 만든다고 해결되지 않는다 — 새 vault는 262번째 자리를 만들 뿐이다.

---

## 5. 도구체인 현황 — 지금 다시 한다면

### 5.1 MCP 서버 (2026-08-08 실측)

| 서버 | Star | 최종 push | REST 플러그인 필요 | 판정 |
|---|---|---|---|---|
| `MarkusPfundstein/mcp-obsidian` | 4,277 | 2026-05-15 | 필요 | 최다 채택, 도구 7종 |
| `basicmachines-co/basic-memory` | 3,606 | 2026-08-06 | 불필요 | 가장 활발, Obsidian 자체가 선택 사항 |
| `bitbonsai/mcpvault` | 1,598 | 2026-08-06 | 불필요 | 파일시스템 직접, 도구 16종 |
| `cyanheads/obsidian-mcp-server` | 652 | 2026-08-02 | 필요 | 활성, 도구 14종 |
| `StevenStavrakis/obsidian-mcp` | 720 | 2025-06-23 | 불필요 | 1년 넘게 정체 — 신규 채택 비권장 |
| `iansinnott/obsidian-claude-code-mcp` | 328 | 2025-06-27 | 불필요(플러그인형) | 1년 넘게 정체 — 신규 채택 비권장 |
| `newtype-01/obsidian-mcp` | 311 | 2025-08-04 | — | 1년 정체 |

기반이 되는 `coddingtonbear/obsidian-local-rest-api`(별 2,765, 최종 push 2026-08-03)는 활성이고, 최근 **자체적으로 MCP 엔드포인트를 내장**하기 시작했다. 이 방향이 굳으면 위 표의 별도 MCP 서버 상당수가 불필요해진다.

여기서 읽어야 할 것은 개별 순위가 아니라 **별 수와 생존이 어긋난다**는 사실이다. 별 720개짜리가 1년 넘게 멈춰 있고 별 1,598개짜리가 어제도 커밋된다. 채택 기준을 별로 잡으면 죽은 프로젝트를 고른다.

### 5.2 MCP 없이 하는 방법

Obsidian vault는 마크다운 폴더이므로 Claude Code가 그냥 읽고 쓸 수 있다. 실제 사례에서 확인된 세 갈래와 각각의 함정은 다음과 같다.

- **vault 루트에서 Claude Code 실행** — 플러그인 없이 `CLAUDE.md`로 vault 규칙을 통제한다. 보고된 문제는 수천 노트에서 컨텍스트 초과, 그리고 `CLAUDE.md`의 "Active Context" 섹션을 갱신하지 않으면 응답이 어긋나는 drift다.
- **Claude Desktop의 Filesystem 커넥터** — 설정에서 vault 폴더를 지정하면 끝난다. 결함이 명확하다. OS 레벨 파일 조작이라 Obsidian의 링크 갱신 이벤트를 받지 못해, **리네임·이동 시 `[[위키링크]]`가 깨진다.** 원 저자의 권고는 inbox와 초안만 맡기고 그래프에 얽힌 노트는 건드리지 말라는 것이다.
- **Obsidian 공식 CLI(1.12+)** — 100개 넘는 커맨드를 제공하며 이를 감싼 MCP도 등장했다.

### 5.3 Obsidian AI 플러그인 (2026-08-08 실측)

| 플러그인 | Star | 최종 push | Claude 연동 |
|---|---|---|---|
| `logancyang/obsidian-copilot` | 7,525 | 2026-08-08 | 최신 Anthropic 모델 포함, 공식 REST API 내장 MCP와 통합 방향 |
| `brianpetro/obsidian-smart-connections` | 5,346 | 2026-08-06 | 로컬 임베딩 기반 연결 제안 |
| `nhaouari/obsidian-textgenerator-plugin` | 1,972 | 2026-08-06 | 멀티 프로바이더 |

셋 다 활성이다. 이 영역의 도구 가용성은 문제가 아니다.

---

## 6. 반대 증거

트랙 4가 전담해 모은 근거를 강도별로 정리한다. **강도 구분이 핵심이다** — 아래 대부분은 실무자 일화이지 통제된 연구가 아니다.

### 6.1 AI가 만든 노트가 저장소를 오염시킨다 (일화 · 구체적)

가장 정확히 겨냥된 비판은 "Keep AI Out of Your (Obsidian) Vault" 한 편이다. 네 갈래 주장을 편다.

- **AI 슬롭 축적** — 생성된 요약이 검색을 소음으로 채우고, 자기가 강조했을 지점과 다르게 강조돼 결국 원문을 다시 읽게 만든다.
- **저자성 상실** — 시간이 지나면 이게 자기 생각이었는지 AI 생각이었는지 구분되지 않는다.
- **연결 형성의 붕괴** — 노트 사이 링크를 AI가 자동으로 만들면, 몇 년 뒤 사람이 손으로 링크를 발견하며 얻는 통찰 과정 자체가 사라진다.
- **귀결 예측** — 노트를 전부 AI로 생성하면 명료함과 통찰이 줄고 결국 유지를 멈추게 된다.

저자의 대안은 **AI를 조회에만 쓰고 연결과 태그는 손으로 붙이는 것**, 그리고 AI 생성물은 별도 vault에 격리하거나 라벨링하는 것이다. 이 문서 §9의 권고와 방향이 같다.

### 6.2 그래프뷰는 일정 규모를 넘으면 탐색 도구가 아니다 (커뮤니티 컨센서스)

force-directed 배치가 노드를 밀집 클러스터로 밀어넣어 "보기에는 인상적이나 탐색에는 거의 쓸모없다"는 비판이다. 제시된 기준은 **노트 200개 이상에서 심화되고 50개 미만에서만 실제 가치가 있다**는 것이다. r/ObsidianMD에서 "보기는 재밌지만 탐색은 안 된다"가 다수 의견으로 형성돼 있다.

쟁점을 정확히 하면 갈리는 지점이 보인다. **전체 그래프와 로컬 그래프는 평가가 다르다.** 전체 그래프에 대한 회의론이 우세한 반면, 현재 노트 주변만 보여주는 로컬 그래프는 "거의 마법 같다"는 호평이 있다. 즉 무용론의 대상은 그래프 개념이 아니라 **전체 그래프 시각화**다.

"링크가 실제 회수 성능을 높이지 않는다"는 통제 실험은 조사에서 발견되지 않았다. 있는 것은 실무자 관찰뿐이다.

### 6.3 PKM 자체가 정교한 미루기라는 비판 (개념 · 일화 누적)

**수집가의 오류(Collector's Fallacy)** — 저장하는 행위 자체가 "이해했다"는 착각을 만들어, 뇌가 저장을 완료로 등록해 버리고 미처리 아카이브만 쌓인다. **정교한 미루기(sophisticated procrastination)** — 폴더 구조·태그 분류·자동화 워크플로 구축이 생산성의 언어를 입은 미루기라는 지적이 여러 저자에게서 독립적으로 반복된다.

이 저장소 이력은 이 비판에 부분적으로 해당한다. 두 차례 모두 **구축은 완료됐고 사용은 두 번의 query에서 멈췄다**(§4).

### 6.4 유지비용 (일화 다수)

Obsidian 업데이트마다 플러그인이 깨질 수 있고, 사용자가 플러그인 추적·업데이트 확인·업데이트 후 테스트·방치된 플러그인 대체·충돌 해결까지 떠안는다는 서술이 여러 곳에서 반복된다. "노트 앱이 시스템 관리 업무로 변질된다"는 표현이 나온다. iCloud와 Obsidian Sync가 같은 파일을 동시에 관리하려다 충돌하는 사례도 포럼에 보고돼 있다.

### 6.5 보안 — 근거는 가장 강하지만 해석에 주의가 필요하다

실제 CVE가 존재한다. **CVE-2025-52882**를 NVD에서 직접 확인했다.

| 항목 | 값 |
|---|---|
| 내용 | Claude Code 확장이 웹소켓 연결을 검증하지 않아, 악성 웹페이지가 인증 없이 연결해 MCP 명령을 주입 가능 |
| CVSS 4.0 | 8.8 (HIGH) |
| 영향 | VS Code 확장 0.2.116–1.0.23, JetBrains 플러그인 0.1.1–0.1.8 |
| 수정 | VS Code 1.0.24 이상, JetBrains 0.1.9 이상 |
| 공개 | 2025-06-24 |

**이 CVE는 1년 넘게 전에 패치됐다.** 따라서 오늘의 위험 근거로 그대로 쓰면 과장이 된다. 이것이 말해 주는 것은 특정 취약점의 잔존이 아니라 **에이전트에 파일시스템 접근을 주는 구조 자체가 공격면**이라는 사실이다. 같은 계열로 CVE-2025-54794/54795(경로 제한 우회·명령 주입), Anthropic 공식 Git MCP 서버의 프롬프트 인젝션 3중 취약점이 보고됐다.

구조적 위험 하나는 이 주제에 특히 들어맞는다. **간접 프롬프트 인젝션** — 마크다운 문서에 숨긴 지시를 LLM이 데이터가 아니라 명령으로 처리하는 공격이다. Obsidian vault는 마크다운 파일 더미이므로, 외부에서 받아 vault에 넣은 노트가 그대로 공격 벡터가 된다. 다만 **vault를 경유한 실제 사고 사례는 조사에서 발견되지 않았다** — 기법의 존재는 확실하고, 이 경로로 당한 사례는 미확인이다.

---

## 7. 규모가 커질 때의 비용

| 출처 | 수치 | 신뢰도 |
|---|---|---|
| Viget 실험 | 노트 3,000~4,000개에서 툴 콜·토큰 급증. 유튜브 영상 요약 1건에 **약 50만 토큰 · $1.02** | 원문 직접 확인, 저자 자신의 `ccusage` 측정 |
| Medium 사례 | vault 전체 MCP 스캔 시 쿼리당 약 700만 토큰 대 ripgrep 타겟 검색 약 100토큰 | **미검증** — 재현 수단 없음, 과장 가능성 |
| starmorph 가이드 | 고아 노트 찾기에서 grep 15.6초 대 Obsidian CLI 0.26초 | **미검증** — 블로그 자체 벤치마크, 제3자 확인 없음 |

Viget 저자의 결론도 함께 인용한다. *"I don't feel we're at the point where I'd blindly trust AI-generated code on a high-stakes client project. But for a lower-risk project ... it's a fast path from idea to finished product."*

여러 소스가 공통으로 권하는 아키텍처는 같다 — 로컬 임베딩(Ollama + `nomic-embed-text`)으로 벡터 인덱스를 만들고, Claude에는 상위 5~20개 청크만 주입한다. 다만 **이 저장소 규모(문서 261개)는 위 임계값 어디에도 도달하지 않는다.** 3,000개에서 나타나는 문제는 261개에서 나타나지 않으므로, 벡터 인덱스 구축은 지금 시점에서 해결할 문제가 없는 해법이다.

---

## 8. 대안 비교

파일을 그대로 두고 접근성만 더하는 쪽과, 파일을 떠나 구조화된 저장소로 옮기는 쪽으로 갈린다.

| 접근 | 대표 | 개인 규모 적합성 | 판정 |
|---|---|---|---|
| 마크다운 + git + grep | 현재 이 저장소 방식 | 구독료·종속 없음, 이식성 검증됨 | 이미 채택 중 — 결핍은 포맷이 아니라 가로 연결 |
| Claude Code auto-memory | 공식 기능 | `MEMORY.md` 인덱스 + 주제별 파일, 온디맨드 로드 | 이미 채택 중(파일 139개), 머신 로컬이라 기기 간 동기화 없음 |
| Obsidian + MCP | §5.1 서버들 | 그래프뷰·백링크 UI 추가 | 파일 포맷은 그대로 — 얻는 것은 시각화, 잃는 것은 유지비 |
| Anytype | 공식 MCP(도구 34종) | 로컬 우선 + E2E 암호화 | 로컬 우선을 지키는 유일한 대안이나 이주 비용이 크다 |
| Notion / Capacities / Tana | 클라우드 | MCP·AI 내장 | 클라우드 종속, 로컬 파일 포기 |
| Logseq | DB 버전 전환 중 | 2.0 베타가 SQLite를 정본으로 전환 | 마크다운 유지하려면 구버전 고정 — 지금 진입할 시점이 아니다 |
| Cognee / Graphiti | 진짜 그래프 저장소 | 문서 인제스트 + 그래프 구조 | 셀프호스팅 운영 부담이 개인 규모에서 정당화되지 않음 |
| GraphRAG 계열 | MS GraphRAG / LightRAG | 500페이지 인덱싱에 $50~200 대 $0.50 | 개인 PKM에는 과잉이 다수 소스의 공통 결론 |

에이전트 메모리 계열(Mem0 62.8k★, Graphiti 29.7k★, Cognee 29.9k★, Letta 24.2k★)은 별 수가 크지만 **1차 설계 목적이 에이전트의 대화 기억**이지 사람이 큐레이션하는 지식 저장소가 아니다. 목적이 다르므로 이 비교에서 대안이 되지 못한다.

---

## 9. 판정과 권고

### 9.1 세 가지 선택지

| 옵션 | 내용 | 드는 비용 | 얻는 것 | 판정 |
|---|---|---|---|---|
| A. 전면 도입 | Obsidian vault + MCP 서버 + 위키 컴파일 재개 | 초기 셋업, 이후 상시 유지(플러그인·동기화·재컴파일) | 그래프 시각화, 자동 편찬 | ❌ 두 번 검증된 실패 경로 — 같은 조건에서 세 번째를 시도할 근거가 없다 |
| B. 최소 개입 | `docs/` 261개를 대상으로 **가로 인덱스 한 장**을 만들고 세션 마감 때 갱신 | 인덱스 1개 생성 + 마감 루틴 한 줄 | 프로젝트 경계를 넘는 검색 진입점 | ✅ 권고 — 실제 결핍만 겨냥하고 새 도구를 요구하지 않는다 |
| C. 유지 | 아무것도 하지 않는다 | 없음 | 없음 | ➖ 결핍이 실재하면 그대로 남는다 |

### 9.2 B를 권하는 이유

결핍의 형태가 그것을 결정한다.

```
현재                              B 적용 후
─────────────────────            ─────────────────────
docs/ ×20   auto-memory ×15       docs/ ×20   auto-memory ×15
  │  ...  │      │  ... │            │  ...  │      │  ... │
  └───────┴──────┴──────┘            └───────┴──────┴──────┘
   서로를 모른다                              │ 참조(복사 아님)
                                    ┌─────────▼──────────┐
   ※ A는 여기에 vault를            │  가로 인덱스 1장    │
     하나 더 붙인다                │ 주제 → 문서 경로    │
     = 262번째 자리                 └────────────────────┘
```

핵심은 **참조이지 복사가 아니라는 점**이다. 두 번의 실패는 원본을 베낀 데서 왔다(§4). 인덱스가 경로만 가리키면 원본이 움직여도 인덱스는 낡지 않고, 낡는 것은 주제 분류뿐이라 갱신 비용이 작다.

Obsidian도 MCP도 필요 없다. Claude Code가 `docs/`를 grep하는 것으로 충분하고, 문서 261개는 컨텍스트 문제가 생기는 규모가 아니다(§7).

### 9.3 그래도 A를 하겠다면 — 중단 조건을 먼저 정한다

세 번째 시도가 앞의 둘과 달라지려면, **읽을 이유**를 구조에 심어야 한다. 조사에서 확인된 조건은 세 가지다.

1. **원본을 복사하지 않는다.** 위키는 `docs/`가 답하지 못하는 것만 담는다 — 프로젝트를 가로지르는 주제, 여러 문서에 흩어진 결론의 종합. 이미 한 문서 안에 있는 내용은 위키에 넣지 않는다.
2. **연결은 손으로 붙인다.** AI에게는 조회와 초안만 맡긴다(§6.1의 권고). 자동 생성된 링크는 통찰을 만들지 않는다.
3. **실패 조건을 미리 적는다.** 예컨대 "4주 안에 query가 10회에 이르지 못하면 폐기한다." 앞선 두 시도의 query는 각각 0회와 2회였다(§4). 이 조건이 없으면 세 번째도 같은 자리에서 멈춘 채 방치된다.

도구를 고른다면 §5.1에서 최종 push가 2026-08 상순인 것들 — `basic-memory`, `mcpvault`, `cyanheads/obsidian-mcp-server` — 로 좁힌다. 별이 많아도 1년 정체된 것은 제외한다.

---

## 10. 확인하지 못한 것

- **HN·Reddit 원문**: WebFetch가 reddit.com 계열 접근을 거부해 커뮤니티 반응은 2차 요약에 의존했다. §6.2의 "다수 의견" 서술은 이 한계를 안고 있다.
- **링크와 회수 성능의 인과**: 그래프 링크가 실제 정보 회수를 돕는지에 대한 통제 연구는 발견되지 않았다. 양쪽 주장 모두 실무자 관찰이다.
- **Obsidian vault 경유 프롬프트 인젝션 실사고**: 기법의 존재는 확실하나 이 경로로 발생한 사고 사례는 찾지 못했다.
- **Claude Code + Obsidian 장기 이탈 후기**: 몇 달 써보고 명시적으로 그만뒀다는 회고는 발견되지 않았다. 조합 자체가 2026년 4월 이후의 신생 트렌드라 아직 축적되지 않았을 가능성이 있다. **이 저장소의 두 차례 이력이 현재 확보된 가장 구체적인 이탈 사례다.**
- **일부 성능 수치**: §7 표의 "700만 토큰", "54배" 수치는 원 출처의 자체 주장이며 재현하지 못했다.

---

## 11. 출처

**1차(직접 열람 확인)**
- [Karpathy — LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [nvk/llm-wiki](https://github.com/nvk/llm-wiki)
- [NVD — CVE-2025-52882](https://nvd.nist.gov/vuln/detail/CVE-2025-52882)
- [Viget — Pointless Explorations of Obsidian + Claude Code](https://www.viget.com/articles/pointless-explorations-of-obsidian-claude-code/)
- [Claude Code 메모리 공식 문서](https://code.claude.com/docs/en/memory)

**도구**
- [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) · [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory) · [bitbonsai/mcpvault](https://github.com/bitbonsai/mcpvault) · [cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server) · [coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api)
- [logancyang/obsidian-copilot](https://github.com/logancyang/obsidian-copilot) · [brianpetro/obsidian-smart-connections](https://github.com/brianpetro/obsidian-smart-connections)
- [anyproto/anytype-mcp](https://github.com/anyproto/anytype-mcp) · [topoteretes/cognee](https://github.com/topoteretes/cognee) · [getzep/graphiti](https://github.com/getzep/graphiti)

**비판·분석**
- [Keep AI Out of Your (Obsidian) Vault](https://www.ssp.sh/brain/using-obsidian-with-ai/)
- [Obsidian's Graph View Is Beautiful and Almost Completely Useless](https://codeculture.store/blogs/developer-culture/obsidian-graph-view-useful)
- [PKM Anti-Patterns](https://www.dsebastien.net/ai-wiki-pkm-pkm-anti-patterns/)
- [Personal Knowledge Graphs in Obsidian](https://volodymyrpavlyshyn.medium.com/personal-knowledge-graphs-in-obsidian-528a0f4584b9)
- [Datadog Security Labs — CVE-2025-52882](https://securitylabs.datadoghq.com/articles/claude-mcp-cve-2025-52882/)
- [The Hacker News — Anthropic MCP Git 서버 취약점 3건](https://thehackernews.com/2026/01/three-flaws-in-anthropic-mcp-git-server.html)

**실사용**
- [30 Days of Claude Code + Obsidian](https://constructbydee.substack.com/p/30-days-of-claude-code-obsidian)
- [Claude Code Inside Obsidian](https://dev.to/numbpill3d/claude-code-inside-obsidian-the-setup-that-10xd-my-thinking-20e8)
- [Obsidian + Claude Code 통합 가이드](https://blog.starmorph.com/blog/obsidian-claude-code-integration-guide)
- [MCP 없이 Claude를 Obsidian에 연결](https://www.xda-developers.com/hooked-up-claude-to-obsidian-without-setting-up-mcp/)

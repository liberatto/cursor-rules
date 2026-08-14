# Rules Repository — 운영 컨텍스트

> Last updated: 2026-08-14

이 저장소는 다른 실제 프로젝트 진행 중 발견되는 개선점을 지속 반영하는 **상시 운영 프로젝트**이다. 특정 목표 완료 후 리셋하지 않고, rolling 방식으로 관리한다.

---

## Design Decisions (확정된 설계 결정)

> 이 저장소 운영에 관한 결정. 향후 세션에서 동일 질문이 나오면 참조.

- **CLAUDE.local.md는 rolling 운영**: 목표 완료 후 리셋하지 않음. Backlog/Recent Changes/Known Issues를 상시 관리
- **CLAUDE.local.md = "session context manager"**: 복수 대화에 걸친 연속 작업 흐름 관리. 완료 항목도 간략 보존
- **Global CLAUDE.md 자동 수정 제외**: `claude.md-update` 커맨드가 `~/.claude/CLAUDE.md`를 자동 수정하지 않음
- **커밋 그루핑 원칙**: 기능 개선 / 신규 추가 / 설정 유지보수로 논리 분리
- **frontmatter `argument-hint` 따옴표 필수**: YAML 특수문자 포함 시 크래시 방지
- **배포는 심링크, 사본 금지** (2026-08-14): 스킬·에이전트·커맨드 모두 루트와 외부 프로젝트가 `ClaudeCode/` 원본을 가리킨다. 절차는 `CLAUDE.md` §배포 규칙·§파일 수정 원칙 참조
- **`prompt-master` 정본은 커스터마이징본**: upstream(`nidhinjs/prompt-master`) 클론이 아니라 Claude Code Edition(한국어 트리거·29 패턴)이 정본. upstream 은 gitlink 고아 상태였어서 제거했고, 필요하면 원격에서 재클론한다
- **`claude-md-audit` 적용 범위는 배포되는 글로벌 지침뿐** (2026-08-14): `ClaudeCode/CLAUDE.v.*.md` 시리즈와 배포본 `~/.claude/CLAUDE.md` 에만 쓴다. 이 저장소 루트 `CLAUDE.md`·`CLAUDE.local.md` 는 배포되지 않아 스킬의 전제(매 턴 상주 비용·편입 게이트)가 성립하지 않으므로 **감사 없이 직접 고친다**
- **`skill-creator` 는 Anthropic 공식판으로 교체 예정**: 현재 `ClaudeCode/` 원본은 곧 삭제한다. 그래서 2026-08-14 심링크 전환 대상에서 제외했다

---

## Recent Changes

### 2026-08-14 (2회차) — doc-writer 정합성 점검·정리

새 세션에서 doc-writer 를 충돌·모호성 기준으로 점검해 4건을 고쳤다. 커밋 2개(`8ccbe9c`, `ca63686`).

| 발견 | 처리 |
| --- | --- |
| 규칙 절 15항목이 전부 본문 재서술이고 2곳 드리프트(NOTE 프론트매터·비유 예외) | 마감 점검 10항목(판정 질문 + 참조)으로 교체 |
| §4 는 ADR 불변인데 프론트매터 예시가 `status: active` ADR 의 본문 편집을 시연 | 예시를 `type: strategy` 로 교체 + ADR 단서 추가 |
| `technical-writer` 가 GUIDE·DOCUMENTATION 트리거 중첩, §1~§5 는 writing-principles 의 출처(문장 4/4 동일) | 삭제(배포처 0곳) |
| agent-studio·bmad2 의 `.agents/skills/doc-writer` 가 08-09 사본으로 잔존 | 심링크 전환 |

**§7 자기 적용 범위를 §7.3(구어·비유·의인화)만으로 확정**했다 — 스킬 파일은 산출물이 아니라 지시문이라 §7.7(제목 dash)·§8(화살표 체인)은 제외한다. 이 결정에 따라 어휘 19곳을 교정했다(줄 기준 — SKILL.md 14·personas 1·ascii-diagrams 1·writing-principles 3).

`갈린다` 계열의 이력을 `git log -S` 로 추적한 결과가 이 회차의 교훈이다. `5f2633c` 가 유입시켰고, **`c5e85b0`("자기 적용" 커밋)은 `가르다` 계열만 고쳐 `갈린다` 를 남겼으며**, 이후 `30be303` 이 추가로 유입시켰다. 즉 자기 적용은 되돌려진 것이 아니라 **처음부터 한 어간을 놓친 것**이고, 놓친 어간은 계속 누적된다. 한국어 활용형이 원인이다 — `손대` 로 grep 하면 `손댄다` 를 못 잡는 것과 같은 구조다.

### 2026-08-14 — 마스터-사본 구조를 심링크로 전환

전 프로젝트에 흩어진 스킬 사본을 원본 심링크로 대체했다. 커밋 9개(`a6a6d3b`~`dd67a2d`), 심링크 22곳.

| 대상 | 범위 |
| --- | --- |
| 루트 `.claude/skills` | 7종 전부 |
| `doc-writer` | axplatform·Incubation·agent-studio·agent-composer-core·bmad2 |
| `ktspace` | 위 5곳 중 axplatform·agent-studio·agent-composer-core·bmad2 + Langgraph-Agent |
| `ktspace-explorer` | agent-studio·agent-composer-core·hybrid-aicc |
| `ktspace-atlassian-explorer` (에이전트) | 루트·axplatform·Incubation·Langgraph-Agent |

**전환 과정에서 원본이 낡아 있던 5건을 역반영했다** — 그냥 배포했다면 `report-style` 배타 규칙, explorer 4공간 서술, 에이전트 4스페이스 체계가 소실됐을 것이다. 이 경험이 `CLAUDE.md` §파일 수정 원칙 2번(배포 전 양방향 대조)의 근거다.

`claude-md-audit`·`excalidraw-diagram-generator` 는 루트에만 있던 것을 `ClaudeCode/` 원본으로 승격했다.

---

## Backlog

- **doc-writer §7.3 grep 자기 점검**: 손으로 짠 패턴이 어간을 놓치는 것이 두 번 확인됐다(`c5e85b0` 이 `갈린다` 를 놓침 · 이번 회차 1차 패턴이 `손댄다` 를 놓침). `report-style/scripts/check.sh` 를 선례로 스크립트화할지 판단 필요 — 그때 **패턴은 §7.3 표에서 생성해야 한다**. 손으로 옮겨 적으면 표와 어긋나 같은 구멍이 재현된다
- **`.agents/skills/` 트리의 소비자 미상**: agent-studio·bmad2 에만 있고 `.claude/skills/` 와 같은 스킬 목록을 미러링한다. 읽는 도구를 확인하지 못해 doc-writer 만 심링크로 돌려 뒀다 — 나머지 스킬도 같은 처리를 할지는 소비자 확인 후 결정
- **아직 사본인 자산**: `Incubation` 의 LangChain/LangGraph 학습 스킬군(4개 프로젝트 공유), `azureml-examples` 12종, `axplatform` 업무 스킬군(`weekly-*`·`monthly-report`·`aidm-assess` 등). 원본화 여부부터 판단 필요
- **`midm`·`voiceintent` 의 구세대 커맨드·에이전트**: `dive2`·`plan2`·`mlops-engineer`·`websearcher` 등. 레거시로 보이나 미확인 — 정리 전 실사용 여부 확인
- **`ktspace-atlassian-explorer` 가 뺀 타 부문 스페이스 키 7종**(`ITPLATFORM`·`ConneKT`·`AITechLab` 등): 07-14 판이 Agent Memory 방식으로 대체했다. 소속 밖 검색 편의가 필요하면 복원 검토

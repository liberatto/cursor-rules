# Rules Repository — 운영 컨텍스트

> Last updated: 2026-08-21

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
- **구판 `v5.4`(폐기) 는 넣었다가 되돌렸다** (2026-08-14) — 현행 `v5.4`(2026-08-18 배포, 한국어 문체 조항)와 다른 변경이다: Rule 5 에 "0건 결과는 부재의 근거가 아니다" 규칙을 넣고 배포까지 했으나(`4c2dc4c`·`1ad4a3c`), 게이트를 다시 돌려 **G3(충족) 탈락**으로 제거했다. 사유 셋 — ① 규칙이 요구하는 "반드시 걸려야 한다고 아는 사례"를 만들 수 없는 경우가 흔하고, 만들 수 있는 사례는 패턴과 같은 맹점을 공유한다 ② 그래서 이번 실패(`갈리`→`갈릴`)를 **그 규칙이 있었어도 못 잡았을 것**이다 ③ 값이 한글·정규식·glob 검색에 몰려 있어 매 턴 상주 비용을 넘지 못한다. 대신 §한국어 검색에 사실로 남겼다. **같은 유혹이 오면 이 항목을 먼저 읽는다** — 특정 사건을 글로벌 패턴으로 승격하려는 충동이 이 저장소의 반복 함정이다
- **`skill-creator` 는 Anthropic 공식판으로 교체 예정**: 현재 `ClaudeCode/` 원본은 곧 삭제한다. 그래서 2026-08-14 심링크 전환 대상에서 제외했다

---

## Recent Changes

### 2026-08-21 (4회차) — v5.7 222줄 표 트리거 되돌림 (같은 필드 → 비교, 버전 유지)

3회차에서 넓힌 표 트리거를 v5.5 이전 문안으로 되돌렸다. 발단은 사용자의 "표가 너무 자주 나온다"는 체감이고, **3회차가 "체감 변화는 미확인 — 관찰해야 안다"고 남긴 그 관찰의 첫 데이터가 이번 세션이다.**

```
as-is(3회차): three or more items sharing the same fields belong in a table,
              with a verdict column when the reader has to choose among them
to-be(4회차): three or more items compared on the same axes belong in a table,
              with a verdict column when the reader has to choose among them
```

3회차가 한 두 가지 변경 중 **트리거만 되돌리고 조건부 판정 열은 지켰다.** 판정 열 완화는 as-is 문안의 G3(충족) 탈락을 고친 부분이라 되돌릴 이유가 없다. 되돌림의 대가는 3회차가 문제 삼았던 것 그대로 — 측정표·대응표가 다시 산문으로 밀린다. 다만 3회차 기록 자체가 근거의 약점을 적어 뒀다: 근거로 든 표 3개가 전부 이 파일의 것인데 Response Discipline 은 `user-facing responses` 한정이라 위반 사례가 아니라 형태의 예시였고, 실제 위반 사례는 0건이었다.

**원인 특정은 세션 표를 기계적으로 세어서 했다.** 트랜스크립트를 파싱해 답변 7개에 표 8개를 확인했고, 넷으로 갈렸다 — 축 매트릭스 3개는 `claude-md-audit` §5 보고 형식이 강제한 것이라 222줄 소관 밖, 감사 2회차의 불변조건 위반 표 1개는 데이터행 2개로 `three or more` 미달이라 규칙 위반(실행 실패, 규칙을 고쳐도 안 잡힘), 나머지 4개가 222줄 발동이다. 그 4개를 구판 트리거(비교)로 재분류하면 10행 모델 비교표만 남고 나머지 셋(청구처 대응표·문턱 해설표·경계선 1건)은 구판에서 발동하지 않는다. 어제 넓힌 것이 오늘 체감된 것이 확인됐다.

**기각 3건.** 모두 같은 세션에서 사용자가 제안했고 감사 결과 보류로 냈다. ① 라벨을 v5.6 의 `Prose first, structure when the content has a shape` 로 되돌리는 안 — `only` 를 잃어 라벨이 단독으로 배타성을 못 갖고, v5.6 은 그래서 `Never impose a shape the content doesn't have.` 를 따로 뒀는데 라벨만 되돌리면 둘 다 사라진다. 나머지 6개 라벨이 전부 단일 주제명인 것과도 형식이 어긋난다. ② 표 조항 통째 삭제 — `Everything else is prose` 가 배타 조항이라 트리거에서 빠지면 허용이 아니라 **금지**로 떨어진다. 223줄 `status tables` 전제와 222줄 끝 `no table` 이 근거를 잃는다. ③ Concise 아웃풋 스타일 문안(`Use headers, tables, and bullet lists only when they carry real structure`)으로 대체 — `real structure` 는 반증 불가능한 내성 판정이라 `The test` 렌즈 ②에서 탈락하고, 앞 문장(`1-3 sentences`)은 v5.6 A건으로 이미 흡수돼 있다. 244줄 Final Gate 6 의 `shape` 참조도 정의를 잃는다.

**세 기각에 공통된 진단**: 라벨은 원칙이고 트리거는 `shape` 의 정의다. `has a shape` 는 그 자체로 순환적이라 판별을 못 하며, 이 실패는 v5.6 회차에서 이미 실증됐다(헤딩이 트리거 목록에 없던 시절, 라벨과 Final Gate 6 이 있었음에도 장문 브리핑이 산문으로만 나왔다). 정의를 지우는 방향의 제안은 전부 같은 자리에서 걸린다.

`check.sh` 3/6/14 로 되돌리기 전과 출력 문자 단위 동일(신규 위반 0건). 222줄 95 → 96단어, 파일 3580 → 3581(+0.03%), 246줄 유지. 버전은 v5.8 로 올리지 않고 v5.7 을 제자리 수정했다(3회차 선례). `~/.claude/CLAUDE.md` 배포 완료, sha1 `af91ddfc…` 바이트 일치 확인. **위 3회차 항목의 트리거 확대 서술은 이 회차로 무효다** — 판정 열 조건부화만 유효하다.

### 2026-08-21 (3회차) — v5.7 222줄 표 트리거 확대 (버전 유지, 제자리 수정)

222줄 표 조항의 트리거가 **비교만 덮고 나열·측정·대응(매핑)을 덮지 않는다**는 것이 발단이다. 뒤의 `Everything else is prose` 가 배타 조항이라, 판정할 것이 없는 표는 전부 산문으로 밀려났다.

```
as-is: three or more items compared on the same axes belong in a table
       with a verdict column
to-be: three or more items sharing the same fields belong in a table,
       with a verdict column when the reader has to choose among them
```

두 곳을 한 세트로 바꿨다. 트리거만 넓히면 대응표에도 판정 열이 강제되어 **G3(충족)에 걸린다** — 그래서 판정 열 요구를 선택 상황으로 한정했다. 반대로 판정 열 요구만 완화하면 트리거가 그대로라 대응표는 여전히 산문이다.

**as-is 쪽이 G3 ❌였다는 것이 이 회차의 핵심 발견이다.** 판정할 것이 없는 표에 판정 열을 요구하는 조건은 충족 불가라, 스킬이 경고한 "규칙 전체의 구속력을 갉아먹는" 형태였다. 근거는 이 파일 자체다 — 표 8개 중 3개(76·145·192줄 — 증감 측정표·발견 목록표·대상-범위 대응표)가 판정 열 없는 형태다. 다만 Response Discipline 은 적용 범위를 `user-facing responses` 로 한정하므로 그 표들은 위반 사례가 아니라 **형태의 예시**다(G1 을 ⚠️ 로 둔 이유).

**기각 1건** — 판정 열을 "판정 또는 시사점"으로 넓히는 안. `판정` 은 표 밖의 결정을 요구해 적을 것이 없으면 그 자리에서 막히지만, `시사점` 은 표 안의 숫자를 말로 옮기는 것만으로 채워진다. 세 문턱 중 **유일한 의미 필터를 자기충족적인 칸으로 바꾸는** 선택이라, 08-21 회차에 관찰 대상으로 남긴 헤딩 트리거(`each needing paragraphs of its own`)와 같은 성질을 하나 더 만든다.

**회색지대 1건 신설, 문구 추가 없이 관찰한다.** 같은 줄의 다이어그램 조항(`a claim about arrangement — where something belongs`)과 원본→배포처 같은 대응표가 겹친다. as-is 에서는 표 트리거에 애초에 안 걸려 충돌이 없었다. `a claim` 이 단수 주장이라 데이터 나열과 구분된다는 독법으로 범위는 좁고, 해소하려면 선후 규칙을 한 절 더 써야 해 G4 에서 회수되지 않는다.

**대가 1건** — 짧은 3항목 답변에 표가 붙어 대화가 딱딱해진다("방금 파일 3개 뭐 고쳤어?" → 문장 셋 대신 3행 표). 축 C 간결 쪽 작음.

**체감 변화는 미확인이다.** 이 세션에서 만든 표 셋이 전부 비교이고 판정 칸이 있어 as-is 위반 사례가 하나도 없었다 — 규칙을 고쳐도 답변이 실제로 얼마나 달라질지는 관찰해야 안다. 달라지지 않는다면 남는 이득은 충족 불가 조항 제거 하나다.

`check.sh` 3/6/14 로 as-is 와 출력 문자 단위 동일(신규 위반 0건). 222줄 88 → 95단어(+8.0%), 파일 3573 → 3580(+0.20%), 246줄 유지. 버전을 v5.8 로 올리지 않고 v5.7 을 제자리 수정했다(사용자 판단). `~/.claude/CLAUDE.md` 배포 완료, sha1 `9594062a…` 바이트 일치 확인.

### 2026-08-21 (2회차) — 글로벌 지침 v5.7 배포 (Response Discipline 중복 제거, 3줄)

기능은 하나도 건드리지 않고 같은 말을 반복하는 자리만 걷어냈다. 발단은 222줄이 길다는 지적이었고, 원인을 재면 **105단어 중 26단어가 같은 명제를 세 번 말하고 있었다**.

| 조각 | 문안 | 역할 |
| --- | --- | --- |
| 라벨 | `structure when the content has a shape` | 명제 1회차 |
| 도입 | `Reach for structure when the content already carries one:` | 명제 2회차 |
| 마감 | `Never impose a shape the content doesn't have.` | 명제 3회차(부정형) |

명제를 라벨의 `only` 한 곳으로 모으고 트리거 셋을 연달아 붙인 뒤 기본형(`Everything else is prose`)으로 닫았다. **트리거 세 개의 조건 문구는 한 글자도 바뀌지 않았다** — 발동 범위 불변이다. `shape` 를 라벨에 남긴 것은 필수였다: 244줄 Final Gate 6 의 `content with a shape of its own is shown in that shape` 가 여기서 정의를 가져온다. 오히려 라벨 바로 뒤에 세 shape 의 열거가 붙어 정의 연결이 원문보다 가까워졌다.

**224줄은 거의 손대지 않았다 — 압축할 것이 없어서다.** 아홉 조각이 각각 다른 일을 하고(원칙·절단 기준·분량 배분·설명 기본값·빈발 위반 열거·과다 절단 하한·형태 규제·턴 말미 범위), 길이가 기능 수에서 나온 것이라 줄이려면 기능을 버려야 했다. 222줄과 정반대 구조다. 잘라낸 것은 `an arrow chain standing in for a sentence` → `arrow chains` 6단어뿐이고, 그마저 같은 절이 `stays in full sentences` 로 시작해 이미 함의된 부분이다.

**진짜 낭비는 227줄에 있었다.** 224줄과 두 지점에서 겹친다 — `cut any detail that wouldn't change what the reader does next` ↔ `Name the sentence the reader acts on` 은 같은 기준의 두 표현이고, `Stop cutting where a first-time reader would lose the thread` ↔ 227줄 꼬리는 문자 그대로 중복이다. 꼬리는 "규칙을 어기면 규칙을 어긴 것"이라는 동어반복이라 `The test` 렌즈 ①(규칙 본문의 재진술인가)에서 탈락한다. 앞부분은 문장을 지목하고 분류하라는 새 동작을 요구하므로 남겼다. 42 → 23단어.

**대가 1건** — 227줄이 절단 방향으로만 작동하게 됐다. 과다 절단 방지는 224줄 `Stop cutting where…` 하나에만 남는다. 반대로 224줄 하한을 빼고 227줄을 두는 선택은 **작성 중 발동하는 지시가 사라지고 사후 점검만 남아** 더 나쁘다고 판단했다.

**하네스 중복 2건은 확인 후 남겼다** — Claude Code 시스템 프롬프트의 `Don't add apologies or preambles` 는 교정 상황 한정이라 224줄 `no greetings, filler, or offers of follow-up` 보다 좁고, `Do not re-derive facts already established` 도 대화 맥락 한정이라 요청 재진술 금지를 덮지 못한다. 둘 다 CLAUDE.md 쪽이 넓어 삭제 대상이 아니다.

**미포함 1건** — 헤딩 트리거에 사후 점검(`a section that came out as a single paragraph loses its heading`)을 붙이는 안을 같은 세션에서 제안했으나 이번 배포에 넣지 않았다. `each needing paragraphs of its own` 이 자기충족적이라는 진단(헤딩을 쓰기로 정하면 문단이 생겨난다)은 유효하니 **관찰 대상으로 남긴다** — 사례가 하나 더 나오면 v5.8 에서 13단어로 넣는다.

| 줄 | as-is → to-be | 증감 |
| --- | --- | --- |
| 222 | 105 → 88 | −16.2% |
| 224 | 143 → 137 | −4.2% |
| 227 | 42 → 23 | −45.2% |
| 파일 | 3615 → 3573 | −1.16% |

246줄 유지, `check.sh` 3/6/14 로 v5.6 과 출력 완전 동일(신규 위반 0건). `~/.claude/CLAUDE.md` 배포 완료, sha1 `b7c36746…` 바이트 일치 확인.

### 2026-08-21 — v5.6 222줄에 헤딩 발동 조건 신설 (버전 유지, 제자리 수정)

다른 세션의 장문 맥락 브리핑(EOS 관련)이 헤딩·표 없이 산문으로만 나온 것이 발단이다. 원인을 지침에서 추적한 결과 **222줄이 그 답변을 막지도, 구조를 요구하지도 않았다** — 헤딩을 언제 써야 하는지 정한 문장이 지침 전체에 없었다.

| 확인한 문장 | 실제 역할 |
| --- | --- |
| 221줄 `Headings carry the flow, not replace it` | 헤딩을 **쓸 때의** 사용법 |
| 222줄 `no headings` | `A simple question` 한정 상한 |
| 223줄 `When headings or status tables are used` | 이미 썼다는 전제 |

Final Gate 6 의 `content with a shape of its own` 도 shape 정의를 222줄에서 가져오는데 222줄이 표·다이어그램만 열거해, 문자 그대로 실행해도 헤딩에 도달하지 않았다. G2 공백 확정.

**구조 억제 3문장(`Prose first`·`Never impose a shape`·`never add structure just to host an emoji`) 대 요구 2문장의 비대칭**이 이 공백의 배경이다. 억제 쪽은 조건 없이 상시 발동하고 요구 쪽은 좁은 조건을 통과해야 해서, 애매한 내용이 전부 산문으로 흘렀다.

채택 문안은 `subjects the user could have asked separately, each needing paragraphs of its own, get one heading each` 다. 원안의 "독립 주제 둘 이상"을 두 번 좁혔다 — ① `could have asked separately` 로 판별을 관측 가능하게, ② `paragraphs of its own` 으로 짧은 답의 오발동을 차단. 후자가 없으면 "원인이 뭐고 어떻게 고쳐?" 같은 세 문장짜리 답에도 헤딩 둘이 붙는다. 수치 상한("N문단 이상")을 피한 것은 의도적이다 — `check.sh` 검사 2 에서 224줄 `a sentence or two` 와 대상 판정을 다투게 된다.

**기각 1건** — 표 트리거를 "속성 나열"까지 넓히는 안은 G4 에서 탈락했다. 속성 넷은 2열 세로 표가 되어 비교를 보여주지 못하면서 같은 줄의 `Never impose a shape the content doesn't have` 와 회색지대만 넓힌다.

**attack 산출물 2건.** ① 223줄 이모지 조항이 문자 그대로는 모든 헤딩을 겨냥해, 헤딩 발동이 늘면 따라 발동한다 — 기존 모호성이고 (a)는 빈도만 올리므로 별건으로 분리했다. ② 발단이 된 답변의 `eos-scope → … → eos-report` 화살표 체인은 222줄·224줄이 이미 금지 중이라 **규칙 공백이 아니라 실행 실패**다. 지침을 늘려 고칠 자리가 아니다.

G3 는 ⚠️ 로 남는다 — `could have asked separately` 판별은 여전히 자기 재량이라, 08-20 A건의 `simple question` 판별과 같은 취약점을 공유한다. **관찰 대상**이다.

`check.sh` 3/6/14 로 as-is 와 완전 동일(신규 위반 0건). 단어 3598 → 3615(+0.47%). 버전을 v5.7 로 올리지 않고 v5.6 을 제자리 수정했다(사용자 판단). `~/.claude/CLAUDE.md` 배포 완료, sha1 `f5ba4dde…` 일치 확인.

### 2026-08-20 (2회차) — v5.5 롤백 후 v5.6 재배포 (왕복, 순변화 없음)

배포본을 v5.5 로 되돌렸다가 같은 세션에서 v5.6 으로 되돌렸다. **현행 배포본은 v5.6**(sha1 `20c1510f…`, 일치 확인)이라 아래 v5.6 항목이 그대로 유효하다.

왕복 중 `ClaudeCode/CLAUDE.v.5.5.md` 가 227줄 `The test` 를 v5.6 문안으로 갖고 있어 버전 순서가 뒤집혀 있었으나, 사용자가 커밋 상태로 되돌려 해소했다(sha1 `5de95b0e…`). 배포 정본인 `ClaudeCode/CLAUDE.v.5.6.md` 는 이 회차에서 추적에 넣었다.

### 2026-08-20 — 글로벌 지침 v5.6 배포 (Concise 스타일 흡수, 3건)

Claude Code 신규 output style `Concise` 의 취지를 Response Discipline 에 흡수했다. 스타일 자체는 켜지 않는다 — 사용자가 config 선택 없이 지침만으로 같은 효과를 원했다.

Concise 6조항을 현행 지침과 1:1 대조한 결과 **4개는 이미 중복, 2개가 공백**이었고, 대조 과정에서 227줄 `The test` 가 224줄의 재진술임을 추가로 발견했다. 채택 3건.

| 건 | 줄 | 변경 | 근거 |
| --- | --- | --- | --- |
| A | 222 | 단순 질문 답변에 `one to three sentences` 상한 신설 | 224줄 `Length is earned by what was asked` 는 언제나 "그렇다"로 답하게 되는 내성 질문이라 관측 가능한 상한이 아니었다 |
| B | 220 | `Never open with process narration` → `Never narrate process` + Final Gate 참조 한정 | 기존 문안이 **첫 문장만** 겨냥해 중간 단계 나열에 발동하지 않았다 |
| C | 227 | `The test` 전면 교체 | `Remove any paragraph and ask what the reader would do differently` 가 224줄 `cut any detail that wouldn't change what the reader does next` 와 사실상 동일 — 검사력 없는 문장이 매 턴 상주 중이었다 |

**기각 1건** — hedging boilerplate 금지(Concise 4)는 219줄 epistemic labeling 과 정면 충돌한다. `likely — because…` 는 hedging 의 형태를 띠지만 필수 라벨이다. 축 C 를 간결 쪽으로 밀다 정직을 깎는 사례.

**보류 2건** — ① 말미 재요약 금지(224줄 `restated in a line each` 의 경계 명시)는 한 문장에 허용·금지가 붙어 판단이 갈려 문안 분리 후 재검토. ② 한국어 평이체 조항 보강은 **08-19 v5.5 실험(종결어미 조항 삭제)을 오염시키므로 결론 후로 미뤘다.**

`check.sh` 3/6/**14** — 검사 3만 1건 늘었고, 220줄이 `trace` 를 새로 참조한 것으로 정의문(235줄)과 대상이 일치하는 정상 참조다. 단어 3562 → 3598(+1.01%).

**검사 2 의 맹점을 확인했다** — 숫자형(`1-3`)만 매칭하고 철자형(`one to three`)은 지나친다. A 가 걸리지 않은 것은 통과가 아니라 미탐이라, 같은 대상의 다른 상한을 눈으로 대조했다(224줄 `a sentence or two` 는 caveat, 17줄은 push back, A 는 단순 질문 답변 전체 — 셋 다 대상이 다름).

**A 의 실효는 `simple question` 판별의 정직성에 달려 있다.** 복잡한 답을 "이건 simple 이 아니다"로 분류해 상한을 매번 빠져나갈 수 있다 — 관찰 대상.

`~/.claude/CLAUDE.md` 배포 완료, sha1 일치 확인.

### 2026-08-19 — 글로벌 지침 v5.5 배포 (한국어 조항 축소, 실험)

v5.4 에서 넣은 Korean 조항(line 225) 중 **종결어미 조항과 명사 나열 조항을 삭제**하고 존댓말·비유 회피만 남겼다. 발단은 대화 답변의 `한 가지 미확정 사항이 남아 있습니다`(20자)였고, 사용자가 `1가지 미확정 사항` 수준의 압축을 막는 지침이 있는지 물은 데서 시작했다.

`claude-md-audit` 결과는 **보류(유지 권고)** 였다. 근거 셋을 기록한다.

| 발견 | 내용 |
| --- | --- |
| 224줄과 중복 | `Concise by selection` 의 `never fragments` 가 이미 명사구 종결을 금지한다. 즉 225줄을 지워도 `미확정 1건` 은 여전히 못 쓴다 — 노린 이득이 나오지 않는다 |
| 조항의 몫은 3자 | 20자 중 `입니다` 3자만 조항 탓이고, 나머지 11자는 응답 장황함이었다. 규칙을 고쳐도 같은 실패가 재현된다 |
| 명사 나열 조항은 공백 | `보고서 작성 일정 확정 필요` 형태는 224줄이 덮지 않아, 삭제하면 순수 공백이 생긴다 |

축 이동은 C(정직↔간결) 간결 쪽 작음, D(통일↔정밀) 통일 쪽 보통이다. 대가는 대화체와 `report-style`(문서 산출물) 의 경계 판정이 224줄의 영어 표현 하나에만 남는 것 — 한국어 개조식이 fragment 인지는 해석이 갈린다.

**그럼에도 사용자 판단으로 적용했다 — 실험 목적이다.** 관찰할 것은 대화 응답이 개조식(`배포 완료, 검증 잔여`)으로 흘러가는지이며, 흘러가면 v5.6 에서 종결어미 조항만 복원한다.

사용자 제안 원문의 `Keeps` 는 `Keep` 으로 고쳤다 — 앞 문장이 `Honorifics always.` 로 끝나 주어가 이어지지 않으므로 명령형이어야 한다.

`check.sh` 출력은 v5.4 와 완전히 동일(3/6/13건)하고, 225줄은 어느 검사에도 걸리지 않는다. 단어 3588 → 3562(−0.72%). `~/.claude/CLAUDE.md` 배포 완료, 바이트 일치 확인.

### 2026-08-18 — 글로벌 지침 v5.4 배포 (한국어 문체 조항)

`fluent-korean` 아웃풋 스타일(플러그인, 714단어)을 실사용했더니 문체는 개선되나 응답이 길어져(스타일 자체 예시로 42자 → 79자, 1.88배) 상시 사용이 불가능했다. 그래서 조항을 **길이 영향으로 분류해 중립인 것만** Response Discipline line 225 에 옮겼다.

| 구분 | 조항 |
| --- | --- |
| 채택 | 종결어미로 문장 끝내기 · 조사·어미로 관계 표시(명사 나열 금지) · 비유적 어휘 회피 |
| 제외 | 문장 성분 생략 금지 · 부사·보조사·보조용언 "적극 활용" — 둘이 길이 증가의 원인 · 엠대시 자제 — 짧은 삽입구를 감쌀 자리가 없어지면 문장이 하나 더 늘어 길이 중립과 어긋난다. 대화에서는 그대로 쓴다(사용자 판단, 08-18). 문서 산출물은 `report-style` 이 ≤1/100줄로 계속 관할 |
| 부분 | 한자어 조항은 "적극 활용"이 `report-style` §2.5(격식 한자어 회피)와 충돌해, 명사 나열 금지 효과만 가져옴 |

미끄럼 방지로 `None of this adds length` 문장을 붙였고, `prose` 한정어로 대화창에 인용하는 보고서 초안(`report-style` 의 명사형 종결 관할)과 경계를 뒀다. 감사 결과는 G1~G4 전부 통과, 축 이동은 D 정밀 쪽 작음뿐, `check.sh` 출력이 v5.3 과 동일해 불변조건 신규 위반 0건이다. 단어 3544 → 3588(+1.24%).

커밋 `8aa9301`, 배포 완료. 플러그인은 삭제하지 않고 `.claude/settings.local.json` 의 `enabledPlugins` 에서 비활성화했다 — 재검토 시 `true` 로 되돌리면 된다.

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

## 한국어 검색 (grep) — 확인된 사실

> 2026-08-14 실측. 글로벌 지침 편입을 검토했다가 게이트 G3(충족)에서 탈락시키고 이 층에 남긴 것이다 — 아래 §Design Decisions 참조.

- **어간 grep은 활용형을 못 잡는다.** 한글은 어미가 붙으면 음절 블록이 합쳐지므로 `갈리` 는 `갈릴` 의 부분문자열이 **아니다**(`리` U+B9AC ≠ `릴` U+B9B4). 도구 문제가 아니라 인코딩의 성질이고, `rg` 에 정규화 옵션은 없다.
- **받침 범위 표현으로 해결된다.** 한글 음절은 `0xAC00 + (초성*21+중성)*28 + 종성` 으로 합성되어 한 음절의 받침 변형 28개가 코드포인트상 연속이다. 따라서 `갈[리-맇]` 이면 갈리·갈린·갈릴·갈림을 모두 잡는다(`리`+27=`맇`, +28은 다음 음절 `마` 라 경계가 정확히 떨어진다). 평범한 정규식이라 `Grep` 도구·`rg` 에서 그대로 쓴다.
  - 한계: **받침이 붙는 활용만** 덮는다. 모음이 바뀌는 활용(`되돌리`→`되돌려`)은 별도 갈래로 적는다.
- **0건을 근거로 쓸 때는 성질이 다른 두 번째 수단으로 확인한다.** 이번에 통한 것은 양성 대조가 아니라 NFD 정규화 재스캔이었다 — 양성 대조는 내가 만든 사례라 패턴과 같은 맹점을 공유해 통과해 버린다(`갈리` 가 `갈리는` 에 1/1 통과).
- **대조를 별도 임시 파일에 돌리면 범위는 검증되지 않는다.** 경로·glob이 틀린 경우는 본 호출과 같은 인자로 돌려야 드러난다.

## Backlog

- **doc-writer §7.3 grep 자기 점검**: 손으로 짠 패턴이 어간을 놓치는 것이 두 번 확인됐다(`c5e85b0` 이 `갈린다` 를 놓침 · 이번 회차 1차 패턴이 `손댄다` 를 놓침). `report-style/scripts/check.sh` 를 선례로 스크립트화할지 판단 필요 — 그때 **패턴은 §7.3 표에서 생성해야 한다**. 손으로 옮겨 적으면 표와 어긋나 같은 구멍이 재현된다. 아래 §한국어 검색의 두 사실을 전제로 삼는다
- **`.agents/skills/` 트리의 소비자 미상**: agent-studio·bmad2 에만 있고 `.claude/skills/` 와 같은 스킬 목록을 미러링한다. 읽는 도구를 확인하지 못해 doc-writer 만 심링크로 돌려 뒀다 — 나머지 스킬도 같은 처리를 할지는 소비자 확인 후 결정
- **아직 사본인 자산**: `Incubation` 의 LangChain/LangGraph 학습 스킬군(4개 프로젝트 공유), `azureml-examples` 12종, `axplatform` 업무 스킬군(`weekly-*`·`monthly-report`·`aidm-assess` 등). 원본화 여부부터 판단 필요
- **`midm`·`voiceintent` 의 구세대 커맨드·에이전트**: `dive2`·`plan2`·`mlops-engineer`·`websearcher` 등. 레거시로 보이나 미확인 — 정리 전 실사용 여부 확인
- **`ktspace-atlassian-explorer` 가 뺀 타 부문 스페이스 키 7종**(`ITPLATFORM`·`ConneKT`·`AITechLab` 등): 07-14 판이 Agent Memory 방식으로 대체했다. 소속 밖 검색 편의가 필요하면 복원 검토

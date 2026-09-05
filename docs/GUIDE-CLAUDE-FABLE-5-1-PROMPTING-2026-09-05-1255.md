---
type: guide
audience: Claude Fable 5.1을 업무 도구·에이전트·자동화에 적용하려는 실무자 (AI 모델 API 경험이 없어도 읽을 수 있도록 작성)
related_docs:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 (1차 출처 — Anthropic 공식 프롬프팅 가이드)
  - https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1 (모델 소개 — 파괴적 변경·신규 기능·가격·가용성)
  - https://platform.claude.com/docs/en/build-with-claude/preserved-thinking (대화 기록 편집 검사 — 3단계 점검 절차)
  - https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback (거부·폴백 처리)
created: 2026-09-05 12:55
updated: 2026-09-05 12:55
status: active
description: "Fable 5용 프롬프트는 5.1에서 대부분 그대로 동작하나, 대화 기록을 고쳐 쓰던 코드는 오류로 막히고 도구 강제 호출은 아예 차단됨. 이 문서는 무엇이 막히는지, 관찰되는 증상별로 어떤 프롬프트 한 줄을 넣어야 하는지, 비용·거부 처리를 어떻게 잡을지를 AI API 경험이 없는 독자 기준으로 정리."
---

# Claude Fable 5.1 프롬프팅 가이드

## 0. 30초 요약

Claude Fable 5.1은 Anthropic이 내놓은 최상위 모델로, 한 번 물어보고 답을 받는 용도가 아니라 **몇 시간짜리 작업을 스스로 이어서 처리하는 용도**로 만들어진 제품. 코드 저장소를 여러 파일에 걸쳐 고치거나, 웹을 여러 차례 검색해 조사 결과를 쌓거나, 문서·스프레드시트·발표자료를 빈 화면부터 완성하는 작업이 대상. 앞 버전인 Fable 5의 후속이며, 같은 값에 캐시 읽기 비용만 4분의 1로 내려감.

**한 줄 결론**: 기존 Fable 5용 지시문은 대부분 그대로 두고 모델 이름만 바꿔도 되지만, **대화 기록을 중간에 고쳐 쓰던 코드와 도구 호출을 강제하던 코드는 오류로 막히므로 이관 전에 반드시 확인 필요**. 나머지는 증상이 보일 때 지시문 한두 줄로 대응.

**반복 용어**

| 용어 | 이 문서에서의 뜻 |
| --- | --- |
| 턴(turn) | 사람의 요청 한 번과 모델의 응답 한 번을 묶은 한 차례. 대화는 턴이 쌓인 목록 |
| 사고 블록(thinking block) | 모델이 답하기 전에 혼자 따져 본 내용이 담긴 조각. 응답에 함께 실려 오며, 다음 요청에 되돌려 보내야 앞서 한 생각이 이어짐 |
| 추론 강도(effort) | 답하기 전에 얼마나 오래 생각할지를 정하는 설정값. `low`·`medium`·`high`·`xhigh`·`max` 다섯 단계, 기본값 `high` |
| 도구(tool) | 모델이 직접 호출하는 외부 기능. 파일 읽기·웹 검색·명령 실행 등을 API 사용자가 정의해 넘김 |
| 에이전트 루프(agent loop) | 모델이 도구를 부르고 그 결과를 받아 다시 도구를 부르는 과정을 답이 나올 때까지 반복하는 구조 |
| 프리픽스(prefix) | 어떤 사고 블록보다 앞에 있는 모든 내용. 시스템 지시문·도구 목록·앞선 대화가 전부 포함 |
| 컴팩션(compaction) | 대화가 길어졌을 때 앞부분을 요약본으로 갈아 끼워 길이를 줄이는 작업 |
| 베타 헤더(beta header) | 아직 정식이 아닌 기능을 쓰겠다고 요청에 붙이는 표시 문자열. 붙이지 않으면 해당 기능이 동작하지 않음 |
| 거부(refusal) | 안전 분류기가 요청을 막았을 때 돌아오는 정상 응답. 오류가 아니라 "답하지 않음"이라는 결과 |
| 폴백(fallback) | 거부된 요청을 다른 모델로 다시 보내 답을 받아내는 처리 |

---

## 1. 모델 기본 제원

- 모델 이름은 `claude-fable-5-1`. 같은 성능의 자매 모델 `claude-mythos-5-1`은 Anthropic의 Project Glasswing 승인 고객 전용이라 일반 계약으로는 사용 불가
- 한 번에 넣을 수 있는 대화 길이(컨텍스트 창)는 100만 토큰이 기본이자 최대이며, 창 전체에 같은 단가 적용. 한 응답으로 뽑을 수 있는 최대 길이는 12만 8천 토큰
- 생각하는 기능(adaptive thinking)은 항상 켜져 있어 끄지 못함. 생각의 양은 추론 강도 설정으로만 조절
- 글자를 토큰으로 세는 방식은 Fable 5와 같음. 다만 Opus 4.7보다 오래된 모델과 비교하면 같은 글이 약 30% 더 많은 토큰으로 계산되므로, 옛 모델 기준으로 잡아 둔 길이 제한과 비용 추정치는 다시 계산 필요
- Claude API 전체 고객이 사용 가능하며 AWS Bedrock·Google Cloud·Microsoft Foundry에서도 제공. 데이터는 30일 보관되고, Anthropic이 별도로 승인하지 않는 한 무보관(zero data retention) 조건 적용 불가

---

## 2. 이관 전 반드시 확인할 파괴적 변경 3건

Fable 5를 쓰던 코드가 모델 이름만 바꿨을 때 **실제로 오류가 나는 지점 세 가지**. 나머지 변경은 전부 추가 기능이라 안 써도 그만이지만, 이 셋은 그냥 두면 요청이 실패.

### 2.1 도구 강제 호출 차단

- **무엇이 막히는가**: 모델에게 "무조건 도구를 불러라"라고 지시하는 설정(`tool_choice`를 `{"type": "any"}` 또는 `{"type": "tool", "name": "..."}`로 지정)이 400 오류로 거부됨. 기본값 `{"type": "auto"}`와 `{"type": "none"}`은 그대로 동작
- **왜 막았는가**: 이 모델은 생각하는 단계를 건너뛸 수 없는데, 도구 호출을 강제하면 그 단계가 생략되면서 모델이 따져 본 내용을 도구 인자 안에 밀어 넣게 되어 인자 품질이 떨어짐
- **대신 무엇을 하는가**: 정해진 형식의 JSON이 필요하면 `tool_choice`는 `auto`로 두고 strict tool use의 `strict: true`를 켜거나 structured outputs로 형식을 지정. 도구를 꼭 부르게 하려면 지시문에 언제 그 도구를 쓰는지 문장으로 적으면 됨(예: `Use the get_weather tool to answer`). 명시적 지시는 안정적으로 따름

### 2.2 사고 블록의 모델 결속

- **규칙**: 사고 블록마다 어느 모델이 만들었는지가 기록되며, 읽기는 한 방향으로만 가능. Fable 5.1은 이전 모델(Opus 5·Fable 5 등)의 사고 블록을 읽지만, 이전 모델은 Fable 5.1의 사고 블록을 읽지 못함
- **실제 영향**: Opus 5로 진행하던 대화를 Fable 5.1로 옮기면 앞서 한 생각이 그대로 이어짐. 반대로 Fable 5.1에서 이전 모델로 되돌리면 그 구간의 생각은 사라짐. 모델을 자동으로 바꿔 태우는 라우터·폴백 구조가 여기에 해당
- **조용히 사라지는 것이 문제**: 읽을 수 없는 블록은 API가 모델에 전달하기 전에 버리며, 버린 토큰은 과금되지 않음. 다만 기본 설정에서는 아무 표시도 남지 않음. `thinking-binding-controls-2026-08-01` 베타 헤더를 붙이면 응답의 `input_transformations` 배열에 무엇이 버려졌는지 기록되므로, 라우터를 운영한다면 이 값을 로그로 남길 필요

### 2.3 앞선 대화 편집 시 오류

가장 손이 많이 가는 변경. **사고 블록보다 앞에 있는 내용을 한 글자라도 고치면 그 뒤의 사고 블록이 전부 무효**가 되고, 다음 요청이 400 오류로 거부됨(오류 문구에 `The block is bound to a different conversation` 포함).

- **검사 대상**: 최상위 시스템 지시문, 도구 목록, 그 블록보다 앞선 모든 메시지
- **적용 범위**: 2026년 8월 31일 00:00 UTC 이후에 만들어진 계정은 기본 적용. 그 전에 만든 계정은 요청에 `thinking.block_binding.prefix_mismatch_behavior` 값을 넣었을 때만 검사. 앞으로 나올 모델은 모든 계정에 적용될 예정이라, 지금 계정이 대상이 아니어도 미리 맞춰 두는 편이 안전. 남이 자기 API 키로 돌리는 도구·프레임워크를 만든다면, 개발자 본인 계정은 오래되어 통과해도 신규 계정 사용자는 막히므로 반드시 이 값을 켜고 시험 필요
- **Claude Code·claude.ai·Claude Managed Agents·Claude Agent SDK 사용자는 해당 없음**. 이들 도구가 대화 기록을 알아서 보존. 직접 `messages` 배열을 만들어 보내는 코드만 점검 대상

**무효가 되는 편집과 안전한 편집**

| 요청과 다음 요청 사이의 변경 | 뒤따르는 사고 블록 |
| --- | --- |
| 대화 끝에 메시지를 덧붙임 | 유효 |
| 맨 앞에서부터 사고 블록을 연속으로 제거 | 유효 |
| `effort`·`max_tokens`·`tool_choice` 등 요청 설정값 변경 | 유효 |
| 캐시 표시(`cache_control`) 추가·이동·제거 | 유효 |
| 서버 쪽 컴팩션·컨텍스트 편집으로 내용이 줄어듦 | 유효 |
| 같은 파일을 주는 서명 URL이 주소만 바뀜 | 유효 |
| 앞선 메시지를 고치거나 순서를 바꾸거나 지움 | 무효 |
| 앞선 사용자 턴에 문장을 끼워 넣거나 지난번에 넣은 것을 뺌 | 무효 |
| 최상위 시스템 지시문 또는 도구 목록을 바꿈 | 무효 |
| 중간에 있는 사고 블록만 빼고 뒤는 남김 | 그 뒤 전부 무효 |
| 같은 주소가 다음 요청에서 다른 이미지를 돌려줌 | 무효 |

**막히지 않고 같은 일을 하는 방법**

| 지금 하던 것 | 대신 쓰는 것 | 필요한 베타 헤더 |
| --- | --- | --- |
| 시스템 지시문을 새로 만들어 덮어씀 | 대화 중간 시스템 메시지(mid-conversation system message) | 없음 |
| 매 턴 알림 문구를 끼워 넣고 다음 요청에 지움 | 한 턴만 유효한 시스템 메시지(turn-scoped system message, `clear_at: "next_user_message"`) | `mid-conversation-system-clear-at-2026-08-21` |
| 도구 목록에 항목을 넣고 뺌 | `tool_addition`·`tool_removal` 블록 | `mid-conversation-tool-changes-2026-07-01` |
| 최상위 추론 강도를 바꿈 | 메시지 단위 `output_config` | `mid-conversation-output-config-2026-07-01` |
| 오래된 턴을 클라이언트에서 지우거나 요약 | 서버 쪽 컴팩션·컨텍스트 편집 | `compact-2026-01-12` 또는 `context-management-2025-06-27` |
| 내용이 바뀌는 이미지·문서 URL | Files API의 `file_id` 또는 base64 | 없음 |

**내 코드가 걸리는지 확인하는 3단계 절차**

1. **보내는 내용 비교**: 평범한 대화 몇 턴을 돌리며 실제로 나가는 요청 본문을 저장. 이웃한 두 요청에서 `system`·`tools`·공통 `messages`가 새로 붙은 턴을 빼고 완전히 같아야 정상
2. **API로 확인**: `thinking-binding-controls-2026-08-01` 베타 헤더를 붙이고 `prefix_mismatch_behavior`를 `"drop_block"`으로 지정한 뒤 여러 턴짜리 세션을 실제로 돌림. 매 턴 `input_transformations`를 기록
3. **결과 해석**: 매 턴 비어 있으면 정상. `reason: "prefix_binding_mismatch"`가 나오면 해당 지점보다 앞이 바뀐 것이므로 `system`·`tools`·`messages`를 비교해 원인을 찾음. `reason: "model_binding_mismatch"`는 편집 문제가 아니라 모델이 바뀐 경우

CI에서 실패로 잡고 싶으면 `"drop_block"` 대신 `"error"`를 지정해 400 응답을 시험 실패로 처리.

**클라이언트에서 직접 압축한다면**, 가장 단순하고 안전한 형태는 지난 대화 전체를 요약 한 덩어리로 만들어 사용자 메시지 하나로 보내고 나머지는 아무것도 되돌려 보내지 않는 방식. 되돌려 보내는 사고 블록이 없으므로 검사에 걸릴 것도 없고, 모델은 요약본을 놓고 새로 생각. 다만 캐시 읽기 값이 내려갔으므로 **비용을 아끼려고 일찍 압축하던 기존 판단은 다시 계산할 필요** — 늦게 압축하는 쪽이 유리해졌을 수 있음.

---

## 3. 추론 강도 고르기

- 기본값 `high`에서 시작한 뒤 나머지 네 단계를 자체 평가 기준으로 시험. 추론 강도가 지능·응답 시간·비용을 맞바꾸는 주된 조절 장치
- **Fable 5에서 이미 시험했더라도 다시 시험 필요**. 단계 이름이 같아도 모델마다 실제 생각의 양이 다름
- `medium`에서 대체로 Fable 5와 비슷한 품질이 더 싼 값에 나오므로, 품질이 유지되는 작업은 `medium`·`low`로 내리는 편이 이득
- `low`에서도 Opus·Sonnet 계열보다 점수가 높으면서 작업당 비용은 비슷한 경우가 많음. 작은 모델을 높은 강도로 돌리려던 자리에 후보로 넣어 비교할 가치
- 강도에 따라 성격이 달라지는 두 가지 — `low`에서는 검색 도구를 덜 부르고, `xhigh`·`max`에서는 긴 결과물을 쓰기 전에 오래 생각(각각 아래 4절의 처방으로 대응)
- 대화 중간에 강도를 바꿔도 캐시가 깨지지 않음. 어려운 단계만 올리고 나머지는 내리는 운영이 가능하며, `mid-conversation-output-config-2026-07-01` 베타 헤더와 `role: "system"` 메시지의 `output_config`로 지정. 새 강도는 다음 사용자 턴부터 적용

---

## 4. 증상별 프롬프트 처방

Fable 5에서 옮겨 왔을 때 코드 변경 없이도 눈에 띄는 행동 차이와 그 대응. **아래 영문 지시문은 시스템 지시문이나 사용자 메시지에 그대로 붙여 쓰도록 만들어진 원문**이라 번역하지 않고 싣고, 용도만 한국어로 설명.

### 4.1 도구를 한 번에 하나씩만 부름

- **증상**: Fable 5가 여러 파일을 한 번에 읽던 자리에서 5.1은 한 턴에 하나씩 부름. 직접 만든 코딩 에이전트, 명령창·편집기를 붙인 구조, 컴퓨터 조작 작업에서 주로 관찰. 답의 품질은 떨어지지 않으나 턴이 늘어난 만큼 토큰·왕복 시간·전체 소요 시간이 증가
- **적용 조건**: 요청에 가져올 대상이 이름으로 적혀 있으면 5.1도 병렬로 부름. 문제는 다음에 무엇을 읽을지가 작업 맥락에서만 유추되는 경우
- **처방**: 도구 결과를 돌려보낼 때마다 아래 한 문장을 한 턴짜리 시스템 메시지(`clear_at: "next_user_message"`)로 새로 덧붙임. 베타 헤더가 없으면 같은 사용자 메시지 안 `tool_result` 블록 뒤의 텍스트 블록으로 대체 가능

```text
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
```

- **주의**: 지난 턴에 붙였던 사본은 지우지 말고 글자 그대로 둘 것. API가 알아서 가리므로 모델은 최신 것만 읽고 가려진 사본은 토큰도 들지 않음. 지우거나 고쳐 쓰면 앞선 대화 편집에 해당해 캐시가 깨지고 사고 블록이 무효화

### 4.2 작업하는 동안 아무 말이 없음

- **증상**: 도구를 오래 부르는 동안 사용자에게 보이는 글을 Fable 5보다 덜 씀. 추론 강도가 높고 도구 사슬이 길수록 두드러져, 몇 분씩 조용하거나 마지막 단계만 언급하고 끝나는 응답이 나옴
- **먼저 확인할 것**: 모델이 도구 호출 사이에 쓰는 짧은 메모는 사고 블록으로 전달되는데, 기본 설정(`thinking.display`가 `"omitted"`)에서는 그 블록이 비어서 옴. `thinking-display-updates-2026-08-18` 베타 헤더와 함께 `display: "updates"`를 켜면 생각은 감춘 채 진행 메모만 글로 받아 상태 표시줄로 보여줄 수 있음. `"summarized"`는 요약된 생각과 섞어서 전달. 즉 **모델이 말을 안 하는 것이 아니라 요청하지 않아 전달되지 않는 상태일 수 있음**
- **두 번째로 확인할 것**: 지시문에 남아 있는 억제 문구 제거. 이전 모델이 말을 너무 많이 해서 넣어 둔 `hold all findings for the final response` 같은 줄이 대표적
- **처방**: 그래도 부족하면 언제 어떤 글을 원하는지 지시문에 명시

```text
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.
```

- **화면에 도구 출력을 보여주지 않는 제품이라면** 그 사실을 알려야 함. 모르면 사용자에게 "보여주려고" 명령을 실행하는데 화면에는 아무것도 안 뜸

```text
Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply.
```

### 4.3 문장이 길고 빽빽함

- **증상**: 전반적인 글은 이전 모델보다 나아졌으나(상투어와 설명 없는 전문용어가 줄어듦), 경우에 따라 Fable 5보다 문장이 길고 문단 나눔이 적음
- **처방**: 피해야 할 글투를 정의해 주는 방식이 효과적. 사용자 메시지에 넣는 쪽이 더 잘 들으며 시스템 지시문도 가능

```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

- 짧은 판도 대체로 통함: `Please remove all mannered prose.`

### 4.4 대화 답변에 구조가 부족함

- **증상**: 이전 모델은 굵은 글씨와 목록을 남용해서 그것을 누르는 규칙을 지시문에 넣어 두는 경우가 많았음. 5.1은 반대로 굵은 글씨를 덜 쓰고 제목·목록·따옴표에 손을 덜 대므로, 옛 규칙이 정작 필요한 구조까지 눌러 버림
- **처방**: 억제 문구를 지우고, 어떤 형식이 언제 적절한지를 정하는 규칙으로 교체

```text
Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose.
```

### 4.5 요약이 원문을 그대로 옮김

- **증상**: 문서를 요약할 때 원문 문장을 인용 표시 없이 그대로 재현하는 빈도가 Fable 5보다 높음
- **처방**: 올바른 응답의 완전한 예시 하나를 시스템 지시문에 넣음. 사용자 요청·응답·왜 그 응답이 옳은지를 설명하는 문장 세 부분을 모두 포함해야 효과가 나옴

```text
<example>
<user>look up how the Riverton Ledger and the Coast Dispatch each covered the Harbor Bridge closure and compare their reporting</user>
<response>
[web_search: Harbor Bridge closure Riverton Ledger]
[web_search: Harbor Bridge closure Coast Dispatch]
Both outlets agree on the basics: the bridge closed on March 3 after inspectors found cracked welds, and the state expects repairs to take about eight months. Where they differ is emphasis. The Ledger treats it as a local-economy story. The Dispatch frames it as a funding failure; its editorial calls the closure "entirely foreseeable." Read together, the Ledger explains who is affected now and the Dispatch explains how it came to this — neither account alone gives the whole picture.
</response>
<rationale>CORRECT: The response is organized around where the two outlets agree and differ, not as a walk through either article. Each outlet's reporting is conveyed in one or two sentences of the assistant's own indirect speech. One short marked phrase from one source; every other claim is reworded. The response is still specific and complete.</rationale>
</example>
```

- `[web_search: ...]` 두 줄은 실제로 쓰는 도구 이름으로 교체 필요. 그래야 모델이 도구 출력의 예시로 읽고 그 글자를 그대로 뱉지 않음

### 4.6 일을 끝내지 않고 턴을 마침

- **증상**: 다음에 무엇을 하겠다고 적어 놓고 실제로는 하지 않거나(`Next, I'll …`), 원래 요청에 이미 포함된 단계를 두고 허락을 물음(`Shall I apply this?`). 사람이 옆에서 지켜보는 작업이면 문제가 아니지만, 사람이 지켜보지 않는 자동 실행에서는 사용자가 "계속"이라고 답할 때까지 멈춤
- **처방**: 아래 두 덩어리를 함께 넣는 것이 권장. 지시문 길이를 줄여야 하면 첫 번째만 넣어도 효과의 대부분이 유지. 첫 덩어리의 **첫 문장(사용자가 지켜보지 않는다는 문장)이 효과의 상당 부분을 담당**하므로 그대로 유지

```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

```text
# Delivering work
The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request.

If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress. If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours. A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies.

Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead.
```

- **대가**: 첫 덩어리는 모호한 요청에 대해서도 되묻는 빈도를 낮추므로, 되물어야 정확해지는 업무라면 자체 작업으로 득실 확인 필요. 특정 상황에서는 반드시 멈추게 하려면 첫 문장 뒤에 그 상황을 한 문장으로 덧붙임

### 4.7 대화 압축 시 중요한 내용이 사라짐

- **증상**: 클라이언트에서 직접 대화를 요약해 이어 붙일 때 제약·결정·정확한 수치가 빠짐. 서버 쪽 컴팩션을 쓰면 이미 처리되므로 해당 없음
- **처방**: 무엇을 반드시 남길지 항목으로 지정하면 잘 따름

```text
Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary such that this conversation will be continued by a new context window without needing to redo work or be reprovided with relevant constraints or context. Be sure to preserve: (1) any difficulties or problems that came up, and how they were handled or resolved; (2) any possibilities, options, or approaches that were raised, tried, or set aside, and why; (3) anything that was asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary — stated exactly; (4) exactly where things stand now — what has been covered, settled, or completed so far; (5) anything still open, unresolved, promised, or expected to happen next; (6) specific details that would be hard to reconstruct — names, numbers, dates, exact wording, links or references — kept exactly. Be complete on these even at the cost of length; keep everything else concise. Weight the two voices differently: keep what the user said, asked for, shared, or established carefully and close to their own words; your own explanations and reasoning can be condensed much further, to what they concluded or produced — as long as nothing in the six items above is dropped.
```

### 4.8 시키지 않은 수정·테스트가 늘어남

- **증상**: 범위가 열린 기능 구현을 맡기면 요청받은 것에 더해 주변 코드를 고치거나, 언급되지 않은 동작을 확장하거나, 변경 규모에 비해 많은 테스트 파일을 커밋
- **처방**: 무엇을 빼야 하는지를 명시하면 잘 따름. 아래 지시문 적용 시 요청하지 않은 추가 작업과 커밋되는 테스트 코드가 크게 줄면서 작업 성공률에는 측정 가능한 변화가 없었다는 것이 공식 가이드의 설명

```text
If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely.
```

### 4.9 낮은 강도에서 검색하지 않고 기억으로 답함

- **증상**: 추론 강도 `low`에서 검색·조회 도구를 부르는 빈도가 Fable 5보다 낮고 아는 대로 답하는 경향
- **처방 1**: 해당 턴만 추론 강도를 올림. 대화 전체를 올릴 필요는 없음
- **처방 2**: 이름을 알아보는 것과 그 이름의 현재 상태를 아는 것은 다르다는 점을 지시문에 명시

```text
When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search.
```

### 4.10 정상 요청이 안전장치에 막힘

- **현황**: 안전 분류기의 오탐은 Fable 5 출시 시점보다 줄었고, 소스 코드에서 취약점을 찾는 작업은 허용됨. 그래도 막히면 응답이 `stop_reason: "refusal"`로 돌아옴
- **오탐이 잘 나는 세 상황과 대응**

| 상황 | 대응 |
| --- | --- |
| 컴파일 여부를 묻는 표현 | `Does this program compile without errors?` 대신 `Are there any bugs in this program?`으로 질문 |
| 덜 알려진 프로그래밍 언어 | 그 언어가 무엇이고 어떻게 동작하는지 맥락 제공. 언어 공식 문서를 읽을 수 있게 붙이는 방식이 효과적 |
| 도구 출력에 섞인 base64 데이터 | base64로 인코딩된 데이터가 모델 맥락에 들어가면 오탐을 유발하므로 제거가 권장 대응 |

### 4.11 작은 수정에 파일 전체를 다시 씀

- **증상**: 텍스트 파일을 고칠 때 필요한 부분만 바꾸지 않고 전체를 새로 씀. 결과 파일은 대체로 같으나 출력 토큰과 시간이 더 듦
- **처방**: 아래 문장을 시스템 지시문이나 첫 사용자 메시지 끝에 덧붙이면 작거나 중간 규모 변경에서 Fable 5 수준으로 돌아옴

```text
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
```

### 4.12 긴 결과물이 잘리거나 오래 걸림

- **증상**: 추론 강도 `xhigh`, 특히 `max`에서 답을 쓰기 전에 오래 생각. 긴 문서 전체 재작성처럼 결과물 자체가 긴 요청이면 생각 안에서 초안을 거의 다 쓰고 응답으로 다시 쓰는 일이 생겨, 대기 시간과 출력 토큰이 함께 늘고 `max_tokens` 한도에 걸릴 수 있음
- **처방 1**: 이런 요청은 권장 출발점인 `high`로 돌리고, 품질 향상을 실제로 측정한 경우에만 `xhigh`·`max` 사용
- **처방 2**: `max_tokens`를 응답 예상 길이가 아니라 **생각과 응답을 합한 크기**로 잡음
- **처방 3**: 사용자 메시지 끝에 아래 문장을 덧붙임. `[max_tokens]`는 그 요청의 실제 값(예: 64,000)으로 교체. 산문·코드 요청에서 생각의 길이가 크게 줄어듦

```text
Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so don't do that.

Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, spend extra effort on understanding the request, checking the inputs the answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. Usually it is not needed to draft an output multiple times.
```

### 4.13 하위 에이전트를 기다리며 상위 에이전트가 멈춤

- **상황**: 모델이 일부 작업을 하위 에이전트에게 넘길 수 있는 구조에서, 상위 에이전트가 결과를 기다리며 멈추도록 강제하지 않는 편이 유리. 코딩 작업 기준으로 품질·토큰·비용은 비슷하면서 평균 완료 시간이 줄어듦
- **구성 방법 세 가지**: ⑴ 하위 에이전트를 시작하는 도구는 즉시 반환 ⑵ 하위 에이전트 결과는 준비된 뒤 나중 사용자 메시지로 전달 ⑶ 기다리고 싶을 때 부를 수 있는 별도 도구 제공
- **한계**: 그래도 모델은 기다리는 쪽을 자주 선택. 시간 이득은 다른 일을 이어서 하는 일부 실행에서 발생

### 4.14 그림·표를 읽는 답이 세부를 놓침

- **현황**: 기본 시각 처리 능력 자체가 향상됐고, 빽빽한 차트 같은 복잡한 입력에서는 **직접 잘라 확대해 확인할 수 있을 때 가장 좋은 결과**
- **구성 방법**: 원본 이미지·영상을 담은 실행 환경(컨테이너)에 PIL·OpenCV 같은 기본 이미지 처리 라이브러리를 미리 깔아 두고 에이전트로 실행. 컨테이너 운영이 부담이면 이미지의 특정 영역을 잘라 확대해 돌려주는 도구 하나만 붙여도 향상분의 대부분을 얻음

---

## 5. 거부와 폴백 처리

### 5.1 거부 응답의 모양

- 거부는 오류가 아니라 **HTTP 200 정상 응답**이며 `stop_reason`이 `"refusal"`. 오류율·5xx 기준으로 만든 감시 체계에는 전혀 잡히지 않으므로 별도 지표로 계측 필요
- `stop_details` 안의 `category`가 어떤 정책 영역이 걸렸는지 표시. `explanation`은 사람이 읽는 설명이며 문구가 고정되지 않으므로 파싱 대상이 아니라 표시 대상
- 분기 판정은 `stop_reason` 또는 `stop_details.type`으로 할 것. `category`와 `explanation`은 이름 붙은 영역에 해당하지 않으면 정상적으로 `null`

| `category` | 뜻 |
| --- | --- |
| `cyber` | 악성코드·공격 코드 개발에 쓰일 수 있는 요청. 정상적인 보안 업무도 걸릴 수 있음 |
| `bio` | 생물학적 위해에 쓰일 수 있는 요청. 정상적인 생명과학 업무도 걸릴 수 있음 |
| `frontier_llm` | 경쟁 AI 모델 개발을 돕는 요청. Anthropic 상업 약관상 제한. 정상적인 기계학습 업무도 걸릴 수 있음 |
| `reasoning_extraction` | 모델 내부의 생각을 응답 본문으로 그대로 재현해 달라는 요청 |
| `general_harms` | 위 네 영역 밖의 이용 정책 영역 |

### 5.2 폴백 세 가지 방식

| 상황 | 방식 | 특징 |
| --- | --- | --- |
| Claude API 사용, 가장 단순한 구성 | 서버 쪽 폴백 | 요청 한 번에 응답 한 번. API가 재시도까지 처리 |
| 어느 플랫폼이든 Anthropic SDK 사용 | SDK 미들웨어 | 클라이언트에 한 번 설정하면 자동 재시도 |
| 직접 HTTP 호출 또는 자체 재시도 로직 | 수동 재시도 | 통제권 전부. 폴백 크레딧으로 비용 절감 |

- 서버 쪽 폴백은 `fallbacks` 값을 `"default"`로 두고 `server-side-fallback-2026-07-01` 베타 헤더를 붙이면 거부 영역별로 Anthropic이 권장하는 모델로 재시도. 자체 모델을 최대 3개까지 지정하는 것도 가능
- **Fable 5.1에 허용되는 폴백 대상은 Claude Opus 4.8과 Claude Opus 5**
- 서버 쪽 폴백은 Message Batches API에서 지원되지 않고 AWS·Google Cloud·Microsoft Foundry에서도 사용 불가. 해당 환경은 SDK 미들웨어 사용
- 한 번 폴백이 일어난 대화는 이후 요청이 곧바로 그 폴백 모델로 감(고정 라우팅, sticky routing). 약 1시간 유지되고 조직 단위로 적용되며, 최선 노력 방식이라 원래 모델이 다시 시도될 수 있으므로 코드가 두 경우를 모두 처리해야 함

### 5.3 과금 규칙

- 출력이 하나도 나오기 전에 거부가 오면 **과금되지 않음**. 토큰 수는 `usage`에 보고되나 청구 대상이 아니며, 요청 자체는 사용량 한도에는 계산
- 출력이 일부 나온 뒤 거부되면 그때까지의 입력·출력은 정상 단가로 과금
- 폴백이 일어난 경우 시도별 기록은 `usage.iterations` 배열이 정본. 서로 다른 모델의 토큰이 한 항목으로 합산되는 일은 없음
- Fable 5.1은 폴백 크레딧 대상이라, 모델을 바꾸느라 다시 물게 되는 캐시 비용을 환급받음

### 5.4 자주 나오는 실수

- 거부된 요청을 같은 모델로 재시도. 대개 또 거부되므로 다른 모델로 보낼 것
- 재시도 예산을 턴·세션 단위로 잡음. 한 턴에서 에이전트와 하위 에이전트가 각각 거부될 수 있으므로 요청 단위로 잡을 것
- 일부 경로에만 폴백을 설정. 오류 복구 분기와 배치 작업에도 필요하며, 하위 에이전트 호출에는 `fallbacks` 값이 자동으로 전달되지 않아 따로 지정 필요
- 전역 설정값으로 폴백 여부를 관리. 값이 어긋나면 조용히 보호가 풀리므로 요청마다 지정하는 편이 안전

---

## 6. 비용

Fable 5와 같은 값이며 캐시 읽기만 인하(단위 USD, 100만 토큰 기준).

| 입력 | 5분 캐시 쓰기 | 1시간 캐시 쓰기 | 캐시 읽기 | 출력 |
| --- | --- | --- | --- | --- |
| $10 | $12.50 | $20 | $0.25 | $50 |

- 캐시 읽기는 입력 단가의 0.025배. 다른 Claude 모델의 0.1배와 비교하면 **같은 앞부분을 계속 다시 읽는 긴 에이전트 작업의 캐시 비용이 4분의 1**
- 캐시 쓰기 단가와 캐시 적용 최소 길이 512토큰은 변동 없음
- 배치 처리는 입력 100만 토큰당 $5, 출력 100만 토큰당 $25

---

## 7. 이관 절차 5단계

1. **모델 이름 교체**: `claude-fable-5` → `claude-fable-5-1`
2. **도구 강제 호출 제거**: `tool_choice`의 `any`·`tool` 지정을 지우고, 형식 강제가 필요하면 strict tool use나 structured outputs로 이동
3. **대화 기록을 덧붙이기 전용으로 전환**: 사고 블록을 손대지 않고 그대로 되돌려 보냄. 직접 `messages`를 만든다면 매 턴 알림은 한 턴짜리 시스템 메시지로, 지시문·도구 변경은 대화 중간 시스템 메시지로 옮기고, 오래된 내용은 서버 쪽에서 줄임. 운영에 쓸 `prefix_mismatch_behavior` 값을 정하고 `input_transformations`를 감시
4. **추론 강도 재조정**: 기본값 `high`에서 다시 시험하고, 세션 내내 한 단계를 유지하는 대신 중간에 바꾸는 운영을 검토
5. **평가 재실행**: 거부 처리·폴백·폴백 크레딧·토큰 계산 방식은 그대로 넘어옴. 캐시 읽기 값이 내려갔고 기본 동작이 달라진 항목이 있으므로, 기존 평가 기준으로 다시 측정

---

## 8. 먼저 할 일 세 가지

- **첫째, 이관 전에 대화 기록 편집 여부부터 확인.** Claude Code·claude.ai·Agent SDK만 쓴다면 확인할 것이 없고, 직접 `messages`를 만드는 코드가 있다면 위 3단계 절차(요청 본문 비교 → `drop_block`으로 실제 실행 → `input_transformations` 해석)를 그대로 실행. 계정 생성일이 2026년 8월 31일 이전이면 지금은 막히지 않으나 이후 모델에서 전부 적용될 예정이라 미루면 같은 일을 급하게 하게 됨
- **둘째, 지시문은 고치지 말고 관찰부터.** 기존 Fable 5용 지시문은 대체로 그대로 동작하므로, 위 4절의 증상 중 실제로 보이는 것에만 해당 처방을 적용. 증상 없이 문장을 미리 넣으면 지시문만 길어지고 서로 부딪힘
- **셋째, 추론 강도를 비용 조절 장치로 사용.** 캐시 읽기 인하와 `medium` 단계의 품질을 함께 놓고 보면, 기본값 `high`를 그대로 두는 것이 대부분의 업무에서 가장 비싼 선택. 작업별로 한 단계씩 내려 보며 품질이 유지되는 하한을 찾는 편이 이득

---
type: guide
audience: Claude Fable 5를 도구·에이전트·워크플로우에 적용하는 개발자·프롬프트 작성자
related_docs:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 (1차 출처 — Anthropic 공식 가이드)
  - https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5 (모델 소개 — API 변경·가격·가용성)
  - https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback (거부·폴백 처리)
  - docs/GUIDE-CLAUDE-OPUS-4-8-PROMPTING-2026-07-19-1828.md (자매 문서 — 폴백 대상 모델 Opus 4.8 프롬프팅)
  - /Users/sspark/.claude/CLAUDE.md (이 저장소의 글로벌 규칙 — 아래 습관 다수와 대응)
created: 2026-07-11 17:10
status: active
description: "Fable 5는 '더 자세히 지시할수록' 좋아지던 이전 모델과 반대로, 짧은 목표 지시·명확한 경계·검증 습관으로 조종해야 성능이 나온다. 이 가이드는 Anthropic 공식 프롬프팅 문서를 바탕으로 무엇이 달라졌고 어떤 프롬프트를 넣어야 하는지 정리한다."
---

# Claude Fable 5 프롬프팅 가이드

## 이 가이드가 다루는 것

Claude Fable 5는 이전까지 너무 복잡하거나, 오래 걸리거나, 모호해서 맡기기 어려웠던 문제를 처리하도록 만들어진 모델이다. 사람이 몇 시간에서 며칠, 몇 주에 걸쳐 하던 종단(end-to-end) 작업에 특히 강하다. 그만큼 **이전 모델(Claude Opus 4.8)에서 통하던 프롬프팅 습관이 오히려 방해가 되는** 지점이 여럿 생긴다.

이 문서는 Anthropic 공식 가이드 *Prompting Claude Fable 5*를 바탕으로, 마이그레이션할 때 실제로 프롬프트·스캐폴딩을 어떻게 바꿔야 하는지를 정리한 실무 가이드다. 아래 프롬프트 스니펫은 **시스템 프롬프트나 에이전트 지시문에 그대로 붙여 쓰도록 설계된 원문**이라 영문 그대로 싣고, 각 용도를 한국어로 풀어 설명한다.

> **참고**: 이 가이드는 Fable 5와 그 자매 모델 Claude Mythos 5에 함께 적용된다. 모델의 API 파라미터 변경(adaptive thinking 전용, 요약된 thinking 출력, extended thinking 예산 없음, `refusal` 종료 사유 등)은 별도 문서인 *Introducing Claude Fable 5 and Claude Mythos 5*를 참조한다.

---

## 한눈에 보는 사고 전환

| 이전 모델에서 하던 것 | Fable 5에서 해야 하는 것 |
|----------------------|--------------------------|
| 단계별 체크리스트로 세세히 지시 | **목표(goal)**를 주고 방법은 맡긴다 |
| 원하는 동작을 하나하나 이름 붙여 나열 | **짧은 지시 한 줄**로 조종한다 |
| 쉬운 작업으로 성능을 가늠 | **가장 어려운 미해결 문제**에 붙여 본다 |
| 요청한 것만 하리라 가정 | **하지 말 것의 경계**를 명시한다 |
| 진행 보고를 그대로 신뢰 | 도구 결과에 **근거를 대게** 시킨다 |

핵심은 한 문장이다 — **Fable 5는 지시를 잘 따르므로, 규칙을 열거하는 대신 의도를 짧게 전달하고 경계와 검증만 걸어 준다.**

---

## Opus 4.8 대비 나아진 지점

공식 가이드가 밝힌, Fable 5가 직전 모델인 Claude Opus 4.8 대비 개선된 영역이다. **어떤 작업을 Fable 5로 옮길지 판단하는 근거**가 된다 — 아래가 강한 영역일수록 마이그레이션 효과가 크다.

- **장기 자율성(Long-horizon autonomy)** — 며칠 단위의 목표 지향 실행에서도 긴·복잡한 작업 내내 지시 유지력이 강하다.
- **복잡·명세된 문제의 첫 시도 정확도** — 이전에 며칠의 반복이 필요하던 시스템을 단일 패스로 구현했다는 초기 테스터 보고.
- **비전(Vision)** — 밀도 높은 기술 이미지·웹앱·상세 스크린샷을 더 정확히, 종종 더 적은 출력 토큰으로 해석한다. 뒤집히거나 흐리거나 노이즈 낀 이미지를 bash·crop 도구로 다루도록 학습됨.
- **엔터프라이즈 워크플로우** — 금융 분석·스프레드시트·슬라이드·문서에서 지시 이행·스코프 유지·전문가급 산출.
- **코드 리뷰·디버깅** — 버그 발견 recall이 (안전 분류기가 다루는 사이버보안 영역 밖에서) 눈에 띄게 높고, 코드베이스·저장소 히스토리 검색 포함.
- **모호성 처리(Navigating ambiguity)** — 복잡·다중 스레드 요청을 주고 다음 단계를 스스로 정하게 할 때 잘한다.
- **위임·협업(Delegation and collaboration)** — 병렬 서브에이전트를 훨씬 안정적으로 띄우고, 장수 서브에이전트·동료 에이전트와의 지속 통신을 신뢰성 있게 관리한다.

> 이 영역들은 Fable 5의 강점인 동시에, **역으로 Opus 4.8을 언제 쓸지의 판단 기준**이기도 하다 — Fable 5가 거부하는 공격적 사이버보안·생명과학 작업, 그리고 추론 노출이 필요한 작업은 Opus 4.8로 폴백한다(별도 문서 *Claude Opus 4.8 프롬프팅 가이드* 참조).

---

## 1. Effort 레벨을 상황에 맞게 고른다

`effort`는 Fable 5에서 **지능 · 지연시간 · 비용** 사이의 균형을 조절하는 1차 손잡이다.

- **`high`** — 대부분의 작업에 대한 기본값
- **`xhigh`** — 역량이 가장 중요한 작업(가장 어려운 문제)
- **`medium` / `low`** — 일상적·정형 작업

Fable 5는 낮은 effort에서도 잘 동작하며, 종종 이전 모델의 `xhigh` 성능을 넘어선다. 작업이 완료되긴 하지만 필요 이상으로 오래 걸리거나, 더 빠르고 대화형으로 진행하고 싶다면 effort를 낮춘다.

높은 effort에서는 검증·추론 품질이 가장 좋아지는 대신, 정형 작업에서 필요 이상으로 맥락을 모으거나 손대지 않아도 될 곳을 "정리"하려는 경향이 생긴다. **요청하지 않은 리팩터링·추상화를 막으려면** 다음을 지시에 넣는다:

```text
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

> 이 지시는 이 저장소 글로벌 규칙의 **Rule 2(Simplicity First)·Rule 3(Surgical Changes)**과 정확히 같은 취지다.

---

## 2. 긴 실행을 전제로 인프라를 준비한다

어려운 작업 하나의 요청이 높은 effort에서 **수 분** 동안 돌 수 있고, 자율 실행은 **몇 시간**까지 이어진다. 이는 Fable 5로 옮길 때 팀이 겪는 가장 큰 변화 중 하나다.

마이그레이션 전에 다음을 조정한다:

- **클라이언트 타임아웃** 상향
- **스트리밍**과 사용자용 **진행 표시** 정비
- 실행이 끝날 때까지 블로킹하지 말고, 예약 작업(scheduled job) 등으로 **비동기 확인**하도록 하니스 재구성

작업이 모호할 때 Fable 5가 과도하게 계획만 세우는 것을 막으려면 다음을 넣는다:

```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

---

## 3. 짧은 지시로 조종한다

Fable 5는 지시 이행 능력이 크게 좋아져서, **동작 하나하나에 이름을 붙여 열거하지 않아도** 짧은 지시로 대부분을 조종할 수 있다. 손대지 않으면 필요 이상으로 장황해지는 경향(안 할 옵션까지 훑기, 근본 원인 장황 설명, 과하게 구조화된 PR 설명, 다음 줄을 설명하는 주석)이 있는데, **짧은 간결성 지시 한 줄이 개별 패턴을 모두 나열하는 것만큼 효과적**이다:

```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

긴 워크플로우의 **체크포인트(멈춤) 동작**도 마찬가지로, 모든 경우를 열거할 필요 없이 한 문단이면 된다:

```text
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

---

## 4. 진행 보고에 근거를 대게 한다

긴 자율 실행에서 Fable 5가 **실제 도구 결과에 비추어 진행 상황을 스스로 감사(audit)**하도록 지시한다. Anthropic 테스트에서, 허위 상태 보고를 유도하도록 설계한 작업에서조차 이 지시가 조작된 진행 보고를 거의 없앴다:

```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

> 글로벌 규칙 **Rule 5(Verify by Execution)·Rule 6(Technical Integrity)**의 "faking 금지"와 대응한다.

---

## 5. 하지 말 것의 경계를 명시한다

Fable 5는 이따금 **요청하지 않은 행동**을 한다(요청 없이 이메일 초안 작성, 방어용 git 브랜치 백업 생성 등). 무엇을 하고 무엇을 하지 말지 명시적 제약을 건다:

```text
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

> 글로벌 규칙 **Rule 1**의 "질문과 변경 요청을 구분하라"와 같은 취지다.

---

## 6. 서브에이전트를 적극 위임한다

Fable 5는 이전 모델보다 **병렬 서브에이전트를 훨씬 잘 띄우고 안정적으로 관리**한다. 다음을 권장한다:

- 서브에이전트를 자주 쓰고, **언제 위임이 적절한지** 명확히 안내한다.
- 오케스트레이터와 서브에이전트 사이는 각 서브에이전트가 반환될 때까지 블로킹하지 말고 **비동기 통신**을 선호한다.
- **장수(long-lived) 서브에이전트**는 서브태스크 간 컨텍스트를 유지해, 캐시 재사용으로 시간·비용을 아끼고 가장 느린 서브에이전트에서 병목이 생기지 않게 한다.

```text
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

---

## 7. 메모리 시스템을 만들어 준다

Fable 5는 **이전 실행에서 얻은 교훈을 기록하고 참조**할 수 있을 때 특히 잘한다. Markdown 파일 하나만큼 단순해도 좋으니 메모를 적을 곳을 준다:

```text
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

기존 히스토리에서 메모리를 부트스트랩하려면 과거 세션을 검토하게 한다:

```text
Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use.
```

> 이 저장소가 이미 쓰는 `MEMORY.md` + `memory/*.md` 구조가 정확히 이 패턴이다.

---

## 8. 요청만 말고 이유를 함께 준다

Fable 5는 요청의 **의도**를 이해할 때 더 잘한다. 의도를 알면 스스로 추측하는 대신 관련 정보를 정확한 작업에 연결한다. 특히 여러 워크스트림을 넘나드는 장기 에이전트에는 "왜 이걸 묻는지"를 함께 준다:

```text
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

---

## 9. 사용자에게 전하는 글의 가독성을 챙긴다

도구 호출이 많고 작업 맥락이 큰 에이전트 대화에서는 Fable 5의 최종 메시지가 **따라가기 어려워질 수 있다**(화살표 축약, 과한 구현 세부, 사용자가 못 본 추론 언급, 지나친 전문 표현). 커뮤니케이션 스타일 부록을 넣어 완화한다:

```text
Terse shorthand is fine between tool calls (that's you thinking out loud, and brevity there is good). Your final summary is different: it's for a reader who didn't see any of that.

If you've been working for a while without the user watching (overnight, across many tool calls, since they last spoke), your final message is their first look at any of it. Write it as a re-grounding, not a continuation of your working thread: the outcome first, then the one or two things you need from them, each explained as if new. The vocabulary you built up while working is yours, not theirs; leave it behind unless you re-introduce it.

When you write the summary at the end, drop the working shorthand. Write complete sentences. Spell out terms. Don't use arrow chains, hyphen-stacked compounds, or labels you made up earlier. When you mention files, commits, flags, or other identifiers, give each one its own plain-language clause. Open with the outcome: one sentence on what happened or what you found. Then the supporting detail. If you have to choose between short and clear, choose clear.
```

> 글로벌 규칙 **Response Discipline**(첫 화면에 결론, 완결 문장, 화살표 체인 금지)과 대응한다.

---

## 10. 드문 경우: 조기 중단과 자율 실행

긴 세션 후반부에서 Fable 5가 드물게 **의도만 텍스트로 말하고("I'll now run X") 실제 도구 호출은 빠뜨리거나**, 이미 진행해도 될 상황에서 허락을 묻고 멈추는 경우가 있다. 이럴 땐 "continue" 또는 "go ahead and do it end to end" 한 마디면 충분하다.

사용자가 실시간으로 지켜보지 않는 **자율 파이프라인**에는 다음 시스템 리마인더를 추가한다:

```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

---

## 11. 드문 경우: 컨텍스트 예산 걱정

아주 긴 세션에서 Fable 5가 드물게 **새 세션을 제안하거나, 요약·인계를 제안하거나, 자기 작업을 줄이려** 한다. 이는 대개 하니스가 **남은 토큰 카운트다운을 모델에게 노출**할 때 유발된다. 가능하면 명시적 컨텍스트 예산 수치를 노출하지 말고, 꼭 보여야 한다면 안심시키는 문구를 넣는다:

```text
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

---

## 스캐폴딩·하니스 변경 권장 사항

프롬프트 개별 문구를 넘어, 도구·하니스 차원에서 손볼 것들이다.

### 난도 범위의 위쪽에서 시작한다
이전 모델에 맡기던 것보다 **더 어려운 작업**을 골라, Fable 5가 스코프를 잡고, 명확화 질문을 하고, 실행하게 한다. 쉬운 작업으로만 테스트하면 역량 범위를 과소평가하게 된다.

### 자기 검증을 프롬프트에 명시한다
자기 비판보다 **별도의 신선한 컨텍스트를 가진 검증 서브에이전트**가 대체로 더 낫다. 장기 작업에는 다음처럼 지시한다:

```text
Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.
```

### 기존 프롬프트·스킬을 리팩터링한다
이전 모델용으로 만든 스킬은 Fable 5에는 **지나치게 규범적(prescriptive)이라 오히려 품질을 떨어뜨릴 수 있다.** 기본 성능이 더 나으면 오래된 지시는 검토 후 제거를 고려한다. Fable 5는 작업 중 배운 것으로 스킬을 즉석에서 갱신하는 것도 잘한다.

> 이 저장소의 `doc-writer`·`report-style` 등 스킬을 Fable 5에 맞춰 재검토할 근거가 된다.

### send-to-user 도구를 만든다
길고 비동기적인 에이전트에는, **턴을 끝내지 않고 사용자가 반드시 봐야 할 메시지를 원문 그대로** 전달하는 클라이언트 측 도구를 준다(생성된 코드 스니펫, 초안 메시지, 중간에 나온 질문에 대한 직접 답변, 구체적 수치가 담긴 진행 업데이트 등). 도구 입력은 요약되지 않으므로 내용이 손실 없이 도착한다.

```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "The content to display to the user."
      }
    },
    "required": ["message"]
  }
}
```

도구를 정의만 해서는 부족하다. 시스템 프롬프트에 호출을 유도하는 지시가 없으면 Fable 5는 이 도구를 거의 부르지 않는다:

```text
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

내레이션·내부 추론을 이 도구로 흘리지 않는다 — 비사용자용 내용으로 과다 호출하면 도구의 목적이 무너진다.

### 추론을 응답에 재현하라고 시키지 않는다
모델에게 **내부 추론을 응답 텍스트로 되풀이·전사·설명하라고 지시하는 프롬프트/스킬/하니스**는 Fable 5의 `reasoning_extraction` 거부 범주를 건드려, Opus 4.8로의 폴백이 잦아질 수 있다. 마이그레이션 시 "show your thinking" 류 지시가 있는지 감사한다. 추론 가시성이 필요하면 adaptive thinking의 구조화된 `thinking` 블록을 읽고, 진행 노출은 위의 send-to-user 도구를 쓴다.

---

## 안전 분류기와 폴백 주의

Fable 5는 다음을 겨냥한 안전 분류기를 돌린다:

- **공격적 사이버 보안**(익스플로잇·멀웨어·공격 도구 제작)
- **생물·생명과학**(실험 기법, 분자 메커니즘 등)
- **모델의 요약된 thinking 추출**

선의의 보안 작업이나 유익한 생명과학 작업도 이 안전장치를 건드릴 수 있고, 그 경우 `stop_reason: "refusal"`이 반환된다. 거부된 요청을 자동 우회하려면 서버·클라이언트 측 **폴백을 Claude Opus 4.8로** 설정한다. 또한 악의적 의도로 의심되면 덜 강력한 모델로 라우팅되므로, **자기 추론을 드러내라는 요청**은 이 방어선을 건드릴 수 있음에 유의한다.

---

## 요약 체크리스트

Fable 5로 옮길 때 점검할 항목이다.

- [ ] effort 기본을 `high`로, 어려운 작업은 `xhigh`로 설정했는가
- [ ] 클라이언트 타임아웃·스트리밍·진행 표시를 긴 실행에 맞게 조정했는가
- [ ] 세세한 체크리스트를 **목표 기반** 지시로 바꿨는가
- [ ] 진행 보고에 **근거를 대게** 하는 감사 지시를 넣었는가
- [ ] 하지 말 것의 **경계**를 명시했는가
- [ ] 서브에이전트 위임·비동기 통신을 활용하는가
- [ ] **메모리 파일**과 기록 규칙을 제공했는가
- [ ] 자율 파이프라인에 **조기 중단 방지** 리마인더를 넣었는가
- [ ] 오래된·과도하게 규범적인 스킬을 검토·정리했는가
- [ ] "추론을 응답에 재현" 류 지시를 제거하고 **Opus 4.8 폴백**을 설정했는가

---

## 참고 자료

- [Prompting Claude Fable 5 — Anthropic 공식 가이드](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) (이 문서의 1차 출처)
- [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) (모델 소개·API·가격)
- [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback) (거부·폴백)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (모든 Claude 모델 공통 기법)

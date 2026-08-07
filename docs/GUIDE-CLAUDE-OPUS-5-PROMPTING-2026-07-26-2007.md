---
type: guide
audience: Claude Opus 5를 도구·에이전트·워크플로우에 적용하는 개발자·프롬프트 작성자
related_docs:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 (1차 출처 — Anthropic 공식 프롬프팅 가이드)
  - https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5 (모델 소개 — API 변경·가격·가용성)
  - https://platform.claude.com/docs/en/build-with-claude/effort (effort 레벨 권장값)
  - docs/GUIDE-CLAUDE-OPUS-4-8-PROMPTING-2026-07-19-1828.md (직전 세대 — 방향이 반전된 항목 다수)
  - docs/GUIDE-CLAUDE-FABLE-5-PROMPTING-2026-07-11-1710.md (자매 문서 — 상위 모델 Fable 5 프롬프팅)
  - /Users/sspark/.claude/CLAUDE.md (이 저장소의 글로벌 규칙 — 아래 습관 다수와 대응)
created: "2026-07-26 20:07"
status: active
description: "Opus 5는 thinking이 기본으로 켜져 있고, 스스로 검증하며, 말이 길고, 위임을 과하게 한다. 4.8용으로 튜닝한 프롬프트는 상당수가 이제 반대 방향으로 작동한다 — 무엇을 지우고 무엇을 넣어야 하는지 공식 가이드 기준으로 정리한다."
---

# Claude Opus 5 프롬프팅 가이드

## 이 가이드가 다루는 것

Claude Opus 5는 **복잡한 에이전트형 코딩과 엔터프라이즈 작업**을 겨냥해 Opus 4.8 위에 세워진 모델이며, Anthropic은 이를 증분이 아닌 **step-change**로 규정한다 — 특히 깊은 추론, 에이전트형·장기 지평 작업, test-time compute 스케일링에서. 기존 4.8 프롬프트에서도 손질 없이 잘 동작하지만, **4.8용으로 넣어둔 스캐폴딩 상당수가 이제 역효과를 낸다.** 이 문서는 Anthropic 공식 가이드 *Prompting Claude Opus 5*를 1차 출처로, 무엇을 지우고 무엇을 넣어야 하는지 정리한 실무 가이드다. 아래 영문 프롬프트 스니펫은 **시스템 프롬프트·에이전트 지시문에 그대로 붙여 쓰도록 설계된 원문**이라 원어 그대로 싣는다.

> **자매 문서**: 상위 모델 Claude Fable 5는 별도 가이드를 참조한다. Opus 5는 "Fable 5의 프론티어 지능을 절반 가격에" 제공하는 위치이며, 거부(`stop_reason: "refusal"`) 시 폴백 대상은 Opus 4.8이다.

> **모델 사실 요약** (출처: *What's new in Claude Opus 5*): 모델 ID `claude-opus-5` · 1M 토큰 컨텍스트(기본값이자 최대값, 축소 변형 없음) · 최대 출력 128k 토큰 · **thinking 기본 ON** · effort 기본값 `high`(전 레벨 `low`~`max` 지원) · $5/$25 per MTok(4.8과 동일) · Claude API·Amazon Bedrock(`anthropic.claude-opus-5`)·Google Cloud·Microsoft Foundry 전 표면 가용.

---

## 한눈에 보는 핵심 손잡이

| 손잡이 | 기본 권장 | 언제 조정하나 |
|--------|-----------|----------------|
| **effort** | 기본 `high`에서 시작해 **아래로 스윕** | 품질이 유지되는 곳은 `low`/`medium`으로 내려 비용·지연을 잡고, 어려운 코딩·에이전트 작업만 `xhigh`/`max`로 올린다 |
| **thinking** | 켠 채로 둔다(기본값) | 끄고 싶으면 effort를 내리는 쪽이 낫다. `disabled`는 effort `high` 이하에서만 허용 |
| **응답 길이** | 기본이 길다 | **effort로는 안 줄어든다** — 프롬프트로 명시해야 한다 |
| **검증 지시** | **제거** | 스스로 검증하므로 "double-check" 류는 과잉 검증만 유발 |
| **서브에이전트** | **상한을 건다** | 기본적으로 위임을 과하게 한다(4.8과 정반대) |

핵심 한 문장 — **Opus 5는 시키지 않아도 검증하고 위임하고 설명하므로, 4.8 시절 "더 하게 만드는" 지시는 지우고 "덜 하게 만드는" 지시를 넣는다. 그리고 길이는 effort가 아니라 프롬프트로 잡는다.**

---

## 0. 4.8 → 5에서 방향이 뒤집힌 항목

마이그레이션에서 가장 비싼 실수는 4.8용 처방을 그대로 들고 오는 것이다. 아래 세 줄이 반전된 지점이다.

| 항목 | Opus 4.8에서의 권고 | Opus 5에서의 권고 |
|------|--------------------|-------------------|
| 서브에이전트 | **덜 띄운다** → "언제 위임하라"를 명시해 늘려라 | **더 띄운다** → 위임 상한·조건을 걸어 줄여라 |
| 검증 | 하니스에 검증 단계를 둔다 | **검증 지시를 삭제**한다(스스로 함, 지시하면 과잉) |
| 진행 내레이션 | 강제 요약 스캐폴딩 제거(기본이 충분) | 기본이 **과하다** → 침묵 기본값·업데이트 형태를 명시 |

> 출처: 공식 *Prompting Claude Opus 5* 및 `claude-api` 스킬 번들의 마이그레이션 가이드(Opus 4.8 절 vs Claude Opus 5 절).

---

## 1. API 파괴적 변경 두 가지

*What's new in Claude Opus 5* 기준. 나머지 요청 표면은 4.7/4.8과 동일하다(`budget_tokens` 400, 샘플링 파라미터 400, 마지막 assistant prefill 400, `thinking.display` 기본 `"omitted"`).

**(1) thinking이 기본으로 켜진다.** 4.8/4.7에서는 `thinking` 필드를 빼면 thinking 없이 돌았지만, Opus 5는 같은 요청이 **adaptive thinking으로 실행**된다. 와이어 값은 그대로이며 `{type: "adaptive"}`는 기본값과 동치다. 문제는 조용한 비용·잘림 변화다 — **`max_tokens`는 thinking + 응답 텍스트 합계의 하드 캡**이므로, 4.8에서 thinking 없이 돌며 `max_tokens`를 빠듯하게 잡아둔 경로는 이제 응답 중간에 잘릴 수 있다. `thinking`을 한 번도 설정하지 않은 모든 라우트의 `max_tokens`를 재점검한다.

**(2) thinking 비활성화는 effort `high` 이하에서만 허용된다.** `thinking: {type: "disabled"}` + `xhigh`/`max`는 **400**이다. 4.8은 이 조합을 받았으므로, thinking을 끄는 경로가 있으면 마이그레이션 전에 전수 조사한다. 검증은 **요청 단위**라, 같은 대화 안에서 뒤늦게 effort만 올린 요청도 개별적으로 거절된다.

```json
// 400 on Claude Opus 5
{ "model": "claude-opus-5",
  "thinking": { "type": "disabled" },
  "output_config": { "effort": "xhigh" } }
```

지연에 민감해 `xhigh` + thinking-off로 돌던 라우트는, **`medium` + thinking-on**으로 바꾸는 편이 대체로 낫다 — Opus 5는 낮은 effort에서의 품질이 특히 좋다.

---

## 2. effort는 "위로"가 아니라 "아래로" 스윕한다

Opus 4.7·4.8의 공식 권고는 "코딩·에이전트는 `xhigh`부터"였다. **Opus 5의 공식 권고는 기본값 `high`에서 시작해 eval 기준으로 양방향 조정**이며, 특히 `low`·`medium`을 **비용·응답시간의 1차 통제 수단으로 적극(liberally) 사용**하라고 명시한다. 이전 모델에서 가져온 effort 설정은 재사용하지 말고 새로 스윕하라는 문장도 함께 있다.

| effort | Opus 5에서의 용도 |
|--------|-------------------|
| **`max`** | 토큰 제약 없이 최고 역량이 정당화되는 작업 |
| **`xhigh`** | 까다로운 코딩·에이전트 작업(30분 이상 장기 실행, 토큰 예산이 백만 단위) |
| **`high`** | **기본값이자 출발점.** 복잡한 추론·코딩·에이전트 일반 |
| **`medium`** | eval에서 품질이 유지되면 여기로 내린다 — 균형점 |
| **`low`** | 단순·지연 민감 작업, 서브에이전트 |

> **참고**: `xhigh`·`max`로 돌릴 때는 서브에이전트·도구 호출을 넘나들며 생각·행동할 여유를 주도록 **max output 토큰을 크게** 잡는다. **64k에서 시작**해 튜닝한다(4.7·4.8과 동일한 권고).

> **주의**: `effort`는 요청 단위 설정이고 **렌더된 프롬프트를 바꾸므로, 대화 중간에 값을 바꾸면 프롬프트 캐시가 깨진다.** 캐시에 의존하는 긴 세션은 시작 시 정하고 고정한다.

---

## 3. 응답 길이는 프롬프트로만 줄어든다

Opus 5의 기본 사용자향 응답은 이전 Opus보다 **길다**. 그리고 결정적으로 — **effort는 "얼마나 생각하는가"를 조절할 뿐 "얼마나 말하는가"는 신뢰성 있게 줄이지 못한다.** effort를 내려 verbosity를 잡으려는 시도는 실패한다. 명시적으로 프롬프트한다:

```text
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

시스템 프롬프트가 길다면 **끝부분에 짧은 리마인더**를 하나 더 붙인다:

```text
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

> 글로벌 규칙 **Response Discipline**("Lead with the outcome", "Concise by selection")과 대응한다 — 다만 Opus 5에서는 이 규칙이 "있으면 좋은 것"이 아니라 **없으면 기본이 길어지는** 부하 지지 요소다.

---

## 4. 에이전트 진행 내레이션은 형태를 지정한다

Opus 5는 에이전트 작업 중 **자발적으로 많이 설명한다** — 무엇을 할지 예고하고, 세션 내 메시지당 출력이 이전 모델보다 길다. 4.8에서 "매 N번 도구 호출마다 요약" 같은 강제 스캐폴딩을 제거했다면, Opus 5에서는 **반대로 억제 지시**가 필요할 수 있다. 원하는 케이던스와 형태를 서술한다:

```text
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

내레이션을 **늘리거나 스타일을 바꾸고 싶을 때도 같은 레버**를 반대 방향으로 쓴다 — 원하는 업데이트의 모습을 명시하고 예시를 준다. 공식 가이드는 "하지 마라"는 지시보다 **원하는 소통 스타일의 긍정 예시**가 대체로 더 효과적이라고 안내한다.

---

## 5. 파일로 쓰는 산출물의 길이는 따로 잡는다

대화 verbosity와 **별개로**, Opus 5가 디스크에 쓰는 파일(리포트·Markdown 문서·요약)이 이전 모델보다 길다. Claude가 작성한 문서를 제품에 싣는다면 길이 보정을 명시한다:

```text
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

---

## 6. 검증 지시는 넣는 게 아니라 지운다

**Opus 5는 시키지 않아도 자기 작업을 검증한다.** 프롬프트에 명시적 검증 지시("include a final verification step for any non-trivial task", "use a subagent to verify")가 있으면 **제거한다** — 이런 지시는 Opus 5에서 **과잉 검증**을 유발하며, 제거하면 **품질 손실 없이 토큰만 줄어든다.** 이전 모델용으로 하니스에 얹어둔 별도 검증 단계에도 같은 원칙이 적용된다.

자기 교정 요청도 같은 함정이다 — `"double-check your answer"`, `"re-verify before responding"` 같은 문구는 모델이 이미 하는 행동과 중첩되어 비용만 늘린다. **이것은 일반적인 프롬프팅 모범사례("자가 점검을 시켜라")를 정면으로 뒤집는 지점**이므로, 프롬프트 라이브러리에 그 규칙을 전역 적용 중이라면 이 모델에 한해 예외를 파야 한다.

> 글로벌 규칙 **Rule 5**(Verify by Execution)와 충돌하지 않는다 — Rule 5는 *무엇을 근거로 완료를 선언하는가*의 기준이고, 여기서 지우라는 것은 *모델에게 검증을 반복 지시하는 문구*다. 기준은 남기고 잔소리는 지운다.

---

## 7. 스코프 확장은 명시적으로 묶는다

Opus 5는 요청되지 않은 단계를 추가하거나, 작업이 무엇이어야 하는지에 대해 **자체 판단을 적용**해 스코프를 넓힐 수 있다. 좁은 작업에는 스코프를 못 박는다:

```text
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

> 글로벌 규칙 **Rule 1**(가정을 명시하고 넘겨짚지 않기)·**Rule 3**(Surgical Changes)·**Rule 12**(모든 부분에 응답)와 정확히 같은 취지다. 위 스니펫은 "전체를 끝내라(finish the whole task)"와 "요청 범위를 넘지 마라"를 한 문단에 함께 담는다 — 축소와 확장을 양쪽에서 막는 구조.

---

## 8. 서브에이전트는 상한을 건다 (4.8과 반대)

Opus 5는 **이전 모델보다 서브에이전트에 더 쉽게 위임한다.** 위임은 진짜로 독립적이고 규모 있는 작업 갈래에서는 이득이지만, 작은 작업에 적용하면 비용과 시간을 곱으로 늘린다(각 에이전트가 컨텍스트를 다시 세우고, 탐색을 다시 하고, 보고하고, 코디네이터가 그 보고를 다시 읽는다). 하니스가 서브에이전트를 지원한다면 **어떤 시나리오가 위임 대상인지 명시하거나, 스폰 개수에 결정적 상한**을 건다:

```text
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

마지막 절("검증용 서브에이전트 금지")은 §6과 같은 뿌리다 — 과잉 검증과 과잉 위임은 같은 문제의 두 얼굴이다.

> **4.8 가이드에서 넣었던 "위임을 더 하라"는 안내가 있다면 지운다.** 4.8은 서브에이전트를 **덜** 띄우는 모델이라 반대 처방이 필요했다.

---

## 9. 자기 교정 내레이션을 제한한다

Opus 5는 자기 실수를 잘 잡아 고치지만, **이전 발언에 대한 교정을 이전 모델보다 길게 설명한다.** 사용자향 제품에서는 이것이 갈팡질팡(thrash)으로 읽힌다. 사용자 결과를 바꾸는 교정만 남긴다:

```text
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

---

## 10. thinking을 끈 채 돌릴 때의 두 가지 결함

Opus 5는 thinking이 기본 ON이고 `disabled`는 effort `high` 이하에서만 가능하다(§1). **끈 상태에서만** 아래 두 아티팩트가 간헐적으로 나타난다. **두 결함 모두 1차 대응은 "thinking을 켜고 effort를 내려라"** — 공식 가이드는 대부분의 작업에서 *비슷한 비용이라면 `low` effort + thinking ON이 thinking OFF보다 낫다*고 명시한다.

**(1) 도구 호출이 텍스트로 새어 나온다.** 구조화된 `tool_use` 블록 대신 사용자향 텍스트에 도구 호출을 써버린다. **턴은 정상 종료되고, 호출은 실행되지 않으며, 에러도 없다** — 하니스 입장에서는 성공한 턴이 아무 일도 안 한 것이다. 에이전트 루프에서는 그 텍스트가 대화 히스토리에 남아 이후 턴까지 오염시킨다. 검색처럼 도구 의존도가 높은 워크로드에서 가장 흔하다.

**(2) `<thinking>` 태그가 응답에 노출된다.** 여기엔 직관에 반하는 규칙이 둘 있다 — **"생각하지 마라 / 추론하지 마라"류 지시가 있으면 삭제한다**(억제가 아니라 누출을 *증가*시킨다). 그리고 **thinking 태그를 이름으로 지목하지 않는다**(일반형 지시보다 효과가 낮다).

thinking을 반드시 꺼야 하는 통합이라면, 두 결함을 한 번에 완화하는 단일 지시를 쓴다:

```text
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

---

## 11. 역량 개선과 프롬프팅 함의

*Prompting Claude Opus 5*가 프롬프팅 관점에서 정리한 개선 항목이다.

| 영역 | 무엇이 좋아졌나 | 프롬프팅 함의 |
|------|----------------|---------------|
| **에이전트형 코딩** | 다중 파일 기능·대규모 리팩터링·엔드투엔드 작업에서 가장 강함. 스텁·플레이스홀더를 남기지 않고 완결 | **전체 작업 명세를 처음에 다 주고 그냥 돌린다** — 단계별로 떠먹이지 않는다 |
| **코드 리뷰·버그 발견** | 패스당 실제 버그 발견율이 높고 추가 발견도 대부분 진짜 이슈. **낮은 effort에서도 정확도 유지** | `"only report high-severity"`·`"be conservative"`는 문자 그대로 따라 **보고량을 줄인다** → 전부 보고시키고 **필터는 별도 패스**로 |
| **낮은 effort 효율** | `low`·`medium`이 상위 설정 대비 토큰·지연의 일부로 강한 품질 | effort 스윕을 새로 돌린다(§2) |
| **비전** | 차트·문서·다이어그램 이해, UI/프론트엔드 시각 재현 | **분석·크롭·시각 검증용 도구를 준다** — thinking을 올리는 것보다 비용 대비 효과가 크다. 이전 모델용 비전 우회 프롬프트는 재검증(불필요해졌을 수 있음) |
| **롱 컨텍스트** | 1M 창이 기본이자 최대, 창 전체에서 지시 이행·도구 호출·추론이 일관 | 컨텍스트 절약용 조기 압축 스캐폴딩을 재검토 |
| **오피스·문서** | 비자명한 수식이 든 다중 시트 스프레드시트, 구조가 잡힌 슬라이드 덱 | 따라야 할 **스타일·템플릿을 프롬프트로 명시**한다 |
| **멀티에이전트 조율** | writer-verifier 패턴이 잘 돌고 에이전트끼리 서로 덮어쓰는 사례가 적음 | 비용 민감 워크로드는 **위임 상한**(§8) |

---

## 신규 API 기능 (4.8 → 5)

- **`fallbacks: "default"`** — 거부 시 폴백 모델을 직접 나열하는 대신 Anthropic 권장 폴백을 **거부 카테고리별로 자동 라우팅**한다(cyber 계열은 Opus 4.8). 베타 헤더 `server-side-fallback-2026-07-01`(구 `-2026-06-01`은 명시 리스트 형태만 허용). **모델을 못 박는 것보다 `"default"`를 권장** — 폴백 모델이 폐기될 때 따라오는 마이그레이션이 사라진다.
- **대화 중간 도구 변경(베타)** — 베타 헤더 `mid-conversation-tool-changes-2026-07-01`. 세션 내내 고정된 도구 목록을 재전송하는 대신, **프롬프트 캐시를 보존한 채** 턴 사이에 도구를 추가·제거한다. 추가할 도구는 `tools[]`에 `defer_loading: true`로 미리 선언해 둔다.
- **프롬프트 캐시 최소 길이 512 토큰** — 4.8의 1,024에서 하향. 코드 변경 없이 캐시 대상이 넓어졌으므로, "너무 짧아서 캐시 안 된다"고 접어둔 프롬프트를 재확인한다.
- **Fast mode(리서치 프리뷰)** — Opus 5에서 사용 가능하나 **Claude API 전용**(Bedrock·Google Cloud·Foundry 불가). 가격 $10/$50 per MTok. Bedrock·Vertex·Foundry 라우트에서는 `speed: "fast"`를 빼야 한다.
- **레이트 리밋은 별도 버킷** — Opus 4.8/4.7/4.6/4.5는 통합 Opus 한도를 공유하지만 **Opus 5는 여기서 끌어오지 않는다.** 트래픽을 옮겨도 기존 버킷 여유가 생기지도, 한도를 물려받지도 않는다 — 물량 이전 전에 티어별 Opus 5 한도를 확인한다.

---

## 요약 체크리스트

Opus 5를 채택·튜닝할 때 점검할 항목이다. `⚠️`는 빠뜨리면 400 또는 조용한 잘림으로 이어지는 항목.

- [ ] ⚠️ `thinking: {type: "disabled"}` + `xhigh`/`max` 조합을 **전 호출부에서** 제거했는가(요청 단위 검증)
- [ ] ⚠️ `thinking`을 설정하지 않던 라우트의 **`max_tokens`를 재점검**했는가(이제 thinking이 예산을 함께 먹는다)
- [ ] `xhigh`/`max`에 **max output 64k+** 예산을 잡았는가
- [ ] effort를 **새로 스윕**했는가 — 기본 `high`에서 `low`/`medium` 쪽으로 먼저
- [ ] 응답 길이를 **effort가 아니라 프롬프트로** 잡았는가(+ 긴 시스템 프롬프트에는 말미 리마인더)
- [ ] 에이전트 진행 내레이션의 **케이던스·형태를 명시**했는가
- [ ] Claude가 쓰는 **파일 산출물 길이** 지시를 넣었는가
- [ ] 프롬프트·하니스의 **검증 지시를 삭제**했는가(`double-check`, `verify` 서브에이전트 포함)
- [ ] 좁은 작업에 **스코프 고정 지시**를 넣었는가
- [ ] 서브에이전트 **위임 상한**을 걸었는가(4.8의 "더 위임하라"는 지웠는가)
- [ ] 사용자향 제품에 **자기 교정 내레이션 제한**을 넣었는가
- [ ] 코드 리뷰 하니스가 **전부 보고 + 하류 필터** 구조인가
- [ ] thinking-off 경로가 남아 있다면 **통합 완화 지시**를 넣고, "생각하지 마라"류 문구를 지웠는가
- [ ] `stop_reason: "refusal"`을 `content` 읽기 **전에** 처리하고 `fallbacks: "default"`를 켰는가
- [ ] 512 토큰으로 낮아진 **캐시 최소치**를 반영해 짧은 프롬프트를 재검토했는가

---

## 참고 자료

- [Prompting Claude Opus 5 — Anthropic 공식 가이드](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) (이 문서의 1차 출처)
- [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5) (모델 소개·API 변경·가격·가용성)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) (§"Recommended effort levels for Claude Opus 5")
- [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) (4.8 → 5 단계별 절차)
- [Introducing Claude Opus 5 — Anthropic 발표](https://www.anthropic.com/news/claude-opus-5) (포지셔닝·벤치마크)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (모든 Claude 모델 공통 기법)
- [Claude Opus 4.8 프롬프팅 가이드](GUIDE-CLAUDE-OPUS-4-8-PROMPTING-2026-07-19-1828.md) · [Claude Fable 5 프롬프팅 가이드](GUIDE-CLAUDE-FABLE-5-PROMPTING-2026-07-11-1710.md)

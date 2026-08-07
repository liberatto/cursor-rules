---
type: guide
audience: Claude Sonnet 5를 API·에이전트·코딩 제품에 적용하는 개발자·프롬프트 작성자
related_docs:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 (1차 출처 — Anthropic 공식 프롬프팅 가이드)
  - https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5 (모델 소개 — API 변경·토크나이저·가격·가용성)
  - https://platform.claude.com/docs/en/build-with-claude/effort (effort 레벨 정의)
  - docs/GUIDE-CLAUDE-OPUS-5-PROMPTING-2026-07-26-2007.md (자매 문서 — 같은 세대 Opus 계열)
  - docs/GUIDE-CLAUDE-FABLE-5-PROMPTING-2026-07-11-1710.md (자매 문서 — 최상위 모델 Fable 5)
  - ClaudeCode/CLAUDE.v.5.2.md (이 저장소의 글로벌 지침 원본 — 본문은 참조하지 않는다. 대응 관계를 찾을 때 여기서 본다)
created: "2026-08-04 19:50"
status: active
description: "Sonnet 5는 Sonnet 4.6 프롬프트를 그대로 받지만, 400을 내는 API 변경이 셋(수동 extended thinking·샘플링 파라미터·기본 thinking) 있고 토크나이저가 같은 텍스트를 약 30% 더 많은 토큰으로 센다. 모델별 전용 공식 가이드가 존재하며, 그 내용을 튜닝 항목 단위로 정리한다."
---

# Claude Sonnet 5 프롬프팅 가이드

## 이 가이드가 다루는 것

Anthropic은 모델별 프롬프팅 문서를 별도 페이지로 운영하며, **Claude Sonnet 5에도 전용 페이지 *Prompting Claude Sonnet 5*가 존재한다.** 공식 문서 구조는 세 층이다 — 모델별 페이지(무엇이 달라졌고 무엇을 바꿔야 하는가), 공통 페이지 *Prompting best practices*(전 모델 공통 기법), 모델 소개 페이지 *What's new in Claude Sonnet 5*(API·가격·가용성). 이 문서는 그중 **모델별 페이지를 1차 출처로**, 실무에서 손대야 할 항목만 추린 가이드다.

Sonnet 5는 **코딩과 에이전트 작업에 강점**을 둔 모델이며, 기존 Sonnet 4.6 프롬프트에서 손질 없이 잘 동작한다. 즉 Opus 4.8 → Opus 5 이행처럼 "이전 처방이 역효과를 내는" 반전 항목이 많지는 않다. 대신 **조용히 비용과 잘림을 바꾸는 변경**이 셋 있고(기본 thinking, 새 토크나이저, 400을 내는 파라미터), 튜닝이 자주 필요한 행동 항목이 아홉 있다.

아래 영문 프롬프트 스니펫은 **시스템 프롬프트·에이전트 지시문에 그대로 붙여 쓰도록 설계된 원문**이라 원어 그대로 싣는다.

> **모델 사실 요약** (출처: *What's new in Claude Sonnet 5*): 모델 ID `claude-sonnet-5` · 1M 토큰 컨텍스트(기본값이자 최대값, 축소 변형 없음) · 최대 출력 128k 토큰 · **adaptive thinking 기본 ON** · effort 기본값 `high`(전 레벨 `low`~`max` 지원) · $3/$15 per MTok(4.6과 동일, 2026-08-31까지 도입가 $2/$10) · Claude API·Amazon Bedrock·Claude Platform on AWS·Google Cloud·Microsoft Foundry 가용 · **Priority Tier 미지원** · ZDR(zero data retention) 계약 조직 지원.

---

## 한눈에 보는 핵심 손잡이

| 손잡이 | 기본 권장 | 언제 조정하나 |
|--------|-----------|----------------|
| **effort** | 기본 `high` 유지 | 가장 어려운 코딩·에이전트 작업만 `xhigh`로 올린다. 비용 절감은 `medium`(4.6의 `high`에 상당) |
| **thinking** | 켠 채로 둔다(기본값) | 4.6에서 thinking을 끄고 쓰던 경로는 **끄지 말고 effort를 내리는 쪽**을 먼저 시도한다 |
| **`max_tokens`** | **재산정 필수** | thinking이 예산을 함께 먹고, 토크나이저가 토큰을 약 30% 더 센다 — 4.6 기준값은 잘릴 수 있다 |
| **응답 길이** | 과제 복잡도에 맞춰 자동 조절 | 제품이 특정 길이·문체에 의존하면 프롬프트로 명시한다 |
| **샘플링 파라미터** | **전부 제거** | `temperature`·`top_p`·`top_k`의 비기본값은 400이다. 문체 다양성은 프롬프트로 대체 |

핵심 한 문장 — **Sonnet 5는 프롬프트를 그대로 받지만 토큰 예산과 요청 파라미터는 그대로 받지 않는다. 프롬프트 튜닝보다 `max_tokens` 재산정과 파라미터 정리가 먼저다.**

---

## 1. API 파괴적 변경 세 가지

*What's new in Claude Sonnet 5* 기준. 셋 모두 **400 또는 조용한 잘림**으로 이어지므로 프롬프트 튜닝보다 먼저 처리한다.

**(1) adaptive thinking이 기본으로 켜진다.** Sonnet 4.6에서는 `thinking` 필드를 빼면 thinking 없이 돌았지만, Sonnet 5는 같은 요청이 **adaptive thinking으로 실행**된다. 문제는 예산이다 — **`max_tokens`는 thinking + 응답 텍스트 합계의 하드 캡**이므로, 4.6에서 thinking 없이 돌며 `max_tokens`를 빠듯하게 잡아둔 경로는 응답 중간에 잘린다. 끄려면 `thinking: {type: "disabled"}`를 명시한다. 다만 4.6에서 thinking-off로 쓰던 워크로드는 **끄는 대신 낮은 effort로 켜 두는 쪽**을 먼저 시험하라는 것이 공식 권고다.

**(2) 샘플링 파라미터가 거부된다.** `temperature`·`top_p`·`top_k`를 **비기본값**으로 설정하면 400이다. 파라미터를 생략하거나 기본값을 넘기는 것은 허용된다. Sonnet 계열에서는 이번이 처음이며, 같은 제약이 Opus 4.7에서 먼저 도입됐다. 모델 동작 유도는 시스템 프롬프트로 옮긴다(→ §9).

**(3) 수동 extended thinking이 제거됐다.** `thinking: {type: "enabled", budget_tokens: N}`은 4.6에서 폐기 예고 상태였고 Sonnet 5에서는 **400**이다. adaptive thinking + effort 파라미터로 대체한다.

```python
# Sonnet 5에서 400
thinking = {"type": "enabled", "budget_tokens": 32000}

# 대체
thinking = {"type": "adaptive"}
```

**상속된 제약**: assistant 메시지 prefill은 4.6과 동일하게 **400**이다. 출력 형식 고정이 필요하면 structured outputs(`output_config.format`)나 시스템 프롬프트 지시를 쓴다. 그 외 도구 정의와 응답 형태는 4.6과 동일하므로, 위 셋만 정리하면 나머지 코드는 그대로 동작한다.

---

## 2. 새 토크나이저와 토큰 예산 재산정

Sonnet 5는 새 토크나이저를 쓴다. **같은 입력 텍스트가 Sonnet 4.6 대비 약 30% 더 많은 토큰으로 계산된다**(정확한 증가폭은 콘텐츠에 따라 다르다). 요청·응답·스트리밍 이벤트의 형태는 그대로이므로 **API 변경은 아니지만, 토큰으로 재거나 예산 잡는 모든 것이 움직인다.**

| 영향 지점 | 무엇이 달라지나 |
|-----------|----------------|
| **토큰 카운트** | `usage` 필드와 token counting 결과가 같은 텍스트에서 더 크게 나온다. 이전 모델에서 측정한 값을 재사용하지 않는다 |
| **컨텍스트 수용량** | 창은 1M 토큰 그대로지만 토큰당 담기는 텍스트가 줄어 **같은 창에 들어가는 분량이 감소**한다 |
| **`max_tokens`** | 예상 출력 길이에 가깝게 잡아둔 한도는 **동등한 출력을 잘라낸다**. 재산정 대상 |
| **요청당 비용** | 토큰당 단가는 그대로($3/$15)지만 같은 텍스트가 더 많은 토큰이 되므로 **동등 요청의 비용이 달라진다** |

측정은 추정하지 말고 token counting API로 다시 잰다 — 프롬프트를 `claude-sonnet-5` 기준으로 재측정한 뒤 `max_tokens`와 압축 트리거를 조정한다.

---

## 3. effort 보정과 교차 매핑

effort 기본값은 `high`이며 이는 **Sonnet 4.6과 동일**하다. 가장 어려운 코딩·에이전트 작업에서만 `xhigh`로 올린다.

| effort | Sonnet 5에서의 용도 |
|--------|--------------------|
| **`max`** | 토큰 지출 제약 없이 절대 최대 역량이 필요한 경우 |
| **`xhigh`** | **가장 어려운 코딩·에이전트 작업의 권장값** |
| **`high`** | **기본값.** 대부분의 용도에서 토큰과 지능의 균형점 |
| **`medium`** | 지능을 일부 내주고 토큰을 줄여야 하는 비용 민감 용도 |
| **`low`** | 짧고 범위가 좁은 작업, 지능 민감도가 낮은 지연 우선 워크로드 |

**세대 간 교차 매핑**(마이그레이션 시 대략적 기준):

- Sonnet 5의 `medium` ≈ Sonnet 4.6의 `high`
- Sonnet 5의 `high` ≈ Sonnet 4.6의 `max`

즉 4.6에서 `high`로 돌던 워크로드는 Sonnet 5의 `medium`으로 내려도 지능이 비슷하다. 벤치마크할 때는 **effort 이름이 아니라 관측된 thinking 길이로 맞춘다.**

**Sonnet 5는 effort를 엄격히 지킨다 — 특히 낮은 쪽에서.** `low`·`medium`에서는 요청받은 범위로 작업을 한정하고 그 이상을 하지 않는다. 지연과 비용에는 유리하지만, 중간 난이도 작업을 `low`로 돌리면 **추론이 얕아질 위험**이 있다. 복잡한 문제에서 얕은 추론이 관측되면 프롬프트로 우회하지 말고 **effort를 `high`·`xhigh`로 올린다.** 지연 때문에 `low`를 유지해야 한다면 표적 지시를 넣는다:

```text
This task involves multistep reasoning. Think carefully through the problem before responding.
```

> **`high`·`xhigh`·`max`로 돌릴 때는 `max_tokens`에 여유를 남긴다.** 긴 작업에서 adaptive thinking이 예산의 큰 몫을 쓸 수 있고, 예산이 빠듯하면 **응답이 거의 전부 thinking이고 답변이 잘린 채 `stop_reason: "max_tokens"`로 끝난다.** `max_tokens`를 올리거나 `medium`으로 내리면 해소된다. 여기에 §2의 토크나이저 증가분이 겹친다.

---

## 4. adaptive thinking 트리거 조절

adaptive thinking의 발동 빈도는 프롬프트로 조절 가능하다. **시스템 프롬프트가 크거나 복잡하면 thinking 블록이 원하는 것보다 자주 나오는 경향**이 있다. 억제하려면 명시한다:

```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```

반대로 `medium`에서 어려운 워크로드를 돌리며 **추론 부족**이 보이면, 1차 레버는 프롬프트가 아니라 **effort 상향**이다. 더 세밀한 제어가 필요할 때만 프롬프트로 직접 요구한다.

어느 방향이든 **프롬프트 변경의 효과를 성능 지표로 측정한다** — 공식 가이드가 이 항목에 대해 특별히 반복하는 주의사항이다.

---

## 5. 응답 길이 보정

Sonnet 5는 고정된 verbosity를 쓰지 않고 **과제 복잡도에 맞춰 응답 길이를 조절한다.** 단순 조회에는 짧게, 열린 분석에는 길게 답한다. 제품이 특정 문체나 길이에 의존한다면 프롬프트 튜닝이 필요하다. 줄이려면:

```text
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

과잉 설명처럼 **특정 유형의 장황함**이 보이면 그 유형을 겨냥한 지시를 추가한다. 이때 **"하지 마라"는 부정형 지시나 금지 예시보다, 원하는 간결함을 보여주는 긍정 예시가 대체로 더 효과적**이다.

---

## 6. 도구 호출 트리거

**Sonnet 5는 Sonnet 4.6보다 에이전트 성향이 강하다** — 도구를 더 적극적으로 집고 자체 검증 루프를 더 자주 돈다. 조정 레버는 둘이다.

- **thinking을 끄면 도구를 덜 집는다.** thinking-off 상태에서는 도구 호출이나 검색을 고려할 가능성이 낮아지므로, **도구 호출에 의존하는 하니스가 thinking을 끈다면 시스템 프롬프트에 명시적 유도 문구를 넣는다.**
- **effort가 도구 사용량을 좌우한다.** `high`·`xhigh`에서 에이전트형 검색과 코딩의 도구 사용량이 뚜렷하게 늘어난다.

도구 사용을 더 원하는 시나리오에서는 **언제 어떻게 그 도구를 써야 하는지 프롬프트에 명시**한다 — 예를 들어 웹 검색 도구가 안 쓰인다면 어떤 상황에서 왜 호출해야 하는지 서술한다.

---

## 7. 사용자향 진행 업데이트

Sonnet 5는 긴 에이전트 실행 중 **규칙적이고 품질 높은 업데이트를 기본으로 제공한다.** 따라서 이전 모델용으로 얹어둔 강제 스캐폴딩("After every 3 tool calls, summarize progress")이 있다면 **제거를 먼저 시도한다.**

기본 업데이트의 길이나 내용이 용도에 안 맞으면, 없애는 대신 **원하는 업데이트의 모습을 프롬프트에 서술하고 예시를 준다.**

---

## 8. 문자 그대로의 지시 이행

Sonnet 5는 프롬프트를 **문자 그대로, 명시된 대로** 해석한다 — 특히 낮은 effort에서 두드러진다. 한 항목에 준 지시를 다른 항목으로 조용히 일반화하지 않고, 하지 않은 요청을 추론하지도 않는다.

이 문자주의의 이점은 정밀성이다. **세밀하게 튜닝한 프롬프트, 구조화된 추출, 예측 가능한 동작이 필요한 파이프라인** 같은 API 용도에서 대체로 더 나은 결과를 낸다. 대신 **지시를 넓게 적용하려면 범위를 명시해야 한다**:

```text
Apply this formatting to every section, not just the first one.
```

---

## 9. 톤·문체와 temperature 대체

새 모델이 나올 때마다 그렇듯 **장문 글쓰기의 문체가 이동할 수 있다.** 제품이 특정 목소리에 의존한다면 스타일 프롬프트를 새 기준선에 맞춰 재평가한다. 예를 들어 더 따뜻하고 대화적인 톤이 필요하면:

```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

**이전에 `temperature`로 문체 다양성을 얻고 있었다면 대체가 필요하다** — §1에서 본 대로 비기본값은 400이다. 다양성은 시스템 프롬프트 지시로만 얻는다.

---

## 10. 프론트엔드·디자인 기본값

Sonnet 5는 열린 프론트엔드·디자인 요청에서 **일관된 기본 시각 스타일로 수렴**할 수 있다. 그 하우스 스타일이 잘 맞는 요청도 있지만, 대시보드·개발자 도구·핀테크·헬스케어·엔터프라이즈 앱에서는 어긋난다.

**일반적 지시("그 색 쓰지 마", "깔끔하고 미니멀하게")는 다양성을 만들지 않고 다른 고정 팔레트로 옮겨갈 뿐이다.** 안정적으로 작동하는 접근은 둘이다.

**(1) 구체적 대안을 명시한다.** 모델은 명시적 스펙을 정밀하게 따른다 — 색상 hex 값, 서체, 레이아웃 구조, 코너 반경, 여백 규칙, 전환 시간까지 지정하면 그대로 구현한다.

**(2) 만들기 전에 방향을 제안시킨다.** 기본값을 깨고 선택권을 사용자에게 넘긴다. `temperature`를 쓸 수 없으므로 **실행마다 의미 있게 다른 디자인 방향을 얻는 권장 수단**이 바로 이 방식이다.

```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

사용자들이 "AI slop"이라 부르는 범용 미감을 피하려면 시스템 프롬프트에 짧은 지시를 함께 넣는다:

```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

---

## 11. 인터랙티브 코딩 제품

**단일 사용자 턴으로 도는 자율·비동기 코딩 에이전트**와 **여러 사용자 턴을 오가는 인터랙티브·동기 코딩 에이전트**는 토큰 사용량과 동작이 다르다. 코딩 제품에서 성능과 토큰 효율을 함께 올리려면 세 가지를 적용한다.

- effort를 `xhigh` 또는 `high`로 쓴다.
- auto 모드 같은 **자율 기능을 추가**한다.
- 사용자에게 요구되는 **상호작용 횟수를 줄인다.**

상호작용을 줄일 때는 **첫 사용자 턴에 작업·의도·제약을 앞당겨 명시하는 것이 핵심**이다. 명확하고 정확한 작업 서술을 처음에 주면 자율성과 지능을 최대화하면서 사용자 턴 이후의 추가 토큰 사용을 최소화한다. 반대로 **모호하거나 덜 명세된 프롬프트를 여러 턴에 걸쳐 점진적으로 전달하면 토큰 효율이 떨어지고 때로는 성능도 떨어진다.**

---

## 12. 코드 리뷰 하니스의 recall 착시

이전 모델에 맞춰 튜닝한 코드 리뷰 하니스를 Sonnet 5로 옮기면 **처음에 recall이 떨어져 보일 수 있다. 이것은 역량 퇴행이 아니라 하니스 효과다.**

리뷰 프롬프트에 `"only report high-severity issues"`·`"be conservative"`·`"don't nitpick"` 같은 문구가 있으면, Sonnet 5는 이전 모델보다 **그 지시를 더 충실히 따른다** — 코드는 똑같이 깊게 조사하고 버그도 찾아내지만, 명시된 기준에 못 미친다고 판단한 발견을 보고하지 않는다. 결과적으로 **조사 깊이는 같은데 보고로 전환되는 비율만 낮아지고**, 낮은 심각도 버그에서 특히 두드러진다. 정밀도는 오르지만 측정된 recall은 떨어진다.

권장 프롬프트:

```text
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

실제 2단계가 없어도 이 프롬프트는 쓸 수 있지만, **확신도 필터링을 발견 단계 밖으로 빼는 편이 대체로 낫다.** 하니스에 별도의 검증·중복 제거·순위 단계가 있다면, 발견 단계의 임무가 필터링이 아니라 **커버리지**임을 모델에게 명시적으로 알린다.

단일 패스 자체 필터링을 원한다면 `"important"` 같은 정성 용어 대신 **기준선을 구체적으로 적는다** — 예를 들어 "잘못된 동작·테스트 실패·오해를 유발하는 결과를 낳을 수 있는 버그는 모두 보고하고, 순수 스타일·네이밍 취향 같은 사소한 지적만 생략하라". 프롬프트 변경은 eval이나 테스트 케이스 부분 집합에 대해 반복 검증해 recall·F1 개선을 확인한다.

---

## 13. computer use 해상도

Sonnet 5는 `computer_20251124` 도구 버전을 지원한다. computer use 역량은 **최대 2576px / 3.75MP**까지의 해상도 전반에서 작동한다.

| 설정 | 특성 |
|------|------|
| **1080p** | 성능과 비용의 균형점(Anthropic 내부 테스트 기준 권장) |
| **720p · 1366×768** | 비용 민감 워크로드용 저비용 옵션, 성능은 여전히 양호 |

이상적인 설정은 용도별로 직접 테스트해 찾는다. effort 조정도 동작 튜닝에 도움이 된다.

---

## 사이버보안 세이프가드

Sonnet 5는 **실시간 사이버보안 세이프가드를 갖춘 첫 Sonnet 등급 모델**이다. 금지되거나 고위험인 사이버보안 주제가 얽힌 요청은 거부될 수 있다.

**거부는 오류가 아니라 HTTP 200 성공 응답으로 돌아온다** — `stop_reason: "refusal"`이 실린다. 따라서 `content`를 읽기 **전에** `stop_reason`을 분기해야 한다. 무조건 `content[0]`을 읽는 코드는 거부 응답에서 깨진다.

---

## 요약 체크리스트

Sonnet 4.6에서 Sonnet 5로 옮기거나 새로 튜닝할 때 점검할 항목이다. `⚠️`는 빠뜨리면 400 또는 조용한 잘림으로 이어지는 항목.

- [ ] ⚠️ `thinking: {type: "enabled", budget_tokens: N}`을 **전 호출부에서 제거**하고 `{type: "adaptive"}`로 바꿨는가
- [ ] ⚠️ `temperature`·`top_p`·`top_k`의 **비기본값을 전부 제거**했는가
- [ ] ⚠️ `thinking`을 설정하지 않던 라우트의 **`max_tokens`를 재점검**했는가(이제 thinking이 예산을 함께 먹는다)
- [ ] ⚠️ 토크나이저 변경(약 +30%)을 반영해 **프롬프트를 재측정하고 `max_tokens`·압축 트리거를 조정**했는가
- [ ] assistant **prefill**이 남아 있지 않은가(4.6부터 400 — structured outputs로 대체)
- [ ] effort를 **교차 매핑 기준으로 재설정**했는가(4.6 `high` → 5 `medium`이 대략 동등)
- [ ] `high`·`xhigh`·`max` 라우트에 **`max_tokens` 여유**를 남겼는가
- [ ] 4.6에서 thinking-off로 돌던 경로를 **낮은 effort + thinking-on**으로 먼저 시험했는가
- [ ] thinking 발동이 잦다면 **트리거 억제 지시**를 넣고 효과를 측정했는가
- [ ] 제품이 길이·문체에 의존한다면 **간결성 지시**를 넣었는가(부정형보다 긍정 예시)
- [ ] thinking-off 하니스에 **도구 사용 유도 문구**를 넣었는가
- [ ] "N번 호출마다 요약" 류 **강제 진행 보고 스캐폴딩을 제거**해 봤는가
- [ ] 넓게 적용해야 할 지시에 **범위를 명시**했는가(문자 그대로 해석한다)
- [ ] `temperature` 기반 문체·디자인 다양성을 **프롬프트 기반(4방향 제안 등)으로 대체**했는가
- [ ] 코드 리뷰 하니스가 **전부 보고 + 하류 필터** 구조인가(보수적 보고 지시를 걷어냈는가)
- [ ] 인터랙티브 코딩 제품에서 **첫 턴에 작업·의도·제약을 명시**하는 구조인가
- [ ] `stop_reason: "refusal"`을 `content` 읽기 **전에** 처리하는가
- [ ] Priority Tier에 의존하는 경로가 없는가(**Sonnet 5 미지원**)

---

## 참고 자료

- [Prompting Claude Sonnet 5 — Anthropic 공식 가이드](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5) (이 문서의 1차 출처)
- [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5) (모델 소개·API 변경·토크나이저·가격·가용성)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (모든 Claude 모델 공통 기법 — 모델별 페이지가 먼저 오고 공통 기법이 뒤따르는 구조)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) (effort 레벨 정의)
- [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) (Sonnet 4.6 → Sonnet 5 절차)
- [Introducing Claude Sonnet 5 — Anthropic 발표](https://www.anthropic.com/news/claude-sonnet-5) (포지셔닝·벤치마크)
- [Claude Opus 5 프롬프팅 가이드](GUIDE-CLAUDE-OPUS-5-PROMPTING-2026-07-26-2007.md) · [Claude Fable 5 프롬프팅 가이드](GUIDE-CLAUDE-FABLE-5-PROMPTING-2026-07-11-1710.md)

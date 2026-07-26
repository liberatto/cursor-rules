---
type: guide
audience: Claude Opus 4.8을 도구·에이전트·워크플로우에 적용하는 개발자·프롬프트 작성자
related_docs:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 (1차 출처 — Anthropic 공식 프롬프팅 가이드)
  - https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8 (모델 소개 — API 변경·가격·가용성)
  - https://platform.claude.com/docs/en/about-claude/models/migration-guide (4.7→4.8 마이그레이션)
  - docs/GUIDE-CLAUDE-FABLE-5-PROMPTING-2026-07-11-1710.md (자매 문서 — 상위 모델 Fable 5 프롬프팅)
  - /Users/sspark/.claude/CLAUDE.md (이 저장소의 글로벌 규칙 — 아래 습관 다수와 대응)
created: "2026-07-19 18:28"
status: active
description: "Opus 4.8은 응답 길이를 작업 복잡도에 맞춰 스스로 조절하고, effort를 1차 손잡이로 삼으며, 지시를 문자 그대로 이행하는 모델이다. 이 가이드는 Anthropic 공식 프롬프팅 문서를 바탕으로 무엇이 달라졌고 어떤 프롬프트를 넣어야 하는지 정리한다."
---

# Claude Opus 4.8 프롬프팅 가이드

## 이 가이드가 다루는 것

Claude Opus 4.8은 **복잡한 에이전트형 코딩과 엔터프라이즈 작업**을 겨냥해 Opus 4.7 위에 세워진 모델이다. 장기 에이전트 작업·지식 노동·비전·메모리 작업에 특히 강하고, 기존 4.7 프롬프트에서도 큰 손질 없이 잘 동작한다. 이 문서는 Anthropic 공식 가이드 *Prompting Claude Opus 4.8*을 1차 출처로, 실제로 프롬프트를 어떻게 조정해야 하는지 정리한 실무 가이드다. 아래 영문 프롬프트 스니펫은 **시스템 프롬프트·에이전트 지시문에 그대로 붙여 쓰도록 설계된 원문**이라 원어 그대로 싣는다.

> **자매 문서**: 상위 모델인 Claude Fable 5는 별도 가이드(*Claude Fable 5 프롬프팅 가이드*)를 참조한다. Opus 4.8은 Fable 5가 안전 분류기(공격적 사이버보안·생명과학·추론 추출)로 요청을 거부(`stop_reason: "refusal"`)할 때 **폴백 대상 모델**이기도 하다.

> **모델 사실 요약** (출처: *What's new in Claude Opus 4.8*): 모델 ID `claude-opus-4-8` · 기본 1M 토큰 컨텍스트(API·Bedrock·Google Cloud·Microsoft Foundry) · 최대 출력 128k 토큰 · adaptive thinking · effort 기본값 `high`(API·Claude Code 전 표면).

---

## 한눈에 보는 핵심 손잡이

| 손잡이 | 기본 권장 | 언제 조정하나 |
|--------|-----------|----------------|
| **effort** | 코딩·에이전트 `xhigh`, 지능 민감 작업 최소 `high` | 얕은 추론이 보이면 프롬프트 대신 effort를 올린다 |
| **thinking** | `{type: "adaptive"}`일 때만 켜짐 | 과하게 생각하면 스티어링, 부족하면 effort부터 |
| **응답 길이** | 작업 복잡도에 맞춰 자동 조절 | 특정 verbosity가 필요하면 명시(긍정 예시가 효과적) |
| **서브에이전트** | 기본은 적게 띄움 | 팬아웃이 필요하면 언제 위임할지 명시 |

핵심 한 문장 — **Opus 4.8은 effort를 1차 손잡이로 삼고 지시를 문자 그대로 이행하므로, "더 세게 생각하게" 하려면 프롬프트로 우회하지 말고 effort를 올리고, "넓게 적용"하려면 스코프를 명시한다.**

---

## 1. 응답 길이는 작업 복잡도에 맞춰 자동 조절된다

Opus 4.8은 고정된 verbosity를 기본값으로 두지 않고, **작업이 얼마나 복잡하다고 판단하는지에 맞춰 응답 길이를 보정**한다. 단순 조회는 짧게, 개방형 분석은 훨씬 길게 답한다. 제품이 특정 문체·길이에 의존한다면 프롬프트로 튜닝한다. 장황함을 줄이려면:

```text
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

과잉 설명 같은 구체적 verbosity 패턴이 보이면 추가 지시를 넣되, **"하지 마라"는 부정 지시보다 적절한 간결도를 보여주는 긍정 예시가 더 효과적**이다.

> 글로벌 규칙 **Response Discipline**("Lead with the outcome", "Concise by selection")과 대응한다.

---

## 2. effort와 thinking 깊이를 보정한다

`effort`는 Opus 4.8에서 **지능 대 토큰 소비**를 조절하는 파라미터이며, **이전 어떤 Opus보다 이 모델에서 더 중요하다.** 업그레이드 시 적극적으로 실험한다.

| effort | 용도 |
|--------|------|
| **`max`** | 지능 극한 작업. 성능 이득이 있으나 토큰 대비 수확 체감·과잉사고 위험. 테스트 후 채택 |
| **`xhigh`** | **대부분의 코딩·에이전트 작업에 최적** |
| **`high`** | 토큰·지능 균형. 지능 민감 작업의 **최소 기준선** |
| **`medium`** | 비용 민감·지능 트레이드오프 허용 작업 |
| **`low`** | 짧고 스코프 좁은 작업·지연 민감 작업 전용 |

Opus 4.8은 **effort를 엄격히 준수**한다(특히 낮은 쪽). `low`·`medium`에서는 요청받은 만큼만 하므로 지연·비용에 좋지만, 중간 복잡도 작업을 `low`로 돌리면 **과소 사고(under-thinking)** 위험이 있다. 복잡한 문제에서 얕은 추론이 보이면 **프롬프트로 우회하지 말고 effort를 `high`/`xhigh`로 올린다.** 지연 때문에 `low`를 유지해야 한다면 표적 지시를 넣는다:

```text
This task involves multistep reasoning. Think carefully through the problem before responding.
```

**thinking은 `thinking: {type: "adaptive"}`를 명시할 때만 켜진다.** adaptive thinking의 발동 조건은 스티어링 가능하다 — 크거나 복잡한 시스템 프롬프트 때문에 원하는 것보다 자주 생각하면 다음처럼 억제한다:

```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multistep reasoning. When in doubt, respond directly.
```

반대로 `medium`에서 어려운 작업에 과소 사고가 보이면 **첫 레버는 effort 상향**이고, 더 세밀한 제어가 필요할 때만 직접 프롬프트한다.

> **참고**: `max`·`xhigh`로 돌릴 때는 서브에이전트·도구 호출을 넘나들며 생각·행동할 여유를 주도록 **max output 토큰 예산을 크게** 잡는다. **64k에서 시작**해 튜닝한다.

> **effort 재보정(4.7→4.8)**: 각 레벨의 토큰 할당이 바뀌었다 — `medium`은 다소 늘고, `high`는 다소 줄고, `xhigh`는 크게 늘었다. 4.7 기준으로 튜닝했다면 비용·지연을 **재베이스라인**한 뒤 조정한다.

---

## 3. 도구 호출보다 추론을 선호한다

Opus 4.8은 **도구 호출보다 추론을 선호**하는 경향이 있고, 대부분의 경우 이쪽이 더 나은 결과를 낸다. 도구 사용을 늘리는 유용한 레버는 **effort 상향**이다 — `high`/`xhigh`는 에이전트 검색·코딩에서 도구 사용을 크게 늘린다. 특정 시나리오에서 더 많은 도구 사용을 원하면, **언제·어떻게 도구를 써야 하는지 프롬프트로 명시**한다(예: 웹 검색 도구를 안 쓰면, 왜·어떻게 써야 하는지 분명히 기술).

> *What's new*가 밝힌 개선점: 4.7에서 일부 사용자가 보고한 "필요한 도구 호출을 건너뛰는" 문제가 줄었다(better tool triggering).

---

## 4. 사용자용 진행 업데이트는 그냥 둔다

Opus 4.8은 긴 에이전트 트레이스 내내 **더 규칙적이고 질 높은 진행 업데이트**를 사용자에게 제공한다. `"After every 3 tool calls, summarize progress"` 같은 **중간 상태 강제 스캐폴딩이 있다면 제거**해 본다. 업데이트의 길이·내용이 용도에 안 맞으면, 어떤 모습이어야 하는지 프롬프트로 명시하고 예시를 준다.

---

## 5. 지시를 문자 그대로 이행한다

Opus 4.8은 프롬프트를 **문자 그대로·명시적으로 해석**한다(특히 낮은 effort에서). 한 항목의 지시를 다른 항목으로 조용히 일반화하지 않고, 하지 않은 요청을 넘겨짚지 않는다. 이 문자주의의 이점은 **정밀성과 스래싱 감소**로, 세심히 튜닝한 프롬프트·구조화 추출·예측 가능한 파이프라인에 유리하다. 지시를 **넓게 적용**하게 하려면 스코프를 명시한다:

```text
Apply this formatting to every section, not just the first one.
```

> 글로벌 규칙 **Rule 1**(넘겨짚지 말고 가정을 명시)·**Rule 12**(요청의 모든 부분에 응답)와 상보적이다 — 모델이 문자대로 이행하는 만큼, 요청자가 스코프를 명시할 책임이 커진다.

---

## 6. 문체는 직설적·단정적 기본값을 갖는다

새 모델답게 장문 산출의 문체가 이동할 수 있다. Opus 4.8은 **직설적·단정적(direct, opinionated)** 문체에, 검증조 표현(validation-forward)을 최소화하고 이모지를 아껴 쓰는 쪽으로 기운다. 제품이 특정 목소리에 의존하면 새 베이스라인 기준으로 스타일 프롬프트를 재검토한다. 더 따뜻하거나 대화체가 필요하면:

```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

---

## 7. 서브에이전트는 기본적으로 적게 띄운다

Opus 4.8은 **기본적으로 서브에이전트를 더 적게** 띄운다(상위 모델 Fable 5와 반대 방향). 이 동작은 스티어링 가능하므로, **언제 위임이 바람직한지** 명시적으로 안내한다. 코딩용 예시:

```text
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

---

## 8. 프론트엔드 기본 미감을 이해한다

Opus 4.8은 강한 디자인 본능과 함께 **일관된 기본 하우스 스타일**을 갖는다 — 따뜻한 크림/오프화이트 배경(≈`#F4F1EA`), serif 디스플레이 서체(Georgia, Fraunces, Playfair), 이탤릭 단어 강조, terracotta/amber 액센트. 에디토리얼·호스피탈리티·포트폴리오에는 잘 맞지만 대시보드·개발도구·핀테크·헬스케어·엔터프라이즈 앱에는 어색하다. 이 기본값은 **끈질기다** — `"don't use cream"` 같은 일반 지시는 다양성 대신 또 다른 고정 팔레트로 이동시킬 뿐이다. 확실히 통하는 두 방법:

**(1) 구체적 대안을 명시한다** — 모델은 명시적 스펙을 정확히 따른다(팔레트 hex, 서체, radius, 간격 등을 구체적으로 기술). **(2) 짓기 전에 옵션을 제안하게 한다** — 기본값을 깨고 사용자에게 통제권을 준다. 과거 `temperature`로 디자인 다양성을 얻었다면 이 방법을 쓴다(temperature는 4.8에서 미지원):

```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction.
```

또한 Opus 4.8은 이전 모델보다 **"AI slop" 미감을 피하는 데 프롬프팅이 덜 필요**하다. 다양성 조언과 함께 쓰기 좋은 스니펫:

```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

---

## 9. 인터랙티브 코딩 제품

Opus 4.8의 토큰 사용·동작은 **자율/비동기 코딩 에이전트(단일 사용자 턴)** 와 **인터랙티브/동기 코딩 에이전트(다중 사용자 턴)** 사이에서 다르다. 인터랙티브 설정에서 토큰을 더 쓰는데, 사용자 턴 이후 더 많이 추론하기 때문이다. 이는 긴 인터랙티브 세션의 일관성·지시 이행·코딩 역량을 높이지만 토큰도 늘린다. 성능·효율을 함께 극대화하려면 **`xhigh`/`high` effort + auto 모드 같은 자율 기능 + 필요한 사용자 상호작용 축소**를 쓴다. 상호작용을 줄일 때는 **첫 사용자 턴에서 작업·의도·제약을 명확히 명세**하는 것이 중요하다 — 모호하고 여러 턴에 걸쳐 점진적으로 전달되는 프롬프트는 효율·성능을 상대적으로 떨어뜨린다.

> 글로벌 규칙 **Rule 4**(성공 기준을 먼저 정의)·**Rule 1**(무엇을 위한 요청인지 먼저 파악)과 대응한다.

---

## 10. 코드 리뷰 하니스

Opus 4.8은 이전 모델보다 **버그를 유의미하게 더 잘 찾는다**(내부 eval에서 recall·precision 모두 상승). 그런데 이전 모델용으로 튜닝한 리뷰 하니스에서는 처음에 **recall이 낮아 보일 수 있다** — 역량 퇴행이 아니라 하니스 효과다. `"only report high-severity issues"`·`"be conservative"`·`"don't nitpick"` 같은 지시를 Opus 4.8이 **더 충실히 따라**, 조사는 똑같이 깊게 하고도 기준 미달로 판단한 발견을 보고하지 않기 때문이다. precision은 오르지만 측정 recall은 떨어질 수 있다. 발견 단계에서 **coverage를 목표로** 삼게 하려면:

```text
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

단일 패스에서 자체 필터링을 원하면 `"important"` 같은 정성적 표현 대신 **기준을 구체적으로**: 예) "report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences." eval 서브셋에 프롬프트를 반복 검증해 recall/F1 이득을 확인한다.

> 글로벌 규칙 **Rule 10**(중요도 라벨은 붙이되 필터링은 독자 몫)과 정확히 같은 취지다 — 발견은 다 올리고 순위·필터는 하류에서.

---

## 11. 컴퓨터 사용(Computer Use)

컴퓨터 사용은 여러 해상도에서 동작하며 **최대 2576px / 3.75MP**까지 지원한다. 내부 테스트상 **1080p 전송이 성능·비용 균형점**이다. 비용 민감 워크로드는 720p·1366×768이 저비용 대안이면서 성능이 강하다. effort 실험으로도 동작을 튜닝할 수 있다.

---

## API·마이그레이션 요점 (4.7 → 4.8)

*What's new in Claude Opus 4.8* 기준. 대부분 4.7 코드는 무수정으로 돈다.

- **effort 기본값 `high`** — 전 표면(API·Claude Code). 명시 설정은 유지된다.
- **adaptive thinking 전용** — `thinking: {type: "enabled", budget_tokens: N}`은 400 에러. `{type: "adaptive"}`로 켜고 깊이는 `output_config.effort`로 조절. `thinking` 필드를 아예 빼면 thinking 없이 실행.
- **샘플링 파라미터 미지원** — `temperature`·`top_p`·`top_k` 비기본값은 400. 프롬프트로 유도한다.
- **중간 대화 시스템 메시지** — 사용자 턴 직후 `role: "system"` 허용. 긴 대화에서 전체 시스템 프롬프트 재기술 없이 지시를 덧붙이면서 앞 턴의 프롬프트 캐시 히트를 보존(입력 비용 절감). 베타 헤더 불필요.
- **거부 stop 상세** — 거부 응답의 `stop_details`가 공개 문서화. 거부 범주를 구분해 사용자를 알맞은 다음 단계로 라우팅 가능.
- **Fast mode(리서치 프리뷰)** — `speed: "fast"` + `fast-mode-2026-02-01` 베타 헤더로 동일 모델에서 출력 토큰/초 최대 2.5배(프리미엄 가격). Claude Code에서는 `/fast`로 토글.
- **프롬프트 캐시 최소 길이 1,024 토큰** — 4.7의 2,048에서 하향. 짧은 프롬프트도 캐시 가능.
- **4.6 이하에서 올라온다면** — 위 4.7→4.8 절차만으로는 안 되는 파괴적 변경이 있으니 마이그레이션 가이드의 4.6 섹션도 함께 적용한다.

---

## 요약 체크리스트

Opus 4.8을 채택·튜닝할 때 점검할 항목이다.

- [ ] 코딩·에이전트에 **`xhigh`**, 지능 민감 작업에 **최소 `high`** effort를 썼는가
- [ ] 얕은 추론을 프롬프트로 우회하지 않고 **effort 상향**으로 해결했는가
- [ ] `max`/`xhigh`에 **max output 64k+** 예산을 잡았는가
- [ ] thinking을 `{type: "adaptive"}`로만 켜고, 과다 발동 시 스티어링했는가
- [ ] 4.7 대비 **effort 재보정**(medium↑·high↓·xhigh↑↑)을 비용·지연에 반영했는가
- [ ] 지시를 넓게 적용해야 하면 **스코프를 명시**했는가(문자주의 대응)
- [ ] 강제 진행-요약 스캐폴딩을 **제거**해 봤는가
- [ ] 서브에이전트 팬아웃이 필요하면 **위임 기준을 명시**했는가
- [ ] 프론트엔드에서 하우스 스타일이 어색하면 **구체 스펙 또는 옵션 제안**으로 깼는가
- [ ] 코드 리뷰는 **coverage 목표 + 하류 필터** 구조로 짰는가
- [ ] Fable 5 거부 시 **Opus 4.8 폴백**을 설정했는가(자매 문서 참조)

---

## 참고 자료

- [Prompting Claude Opus 4.8 — Anthropic 공식 가이드](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8) (이 문서의 1차 출처)
- [What's new in Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) (모델 소개·API·가격)
- [Migrating to Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/migration-guide) (마이그레이션 체크리스트)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) · [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking) (파라미터 상세)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (모든 Claude 모델 공통 기법)
- [Claude Fable 5 프롬프팅 가이드](GUIDE-CLAUDE-FABLE-5-PROMPTING-2026-07-11-1710.md) (자매 문서 — 상위 모델·폴백 원천)

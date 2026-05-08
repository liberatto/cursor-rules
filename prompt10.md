# Claude 10대 프롬프트 가이드

> Claude의 내부 동작 원리(reasoning layer, constitutional backbone 등)를 활용하는 고급 프롬프트 패턴 10선.
> "Act as an expert" 같은 일반론이 아닌, **Claude 전용 구조**로 설계된 프롬프트들.

---

## 📌 핵심 철학 (먼저 읽기)

이 10개 프롬프트는 4가지 공통 원칙 위에 만들어져 있습니다.

| 원칙 | 의미 |
|---|---|
| **맥락 먼저, 요청 나중** | Claude는 상황 지도를 받아야 제대로 탐색한다 |
| **답이 아닌 사고 과정을 요구** | 추론 레이어가 표면에 드러나야 검증 가능하다 |
| **동의가 아닌 반박을 설계** | 도전하는 모델이 동의하는 모델보다 10배 가치 있다 |
| **가정을 항상 감사** | 모든 답변 아래에 숨은 뼈대를 드러내라 |

---

## 🗺️ 사용 흐름 (시간 순)

```
┌─ 질문 전 세팅 ────┐   ┌─ 답변 받는 중 ───┐   ┌─ 답변 후 검증 ────┐
│  1. Situation    │   │  2. Reasoning    │   │  8. Assumption    │
│  4. Role Spec    │ → │  3. Honest       │ → │  9. Compression   │
│  6. Scope Pin    │   │  5. Devil's Adv  │   │  10. Pre-Mortem   │
│  7. Format       │   │                   │   │                    │
└───────────────────┘   └───────────────────┘   └────────────────────┘
```

---

# 🔵 PART 1. 질문 전 세팅 (Setup)

> 질문을 던지기 전에 Claude에게 **지도**를 쥐여주는 단계. 이 단계에서 결과 품질의 70%가 결정됩니다.

---

## 1. The Situation Brief — 상황 브리프

**언제 쓰나:** 모든 중요한 대화의 첫 메시지. 요청만 덜렁 던지지 말고 상황부터 깔기.

```
Here's my context: [role, company, problem].
Here's what I've already tried: [X, Y].
Here's where I'm stuck: [Z].
Now help me think through this.
```

💡 **왜 중요한가:** Anthropic 내부 테스트에서 이 한 줄 변경으로 **유용한 출력이 41% 증가**. Claude는 탐색하기 전에 지도가 필요하다.

🎯 **KT 적용 예시:**
> "Here's my context: AXSP 팀 AI Agent 개발 리드, 사내 여러 팀의 거버넌스 갭 존재. Here's what I've already tried: 공통 프레임워크 제안, 기술 가이드 배포. Here's where I'm stuck: 팀별 자율성과 통합성의 균형. Now help me think through this."

---

## 4. The Role Specification — 역할 구체화

**언제 쓰나:** 전문가 페르소나를 부여할 때. "Act as an expert"는 **가장 약한 프롬프트**다.

```
You are a [specific role] with [specific experience]
who has seen [specific failure mode] before.
You think in [specific framework].
You are direct and skip conventional advice.
```

💡 **왜 중요한가:** 페르소나가 구체적일수록 추론이 구체적이다. **Vague persona = vague output. Every time.**

🎯 **KT 적용 예시:**
> "You are a staff engineer with 10 years building production ML systems, who has seen agent loops collapse under real traffic. You think in terms of observability, fallbacks, and cost ceilings. You are direct and skip conventional advice."

---

## 6. The Scope Pin — 범위 고정

**언제 쓰나:** 할루시네이션을 원천 차단하고 싶을 때. 특히 기술 문서/법률/데이터 질문.

```
Stay strictly within [X context].
If something falls outside this scope, tell me rather than speculating.
I'd rather have a gap than a confident wrong answer.
```

💡 **왜 중요한가:** Claude는 묻지 않은 인접 질문 3개까지 친절하게 답한다. 그 친절함이 그럴듯한 허구로 빈 칸을 채우는 원인이다. 이 프롬프트는 **할루시네이션을 소스에서 죽인다**.

---

## 7. The Format Command — 포맷 선언

**언제 쓰나:** Claude가 너무 장황할 때. 사실상 대부분의 실무 상황.

```
Structure your response as:
1) One sentence summary.
2) Three key points.
3) One recommended next action.
Nothing else unless I ask.
```

💡 **왜 중요한가:** Claude는 기본값이 **포괄성(comprehensiveness)**이지만 당신에게 필요한 건 보통 **간결성**이다. Claude는 다른 어떤 모델보다 포맷 지시를 정밀하게 따른다 — 그 정밀함을 의도적으로 활용하라.

---

# 🟣 PART 2. 답변 받는 중 (Thinking Quality)

> 답변의 품질과 정직성을 끌어올리는 단계. Claude가 당신이 듣고 싶은 말을 하지 못하게 막습니다.

---

## 2. The Reasoning Demand — 추론 요구

**언제 쓰나:** 결론만 필요한 게 아니라 **신뢰할 만한 결론**이 필요할 때.

```
Before you give me a solution, walk me through your reasoning step by step.
Show me where you're uncertain.
Flag any assumptions you're making.
```

💡 **왜 중요한가:** Claude의 **내부 reasoning 레이어를 표면으로 끌어올린다**. 받은 결과물이 단순한 '답'이 아니라 **심문 가능한 사고 과정**이 된다.

---

## 3. The Honest Constraint — 정직 제약

**언제 쓰나:** 자신의 계획/코드/판단에 피드백을 받을 때. 아부가 아닌 진실이 필요할 때.

```
I need you to be honest even if it's uncomfortable.
If my plan has a fatal flaw, say so directly.
Don't soften it.
I'd rather hear the hard truth now than fail later.
```

💡 **왜 중요한가:** Claude의 기본값은 "helpful"인데, 때로 helpful이 "듣고 싶은 말 해주기"로 변질된다. 이 프롬프트가 **Claude의 constitutional backbone(헌법적 중심)을 해제**시킨다.

---

## 5. The Devil's Advocate — 악마의 변호인

**언제 쓰나:** 아이디어/전략/아키텍처 결정을 확정하기 직전. 압력 테스트 단계.

```
I'm about to share my plan. Your job is to destroy it.
Find every assumption that could be wrong,
every risk I'm ignoring,
every reason this fails.
Don't hold back.
```

💡 **왜 중요한가:** Anthropic **내부 팀들이 아이디어를 압력 테스트할 때 쓰는 방식**이다. 당신에게 도전하는 모델이 동의하는 모델보다 10배 가치 있다.

🔗 **실전 팁:** 프롬프트 3(Honest)과 프롬프트 5(Devil's Advocate)를 연속으로 쓰면 가장 강력하다. 먼저 정직을 요구한 뒤, 파괴를 요구하라.

---

# 🟢 PART 3. 답변 후 검증 (Verification)

> 답변을 받은 뒤의 단계. 많은 사람이 여기서 멈추지만, 진짜 가치는 여기서 시작됩니다.

---

## 8. The Assumption Audit — 가정 감사

**언제 쓰나:** 복잡한 답변을 받은 직후. **모든 중요한 답변 뒤에 무조건** 실행.

```
What assumptions did you just make that I should verify?
What would change your answer if those assumptions were wrong?
```

💡 **왜 중요한가:** **가장 덜 사용되는 프롬프트**. 모든 응답 아래에 숨어있는 **scaffolding(뼈대)**을 드러낸다. 계획이 무너지는 지점은 언제나 이 뼈대에 있다.

---

## 9. The Compression Loop — 압축 루프

**언제 쓰나:** 긴 세션(5~6턴 이상) 중간에. 맥락 부채(context debt)가 쌓이기 시작할 때.

```
Summarize where we are.
What problem are we solving,
what have we decided,
and what's the single most important thing we haven't resolved yet?
```

💡 **왜 중요한가:** 긴 세션에서 Claude는 **맥락 부채를 축적**한다. 이 프롬프트가 세션을 핵심에 고정시키고, **Claude가 엉뚱한 문제를 자신만만하게 푸는 사태를 예방**한다.

---

## 10. The Pre-Mortem — 사전 부검

**언제 쓰나:** Claude와 함께 만든 것을 배포/실행하기 직전. 출시 전 마지막 관문.

```
Assume this fails 6 months from now.
Walk me through the 3 most likely reasons why.
Be specific.
What would the failure actually look like?
```

💡 **왜 중요한가:** **Anthropic 제품팀이 모든 주요 의사결정에 실행하는 프롬프트**다. 다른 어떤 리뷰 프로세스도 잡아내지 못하는 것을 잡아낸다.

🎯 **KT 적용 예시:** AI Agent 시스템 배포 전, 기술 의사결정 전, 팀 구조 변경 전 — 모두 여기에 해당.

---

# 🎯 실전 콤보 (Prompt Chaining)

## 콤보 A: 새로운 주제 깊이 파고들기
```
Prompt 1 (Situation) → Prompt 4 (Role) → Prompt 2 (Reasoning) → Prompt 8 (Assumption Audit)
```
**시나리오:** 생소한 기술 스택 검토, 새 프로젝트 킥오프 전 리서치.

## 콤보 B: 계획/설계 압력 테스트
```
Prompt 1 (Situation) → Prompt 3 (Honest) → Prompt 5 (Devil's Advocate) → Prompt 10 (Pre-Mortem)
```
**시나리오:** 아키텍처 결정, 전략 문서, 중요한 의사결정 전.

## 콤보 C: 빠른 의사결정 모드
```
Prompt 7 (Format) + Prompt 6 (Scope) → Prompt 8 (Assumption Audit)
```
**시나리오:** 시간 없을 때, 간결한 답 + 할루시네이션 방지 + 최소 검증.

## 콤보 D: 장시간 세션 관리
```
5~6턴마다 Prompt 9 (Compression Loop) 자동 실행
↓
마지막에 Prompt 10 (Pre-Mortem)
```
**시나리오:** 복잡한 설계/디버깅 세션, 하루 종일 이어지는 작업.

---

# 📋 치트시트 (빠른 참조)

| # | 이름 | 타이밍 | 한 줄 요약 |
|---|---|---|---|
| 1 | Situation Brief | 시작 | 요청 전에 맥락·시도·막힌 곳 3종 세트 |
| 2 | Reasoning Demand | 중간 | 답 말고 사고 과정을 달라 |
| 3 | Honest Constraint | 중간 | 불편해도 진실을 말해라 |
| 4 | Role Specification | 시작 | 역할/경험/실패경험/프레임워크까지 구체적으로 |
| 5 | Devil's Advocate | 중간 | "네 임무는 내 계획을 파괴하는 것" |
| 6 | Scope Pin | 시작 | 범위 밖은 추측 말고 '모름'이라 말해라 |
| 7 | Format Command | 시작 | 요약 1문장 + 핵심 3가지 + 다음 액션 1개 |
| 8 | Assumption Audit | 후 | 방금 만든 가정 중 내가 검증할 것은? |
| 9 | Compression Loop | 중간 | 5~6턴마다 "지금 우리 어디 있나?" |
| 10 | Pre-Mortem | 후 | "6개월 뒤 실패했다고 가정하고 이유 3개" |

---

# 🧭 핵심 메타 원칙

> **Claude는 maps가 필요하다. 지시가 아니라.**
> **Claude에게는 정직을 허가해야 한다. 기본값이 아니다.**
> **Claude의 답변 아래엔 항상 뼈대(scaffolding)가 있다. 그 뼈대를 꺼내는 것이 진짜 사용법이다.**

---

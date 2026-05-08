# 10가지 프롬프트 기법 레퍼런스

> Claude의 reasoning layer와 constitutional backbone을 활용하는 고급 기법 10선.

---

## Phase 1: 질문 전 세팅 (Setup)

### 1. Situation Brief — 상황 브리프

**타이밍**: 모든 중요한 대화의 첫 메시지

**구조**:
```
Here's my context: [역할, 조직, 문제].
Here's what I've already tried: [시도한 것들].
Here's where I'm stuck: [막힌 지점].
Now help me think through this.
```

**원리**: Anthropic 내부 테스트에서 이 구조로 유용한 출력이 41% 증가. Claude는 탐색 전에 지도가 필요하다.

**적용 예시**:
> "Here's my context: AXSP 팀 AI Agent 개발 리드, 사내 여러 팀의 거버넌스 갭 존재. Here's what I've already tried: 공통 프레임워크 제안, 기술 가이드 배포. Here's where I'm stuck: 팀별 자율성과 통합성의 균형. Now help me think through this."

---

### 4. Role Specification — 역할 구체화

**타이밍**: 전문가 페르소나를 부여할 때

**구조**:
```
You are a [specific role] with [specific experience]
who has seen [specific failure mode] before.
You think in [specific framework].
You are direct and skip conventional advice.
```

**원리**: 페르소나가 구체적일수록 추론이 구체적이다. Vague persona = vague output.

**적용 예시**:
> "You are a staff engineer with 10 years building production ML systems, who has seen agent loops collapse under real traffic. You think in terms of observability, fallbacks, and cost ceilings. You are direct and skip conventional advice."

---

### 6. Scope Pin — 범위 고정

**타이밍**: 할루시네이션을 원천 차단하고 싶을 때. 기술 문서/법률/데이터 질문.

**구조**:
```
Stay strictly within [X context].
If something falls outside this scope, tell me rather than speculating.
I'd rather have a gap than a confident wrong answer.
```

**원리**: Claude는 묻지 않은 인접 질문까지 친절하게 답하는데, 그 친절함이 할루시네이션의 원인이다. 이 기법은 할루시네이션을 소스에서 죽인다.

---

### 7. Format Command — 포맷 선언

**타이밍**: Claude가 너무 장황할 때. 대부분의 실무 상황.

**구조**:
```
Structure your response as:
1) One sentence summary.
2) Three key points.
3) One recommended next action.
Nothing else unless I ask.
```

**원리**: Claude의 기본값은 포괄성(comprehensiveness)이지만 실무에서 필요한 건 간결성이다. Claude는 다른 모델보다 포맷 지시를 정밀하게 따른다.

---

## Phase 2: 답변 받는 중 (Thinking Quality)

### 2. Reasoning Demand — 추론 요구

**타이밍**: 신뢰할 만한 결론이 필요할 때

**구조**:
```
Before you give me a solution, walk me through your reasoning step by step.
Show me where you're uncertain.
Flag any assumptions you're making.
```

**원리**: Claude의 내부 reasoning 레이어를 표면으로 끌어올린다. 결과물이 단순한 '답'이 아니라 심문 가능한 사고 과정이 된다.

---

### 3. Honest Constraint — 정직 제약

**타이밍**: 자신의 계획/코드/판단에 진짜 피드백이 필요할 때

**구조**:
```
I need you to be honest even if it's uncomfortable.
If my plan has a fatal flaw, say so directly.
Don't soften it.
I'd rather hear the hard truth now than fail later.
```

**원리**: Claude의 기본값은 "helpful"인데, 때로 "듣고 싶은 말 해주기"로 변질된다. 이 기법이 Claude의 constitutional backbone을 해제시킨다.

---

### 5. Devil's Advocate — 악마의 변호인

**타이밍**: 아이디어/전략/아키텍처를 확정하기 직전. 압력 테스트.

**구조**:
```
I'm about to share my plan. Your job is to destroy it.
Find every assumption that could be wrong,
every risk I'm ignoring,
every reason this fails.
Don't hold back.
```

**원리**: Anthropic 내부 팀들이 아이디어를 압력 테스트할 때 쓰는 방식. 도전하는 모델이 동의하는 모델보다 10배 가치 있다.

**실전 팁**: Honest Constraint(3) + Devil's Advocate(5) 연속 사용이 가장 강력. 먼저 정직을 요구한 뒤, 파괴를 요구하라.

---

## Phase 3: 답변 후 검증 (Verification)

### 8. Assumption Audit — 가정 감사

**타이밍**: 복잡한 답변을 받은 직후. 모든 중요한 답변 뒤에 무조건 실행.

**구조**:
```
What assumptions did you just make that I should verify?
What would change your answer if those assumptions were wrong?
```

**원리**: 가장 덜 사용되지만 가장 강력한 기법. 모든 응답 아래에 숨어있는 scaffolding(뼈대)을 드러낸다. 계획이 무너지는 지점은 언제나 이 뼈대에 있다.

---

### 9. Compression Loop — 압축 루프

**타이밍**: 긴 세션(5~6턴 이상) 중간. 맥락 부채가 쌓이기 시작할 때.

**구조**:
```
Summarize where we are.
What problem are we solving,
what have we decided,
and what's the single most important thing we haven't resolved yet?
```

**원리**: 긴 세션에서 Claude는 맥락 부채를 축적한다. 이 기법이 세션을 핵심에 고정시키고, Claude가 엉뚱한 문제를 자신만만하게 푸는 사태를 예방한다.

---

### 10. Pre-Mortem — 사전 부검

**타이밍**: Claude와 함께 만든 것을 배포/실행하기 직전. 출시 전 마지막 관문.

**구조**:
```
Assume this fails 6 months from now.
Walk me through the 3 most likely reasons why.
Be specific.
What would the failure actually look like?
```

**원리**: Anthropic 제품팀이 모든 주요 의사결정에 실행하는 기법. 다른 어떤 리뷰 프로세스도 잡아내지 못하는 것을 잡아낸다.

**적용 예시**: AI Agent 시스템 배포 전, 기술 의사결정 전, 팀 구조 변경 전.

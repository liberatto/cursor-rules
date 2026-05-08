# Combo Patterns — 기법 조합 가이드

> 단일 기법보다 강력한 조합 패턴. 상황에 맞는 콤보를 선택하면 프롬프트 품질이 비약적으로 향상된다.

---

## 정의된 콤보 4종

### Combo A: Deep Dive — 새로운 주제 깊이 파고들기

```
1 (Situation) → 4 (Role) → 2 (Reasoning) → 8 (Assumption Audit)
```

**시나리오**: 생소한 기술 스택 검토, 새 프로젝트 킥오프 전 리서치

**흐름**:
1. 상황 브리프로 맥락과 막힌 지점 전달
2. 도메인 전문가 역할 부여
3. 사고 과정을 드러내며 분석
4. 숨은 가정 감사로 마무리

**통합 프롬프트 예시**:
```
Here's my context: [상황]. Here's what I've tried: [시도]. Here's where I'm stuck: [막힌 곳].

You are a [구체적 역할] with [구체적 경험] who has seen [구체적 실패] before. You think in [프레임워크]. You are direct and skip conventional advice.

Before giving solutions, walk me through your reasoning step by step. Show me where you're uncertain. Flag any assumptions you're making.

After your analysis, tell me: what assumptions did you just make that I should verify? What would change your answer if those were wrong?
```

---

### Combo B: Pressure Test — 계획/설계 압력 테스트

```
1 (Situation) → 3 (Honest) → 5 (Devil's Advocate) → 10 (Pre-Mortem)
```

**시나리오**: 아키텍처 결정, 전략 문서, 중요한 의사결정 전

**흐름**:
1. 현재 상황과 계획 공유
2. 정직 모드 활성화 — 아부 금지
3. 계획 파괴 요청 — 모든 약점 노출
4. 사전 부검 — 실패 시나리오 구체화

**통합 프롬프트 예시**:
```
Here's my context: [상황]. Here's my plan: [계획 요약].

I need you to be honest even if it's uncomfortable. If my plan has a fatal flaw, say so directly. Don't soften it. I'd rather hear the hard truth now than fail later.

Your job is to destroy this plan. Find every assumption that could be wrong, every risk I'm ignoring, every reason this fails. Don't hold back.

Then assume this fails 6 months from now. Walk me through the 3 most likely reasons why. Be specific. What would the failure actually look like?
```

---

### Combo C: Quick Decision — 빠른 의사결정 모드

```
7 (Format) + 6 (Scope) → 8 (Assumption Audit)
```

**시나리오**: 시간 없을 때. 간결한 답 + 할루시네이션 방지 + 최소 검증.

**흐름**:
1. 포맷과 범위를 먼저 고정
2. 가정 감사로 최소한의 검증

**통합 프롬프트 예시**:
```
Stay strictly within [X context]. If something falls outside this scope, tell me rather than speculating. I'd rather have a gap than a confident wrong answer.

Structure your response as:
1) One sentence summary.
2) Three key points.
3) One recommended next action.
Nothing else unless I ask.

At the end, list any assumptions you made that I should verify.
```

---

### Combo D: Marathon Session — 장시간 세션 관리

```
5~6턴마다 9 (Compression Loop) 자동 실행
→ 마지막에 10 (Pre-Mortem)
```

**시나리오**: 복잡한 설계/디버깅 세션, 하루 종일 이어지는 작업

**중간 체크포인트 프롬프트**:
```
Summarize where we are. What problem are we solving, what have we decided, and what's the single most important thing we haven't resolved yet?
```

**마무리 프롬프트**:
```
Assume everything we built today fails 6 months from now. Walk me through the 3 most likely reasons why. Be specific. What would the failure actually look like?
```

---

## 커스텀 콤보 조합 가이드

정의된 4가지 외에도 상황에 맞게 기법을 자유롭게 조합할 수 있다. 조합 시 지켜야 할 원칙:

### 순서 원칙

```
Setup (1, 4, 6, 7) → Thinking (2, 3, 5) → Verification (8, 9, 10)
```

Phase 순서를 지킨다. Verification 기법을 Setup 앞에 놓지 않는다.

### 조합 시너지

| 조합 | 시너지 효과 |
|------|------------|
| 3 (Honest) + 5 (Devil's) | 정직을 먼저 허가 → 파괴가 더 날카로워짐 |
| 1 (Situation) + 4 (Role) | 지도 + 나침반 = 최적 탐색 |
| 6 (Scope) + 7 (Format) | 범위 제한 + 형식 제한 = 간결하고 정확한 답 |
| 2 (Reasoning) + 8 (Assumption) | 사고 과정 노출 + 뼈대 감사 = 완전한 투명성 |
| 5 (Devil's) + 10 (Pre-Mortem) | 현재 약점 + 미래 실패 = 360도 검증 |

### 피해야 할 조합

| 조합 | 이유 |
|------|------|
| 9 (Compression) + 1 (Situation) | 압축은 진행 중 세션용, Situation은 새 대화 시작용. 목적 충돌 |
| 7 (Format) + 2 (Reasoning) | 간결한 포맷을 강제하면서 사고 과정을 요구하면 모순 |

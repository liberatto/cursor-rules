# Decision Matrix — 상황 → 기법 매핑

> 사용자의 상황 신호를 읽고 최적 기법을 선택하는 판단 기준.

---

## 빠른 매핑 테이블

| 상황 신호 | 1차 추천 | 보조 추천 | Phase |
|-----------|----------|-----------|-------|
| 새 주제 시작, 맥락 공유 필요 | 1. Situation Brief | 4. Role Spec | Setup |
| "전문가 관점이 필요해" | 4. Role Specification | 1. Situation Brief | Setup |
| 사실 기반 답변 필요, 할루시네이션 방지 | 6. Scope Pin | 7. Format Command | Setup |
| "너무 장황해", 간결한 답 필요 | 7. Format Command | 6. Scope Pin | Setup |
| "왜 그렇게 생각해?", 추론 과정 필요 | 2. Reasoning Demand | 8. Assumption Audit | Thinking |
| "솔직하게 말해줘", 진짜 피드백 필요 | 3. Honest Constraint | 5. Devil's Advocate | Thinking |
| 계획/설계 검증, 압력 테스트 | 5. Devil's Advocate | 3. Honest + 10. Pre-Mortem | Thinking |
| 복잡한 답변 받은 직후 | 8. Assumption Audit | 2. Reasoning Demand | Verification |
| 긴 대화 중간, 방향 잃는 느낌 | 9. Compression Loop | — | Verification |
| 배포/실행 직전, 최종 점검 | 10. Pre-Mortem | 8. Assumption Audit | Verification |

---

## 상세 판단 기준

### Phase 판별 — 사용자가 어느 단계에 있는가?

```
사용자가 아직 질문을 구성하는 중인가?  → Setup (1, 4, 6, 7)
사용자가 답변을 받는 중이거나 품질을 높이고 싶은가?  → Thinking (2, 3, 5)
사용자가 이미 답변을 받았고 검증하려는가?  → Verification (8, 9, 10)
```

### 목적별 판별 — 무엇을 달성하려 하는가?

| 목적 | 기법 |
|------|------|
| 맥락을 제대로 전달하고 싶다 | 1. Situation Brief |
| 특정 분야 전문성이 필요하다 | 4. Role Specification |
| 정확한 정보만 원한다 (추측 금지) | 6. Scope Pin |
| 짧고 구조화된 답이 필요하다 | 7. Format Command |
| 결론의 근거를 보고 싶다 | 2. Reasoning Demand |
| 아부 말고 진짜 피드백이 필요하다 | 3. Honest Constraint |
| 내 아이디어의 약점을 찾고 싶다 | 5. Devil's Advocate |
| 답변의 숨은 가정을 확인하고 싶다 | 8. Assumption Audit |
| 대화가 산으로 가는 걸 방지하고 싶다 | 9. Compression Loop |
| 실행 전 실패 시나리오를 점검하고 싶다 | 10. Pre-Mortem |

---

## 모호성 해소 가이드

### 되묻기가 필요한 상황

1. **Phase 혼합**: Setup 기법과 Verification 기법이 동시에 후보
   → "지금 질문을 구성하는 단계인가요, 이미 받은 답을 검증하는 단계인가요?"

2. **상황 정보 부족**: 설명이 50자 미만
   → "조금 더 알려주세요: 어떤 작업을 하고 있고, 어디서 막혔나요?"

3. **기법 2개가 동등하게 유력**: 예) Honest Constraint vs Devil's Advocate
   → "솔직한 피드백이 필요한 건가요(정직 제약), 아니면 계획을 적극적으로 공격해달라는 건가요(악마의 변호인)?"

### 되묻지 않아도 되는 상황

- Phase가 명확하고 후보가 1개일 때
- 사용자가 기법명을 직접 언급했을 때
- 콤보 패턴(A~D)에 정확히 매칭될 때

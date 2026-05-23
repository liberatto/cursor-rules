# NOTE — Ralph-Loop 런타임 흐름

`/ssp:work-ralph-init`로 생성된 산출물(`PROMPT.md` + `progress.md`)이 `/ssp:work-ralph` 루프에서 어떻게 동작하는지 핵심만 도식화.

## 전체 흐름 도식

```
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 0 — Init (1회, 사용자 검토)                                     │
│  /ssp:work-ralph-init "<task>"                                      │
│         │                                                           │
│         ├── Phase 1 추론 (pyproject.toml/CLAUDE.md/...)              │
│         ├── Phase 2 [필요 시] AskUserQuestion ×1                     │
│         ├── Phase 3 PROMPT.md 생성                                   │
│         └── Phase 4 PROMPT.md + progress.md 부트스트랩                 │
│                                                                     │
│  ┌──────────────┐         ┌──────────────────────────────┐          │
│  │  PROMPT.md   │  ←불변  │  progress.md (State=active)  │           │
│  │  Mission     │         │  Iteration: 0 / 10           │          │
│  │  Done When   │         │  Items: [ ] [ ] [ ] ...      │          │
│  │  Never       │         │  Next: <첫 액션>             │            │
│  └──────────────┘         └──────────────────────────────┘          │
│         ↑ 사용자 검토 게이트 (이 문서 통과해야 루프 진입)           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
            git switch -c ralph/<slug>   (권장)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 1 — Loop 진입                                                 │
│  /ssp:work-ralph @PROMPT.md                                         │
│         │                                                           │
│         ▼                                                           │
│  /ralph-loop:ralph-loop @PROMPT.md --max-iterations 10              │
│                          --completion-promise "DONE"                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ╔══════════════════════════════════════════════════════╗
        ║  STAGE 2 — Iteration N (1 ≤ N ≤ max)                 ║
        ║                                                      ║
        ║   ① Read PROMPT.md (불변)                            ║
        ║   ② Read progress.md ## Status + ## Items            ║
        ║         │                                            ║
        ║         ▼                                            ║
        ║   ③ Pick next [ ] item   OR   next gate violation    ║
        ║         │                                            ║
        ║         ▼                                            ║
        ║   ④ Implement + write/update tests                   ║
        ║         │                                            ║
        ║         ▼                                            ║
        ║   ⑤ Run gates (fast → slow):                         ║
        ║         ruff → mypy → pytest                         ║
        ║         │                                            ║
        ║    ┌────┴────┐                                       ║
        ║   PASS      FAIL                                     ║
        ║    │         │                                       ║
        ║    │         └─→ ⑥a Notes에 5줄 요약 + 가설/계획         ║
        ║    │              │                                  ║
        ║    │              ▼                                  ║
        ║    │         같은 실패 3회 연속?                         ║
        ║    │              │                                  ║
        ║    │       ┌──────┴──────┐                           ║
        ║    │      No            Yes ──→ ⑥b BLOCKED 섹션      ║
        ║    │       │                       작성 후 DONE 출력   ║
        ║    │       │                       (운영자 검토)        ║
        ║    │       │                                         ║
        ║    ▼       ▼                                         ║
        ║   ⑦ Update progress.md ## Status:                    ║
        ║         Iteration: N / max                           ║
        ║         Last update: <now>                           ║
        ║         Last change: <한 줄 요약>                      ║
        ║         Next: <다음 액션>                              ║
        ║       Items: [x] flip if completed                   ║
        ║         │                                            ║
        ║         ▼                                            ║
        ║   ⑧ 종료 조건 검사:                                     ║
        ║       모든 게이트 PASS                                  ║
        ║       AND 모든 [x] (멀티스텝)                            ║
        ╚══════════════════════════════════════════════════════╝
                              │
              ┌───────────────┼────────────────┐
            아니오           예               BLOCKED
              │               │                 │
              ▼               ▼                 ▼
        N < max 인가?    State=complete    Notes에 보고서
              │           <promise>            │
        ┌─────┴────┐       DONE         <promise>DONE</promise>
       Yes        No        │                  │
        │         │         │                  │
        │         ▼         ▼                  ▼
        │   summary 출력   루프 정상 종료  루프 정상 종료
        │   (no DONE)         │                │
        │                     ▼                ▼
        └──→ STAGE 2 다시       사용자 검토 (PR / 다음 액션 결정)
             (다음 iteration)
```

## progress.md `## Status`의 시간 진화 예시

```
  Iter 0 (init)              Iter 3 (진행 중)            Iter 7 (DONE)
  ─────────────              ──────────────              ──────────────
  State: active              State: active               State: complete
  Iter: 0 / 10               Iter: 3 / 10                Iter: 7 / 10
  Last upd: 21:40            Last upd: 22:05             Last upd: 22:38
  Last change: (none)        Last change: JWT 만료       Last change: refresh
                             검증 로직 추가, test_       토큰 갱신 통과
                             expired_basic 통과
  Next: test_expired_basic   Next: test_expired_         Next: (DONE)
                             with_grace 분석
```

## 종료 경로 3가지 정리

| 경로 | 트리거 | progress.md 상태 | promise |
| --- | --- | --- | --- |
| **정상 완료** | 모든 게이트 PASS + 모든 `[x]` | `State: complete` | `DONE` 출력 |
| **자가 차단(BLOCKED)** | 동일 실패 3회 연속 | `## BLOCKED` 보고서 작성, `State: blocked`로 변경 권장 | `DONE` 출력 (DONE만 인식하므로 안전 종료) |
| **예산 소진** | iteration N == max | `State: active` 유지, summary는 stdout | promise 없음 (루프 자연 종료) |

## 핵심 설계 포인트 (이 도식이 보여주는 것)

1. **불변/가변 분리** — PROMPT.md(미션 헌법, 변경 금지)와 progress.md(누적 메모리, 매 이터 갱신) 명확 분리
2. **단일 가시 화면** — 운영자가 progress.md 하나만 열면 *지금·방금·다음*을 즉시 파악
3. **3개 종료 경로 모두 안전** — DONE으로 깨끗히 끝나거나(완료/BLOCKED) 명시적 미완료(예산 소진). 폭주 없음
4. **검토 게이트 2중** — Init 후 사용자 검토 1회 + 루프 종료 후 progress.md 검토 1회

---

**관련 파일**
- `.claude/commands/ssp/work-ralph-init.md` (PROMPT.md/progress.md 생성)
- `.claude/commands/ssp/work-ralph.md` (루프 실행)
- memory: `feedback_ralph_loop_init_exec_split.md`

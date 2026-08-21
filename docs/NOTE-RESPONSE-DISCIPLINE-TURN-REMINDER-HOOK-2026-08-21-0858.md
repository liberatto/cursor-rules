---
type: note
audience: 사용자·Claude
related_docs:
  - ClaudeCode/CLAUDE.v.5.7.md (대상 — §Response Discipline 215~227줄)
  - docs/GUIDE-CLAUDE-CODE-OUTPUT-STYLES-2026-02-22-2026.md (선행 정리 — 내장 스타일 3종 시점이라 현행과 어긋난다)
  - docs/GUIDE-CLAUDE-CODE-HOOKS-2026-02-22-1500.md (훅 이벤트·설정 형식)
  - CLAUDE.local.md (2026-08-21 항목 — 이 메모의 발단이 된 실행 실패 사례)
created: 2026-08-21 08:58
updated: 2026-08-21
measured: 2026-08-21
status: active
description: "지금은 훅을 적용하지 않는다 — 지침이 대체로 지켜지고 있어 근거가 얇다. 다만 Response Discipline 은 대화 첫 턴에 한 번만 주입되고 이후 재주입되지 않으므로, 긴 세션 후반의 감쇠는 구조적으로 가능하다. 감쇠성 실패가 반복되면 UserPromptSubmit 훅으로 일곱 조항의 라벨만 매 턴 재주입한다. 문구는 손으로 적지 않고 지침 파일에서 생성한다."
open_issues:
  - 감쇠성 실패의 표본이 1건뿐이라 훅의 실효를 판정할 수 없다 — 같은 유형이 2건 더 쌓이면 적용을 재검토한다
---

# NOTE: Response Discipline 감쇠 대비 훅 옵션

## 결론

훅을 적용하지 않는다. 사용자 판단이며 근거는 하나다 — 훅 없이도 지침이 대체로 지켜지고 있고, 감쇠로 분류할 수 있는 실패가 아직 1건뿐이다.

아래는 그때 다시 꺼내 쓰기 위한 기록이다.

## 배경 — 감쇠는 구조적으로 가능하다

`CLAUDE.md` 는 대화의 **첫 유저 턴에 `<system-reminder>` 로 한 번 붙고, 그 뒤로 재주입되지 않는다.** Claude Code 바이너리 `2.1.238` 에서 주입 함수(`NTf`)가 메시지 배열 앞에 리마인더 메시지 한 개를 얹는 구조임을 확인했다. 매 턴 다시 넣는 경로는 출력 스타일의 `turnReminder` 하나뿐이다.

```
  대화 시작                                          현재 턴
     │                                                  │
     ▼                                                  ▼
  ┌──────────────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │ CLAUDE.md    │ turn │ turn │ turn │ turn │ turn │ turn │
  │ (1회, 고정)  │  1   │  2   │  3   │ ...  │ n-1  │  n   │
  └──────────────┴──────┴──────┴──────┴──────┴──────┴──────┘
     ◀──────────── 턴이 쌓일수록 멀어진다 ────────────▶

  출력 스타일이 켜져 있으면:
  ┌──────────────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │ 스타일 프롬프트│ turn │ turn │ turn │ turn │ turn │ turn │
  └──────────────┴──┬───┴──┬───┴──┬───┴──┬───┴──┬───┴──┬───┘
                    ▼      ▼      ▼      ▼      ▼      ▼
                  turnReminder 한 줄이 매 턴 재주입된다
```

지침이 사라지는 것이 아니라 맨 앞에 고정된 채 멀어진다. 감쇠는 배치의 결과이지 느낌이 아니다.

실제 사례도 하나 있다. `CLAUDE.local.md` 2026-08-21 항목의 attack 산출물 ②가 그것이다 — 어떤 답변의 `eos-scope → … → eos-report` 화살표 체인은 222줄·224줄이 이미 금지하고 있었으므로 **규칙 공백이 아니라 실행 실패**로 분류했고, "지침을 늘려 고칠 자리가 아니다"로 닫았다. 훅은 지침을 늘리지 않으면서 기존 규칙의 발동률만 올리는 수단이라 정확히 그 자리에 들어맞는다.

## 내장 turnReminder 의 동작

내장 출력 스타일은 `2.1.238` 기준 4종이다 — `Proactive`·`Concise`·`Explanatory`·`Learning`. 각 스타일 정의는 세 부분으로 되어 있다.

| 부분 | 내용 |
| --- | --- |
| 기본 문장 교체 | 시스템 프롬프트의 `You are an interactive agent…` 자리에 스타일 고유 문장이 들어간다. `keepCodingInstructions: true` 라 도구·코딩 지시는 남는다 |
| 본문 삽입 | `# <이름> Style Active` 절과 조항 본문이 붙는다. `Concise` 는 6개 조항이다 |
| `turnReminder` | 한 문장이 매 턴 `isMeta` 리마인더로 재주입된다. 렌더 형식은 `"<이름> output style is active. <문구>"` 이다 |

`Concise` 의 리마인더 원문은 다음 한 줄이다.

```
Be concise: lead with the result, skip preamble and narration, keep only what the user needs.
```

### 커스텀 출력 스타일로는 만들 수 없다

`~/.claude/output-styles/*.md` 로 자기 스타일을 정의하는 길이 있으나, **거기에는 `turnReminder` 를 실을 수 없다.** 코드에서 확인한 근거는 둘이다.

- 파일 로더가 만드는 객체는 `{name, description, prompt, source, keepCodingInstructions, forceForPlugin}` 여섯 필드뿐이고 `turnReminder` 를 파싱하지 않는다.
- 리마인더를 그리는 쪽은 `let t = Oke[e.style]; if (!t) return []` 인데, `Oke` 는 내장 4종만 담은 맵이다. 커스텀 스타일 이름은 여기서 잡히지 않으므로 리마인더가 아예 주입되지 않는다.

즉 커스텀 스타일은 세션 시작 시 프롬프트가 한 번 들어갈 뿐이고, 매 턴 보강은 받지 못한다. `criticalSystemReminder_EXPERIMENTAL` 이라는 매 턴 주입 필드가 하나 더 있으나 에이전트 정의 스키마의 실험적 옵션이라 `settings.json` 에서는 쓸 수 없다.

## 적용한다면 — 설계안

### 무엇을 넣는가

조항 전문이 아니라 **일곱 조항의 라벨만** 넣는다. 라벨은 조항 본문을 불러오는 색인이고, 길이는 225자에 그친다.

```
Response Discipline: Label epistemic status · Lead with the outcome ·
One argument, end to end · Structure only when the content already has
a shape · Emojis with intent · Concise by selection, not compression ·
Korean
```

### 어떻게 생성하는가

문구를 훅 스크립트에 적지 않고 지침 파일에서 뽑는다. 아래 명령의 출력이 위 문구다.

```bash
awk '/^## Response Discipline$/,/^The test:/' ~/.claude/CLAUDE.md \
  | sed -n 's/^- \*\*\([^*]*\)\*\*.*/\1/p' \
  | awk '{a=a (a?" · ":"") $0} END{print "Response Discipline: " a}'
```

지침의 조항이 바뀌면 훅 출력도 따라 바뀌므로 손댈 곳이 없다. 이는 백로그의 `doc-writer §7.3` 항목과 같은 교훈이다 — 패턴을 손으로 옮겨 적으면 원본과 어긋나 같은 구멍이 재현된다.

### 어디에 등록하는가

`~/.claude/settings.json` 또는 프로젝트 `.claude/settings.local.json` 의 `UserPromptSubmit` 훅으로 등록한다. 훅의 stdout 이 그대로 그 턴의 모델 컨텍스트로 들어간다. 더 명시적으로 하려면 훅이 JSON 을 출력해 `hookSpecificOutput.additionalContext` 에 문구를 담는다.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "bash ~/.claude/hooks/response-discipline.sh" } ] }
    ]
  }
}
```

동작 확인은 별도로 필요 없다. `remember` 플러그인이 이미 같은 이벤트로 시각 스탬프를 매 턴 주입하고 있어 경로가 살아 있음이 증명된다.

## 기각 근거와 위험

적용하지 않기로 한 직접 사유는 실효 미검증이다. 감쇠가 원인인 실패는 위 화살표 체인 1건만 문서화돼 있어, 훅이 재발을 줄이는지는 켜 봐야 알 수 있다.

구조적 위험은 따로 있다. 훅 문구는 **두 번째 지시 채널**이 된다 — `settings.json` 에 살아 `claude-md-audit` 의 편입 게이트를 통과하지 않고, `CLAUDE.v.*.md` 버전 시리즈에도 남지 않는다. 위의 생성 방식은 이 위험을 없애는 것이 아니라 문구의 출처를 지침 파일로 되돌려 놓을 뿐이다. **훅이 지침에 없는 문장을 말하기 시작하면 그 선이 깨진다.**

비용은 턴당 50토큰 안팎으로 작다. 다만 전문을 붙이는 방식은 비용이 몇 배가 되면서 반복 자체가 둔감해지므로 택하지 않는다.

## 재검토 조건

규칙이 있는데도 지켜지지 않은 실패가 **긴 세션 후반에 2건 더** 나오면 적용을 재검토한다. 세는 대상은 규칙 공백이 아니라 실행 실패로 분류된 건이다 — 공백은 지침 개정으로 가고, 실행 실패만 훅의 관할이다.

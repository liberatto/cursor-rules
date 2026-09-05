---
name: copilot-task
description: |
  프로젝트 작업 중 한정된 job 한 건을 GitHub Copilot CLI에 위임하고 결과만 받아오는 범용 래퍼 스킬. 테스트·빌드 실행, 로그·에러 확인, 반복적 기계 수정,
  범위가 좁은 조사처럼 Claude 컨텍스트를 태울 이유가 없는 작업을 비대화 모드(`copilot -p`)로 넘긴다. 작업 성격에 맞는 권한 등급(조사·실행·편집)을 골라
  플래그로 강제하고, 프리픽스 크기와 캐시 적중으로 정해지는 비용을 관리하며, 위임 결과를 원문 보존한 채 실제 변경분과 대조해 보고한다.
  트리거: "코파일럿한테 시켜", "copilot으로 돌려줘", "코파일럿으로 테스트 돌려", "이거 copilot한테 맡겨", "copilot에게 위임", "코파일럿 시켜서 확인해줘",
  "다른 에이전트한테 돌려", "copilot CLI로 실행". 파일을 바꾸는 등급은 사용자 승인 후에만 실행한다. 다른 모델 계보로 산출물을 검증받는 작업은
  codex-review 담당이며, 이 스킬은 검증이 아닌 일반 작업 위임만 한다. Claude가 직접 하는 편이 빠른 단발 질의나 조직 맥락·보고 문체가 필요한 산출물에는
  트리거하지 않는다.
version: 1.0.0
---

# copilot-task — Copilot CLI 작업 위임

Claude가 직접 하지 않아도 되는 작업 한 건을 GitHub Copilot CLI에 넘기고 결과만 받는다. 위임의 목적은 두 가지다 — **Claude 컨텍스트를 태우지 않는 것**, 그리고 필요할 때 **다른 엔진의 시각을 얻는 것**.

**위임하지 않는 것**: 조직 맥락·보고 문체가 필요한 산출물(→ `doc-writer`·`report-style`), 산출물 교차 검증(→ `codex-review`), 되돌리기 어려운 작업(배포·외부 전송·git push).

## 1. 실행 전 확인

- `copilot` 명령이 없으면 **중단하고 사용자에게 알린다** — 설치를 임의로 진행하지 않는다.
- 인증은 별도로 하지 않는다. 기존 로그인을 그대로 쓴다. 의심되면 `copilot -p "Reply with exactly: OK" -s` 한 번으로 확인한다.
- **작업 디렉터리를 먼저 정한다.** `-C <dir>` 로 명시한다. 이 값이 비용과 컨텍스트를 동시에 정한다(§4).

## 2. 권한 등급 — 반드시 하나를 고른다

| 등급 | 용도 | 플래그 | 승인 |
| --- | --- | --- | --- |
| **L1 조사** | 코드·로그 읽기, 검색, 상태 확인 | `--allow-tool 'shell(rg:*)' --allow-tool 'shell(cat)' --allow-tool 'shell(ls)' --allow-tool 'shell(git:*)' --deny-tool write` | 불필요 |
| **L2 실행** | 테스트·빌드·스크립트 실행 | L1 + 필요한 실행기만 (`--allow-tool 'shell(pytest:*)'` 등) `--deny-tool write` 유지 | 불필요 |
| **L3 편집** | 파일 수정까지 맡김 | `--allow-all-tools` (또는 `--yolo`) | **사용자 승인 후에만** |

**등급 규칙.**

- `--deny-tool` 이 `--allow-all-tools` 보다 **항상 우선**한다. L3에서도 지키고 싶은 경계는 deny로 박는다.
- **`--no-ask-user` 를 반드시 붙인다.** 비대화 모드에서 미승인 도구 호출은 질문 대신 실패로 처리되고 세션은 정상 종료된다(실측: `Permission denied and could not request permission from user` 출력 후 exit 0, 파일 미생성). 없으면 승인 대기로 멈출 수 있다.
- **allowlist는 명령 stem 단위로 매칭된다.** `shell(cat)` 을 허용해도 `echo BAD > f && cat f` 는 거부된다(실측). 우회를 걱정해 등급을 올릴 필요가 없다.
- `write(path?)` 는 **shell 리다이렉션을 막지 못한다** — 파일 생성을 확실히 막으려면 deny(write)와 shell allowlist를 함께 좁힌다.
- L3는 **git이 깨끗한 상태에서만** 실행한다. 변경분을 되돌릴 수 있어야 한다.

## 3. 호출 골격

```bash
copilot -C <작업디렉터리> \
  -p "<지시 — 무엇을 하고 무엇을 돌려줄지까지>" \
  --model claude-sonnet-5 --effort high \
  --no-ask-user --no-color --log-level none \
  --disable-builtin-mcps \
  --max-ai-credits 30 \
  <§2 권한 플래그> \
  -s
```

- `-s` 는 **에이전트 응답만** 출력한다(통계 없음) — 결과를 파이프로 받을 때 쓴다. 진행과 비용을 보려면 `-s` 를 빼고 `tail -15` 로 받는다.
- `-p` 는 **stdin을 읽지 않는다.** 인자가 필수이며(`-p` 만 주면 `option '-p, --prompt <text>' argument missing`), 긴 지시는 `-p "$(cat prompt.txt)"` 로 넘긴다.
- **Bash 도구 timeout 상한은 600000ms(10분)이며 그보다 큰 값은 무시된다.** 오래 걸릴 작업은 처음부터 `run_in_background: true` 로 실행하고 완료 알림을 기다린다.
- 지시문에 **무엇을 돌려줄지**를 적는다. 위임의 산출물은 파일 변경이 아니라 "받아서 보고할 내용"이다.

### 파라미터

| 항목 | 기본값 | 선택지 |
| --- | --- | --- |
| 모델 | **`claude-sonnet-5`** | `claude-sonnet-5` · `gpt-5.6-sol` · `gpt-5.6-terra` · `gpt-5.6-luna` · `gpt-5.5` · `auto` |
| 추론 강도 | **`high`** | `none` · `minimal` · `low` · `medium` · `high` · `xhigh` · `max` |
| 컨텍스트 창 | **손대지 않는다** (플래그 생략) | `--context default` · `--context long_context` |

사용자가 "sol로 돌려", "강도 낮춰서" 같이 말하면 그 값으로 바꾸고, **아무 말이 없으면 위 기본값을 쓴다.** 골격의 `--model`·`--effort` 를 비워두거나 `auto` 로 대체하지 않는다.

- **`auto` 는 기본값이 아니다.** Copilot이 건별로 모델을 고르므로 싸지지만 **어떤 모델이 돌지 보장이 없어** 같은 지시의 결과가 흔들린다. 재현할 필요가 없는 단발 작업에만 명시적으로 고른다.
- **두 값 모두 CLI가 검증하며, 오타는 모델 호출 전에 즉시 죽으므로 비용이 들지 않는다.** 모델은 `Error: Model "..." from --model flag is not available.`, 강도는 `argument '...' is invalid. Allowed choices are none, minimal, low, medium, high, xhigh, max.` 로 떨어진다. 새 모델명은 부담 없이 시도해 보면 된다.
- **기본 강도 `high` 는 응답이 느려지고 reasoning 토큰이 붙어 1건당 비용이 오른다.** 판단이 필요 없는 기계적 작업(로그 grep·파일 나열·정형 변환)은 `--effort low` 로 낮춰 돌린다 — §3의 timeout 판단과 §4의 비용에 함께 넣는다.
- **컨텍스트 창은 모델이 정한다 — `--context` 플래그를 건드리지 않는다.** 기본 모델 `claude-sonnet-5` 의 카탈로그 상한은 **936,000 토큰**이며, 별도의 `long_context` 항목이 없다(§4-1 조회 결과). `--context long_context` 는 오류 없이 받아들여지지만 카탈로그에 대응 항목이 없으므로 **켠다고 창이 커진다는 근거가 없다.**

### 모델 능력 조회 — 추측하지 않는다

모델의 컨텍스트 상한·추론 강도 지원 여부는 **서버 카탈로그에 있고 로컬 파일에는 없다.** 웹 문서나 기억으로 답하지 말고 SDK로 직접 조회한다(모델을 호출하지 않으므로 **크레딧이 들지 않는다**).

```bash
# @github/copilot-sdk 가 설치된 폴더에서 실행
node -e '
import("@github/copilot-sdk").then(async ({CopilotClient}) => {
  const c = new CopilotClient({mode:"empty", baseDirectory: process.env.HOME+"/.copilot"});
  await c.start?.();
  for (const m of (await c.listModels()).models ?? [])
    console.log(m.id, m.capabilities?.supports?.reasoningEffort, m.capabilities?.limits?.max_prompt_tokens);
  await c.stop?.();
})'
```

기준일(2026-08-22) 조회값 일부 — 카탈로그는 바뀌므로 **인용 전 다시 조회한다.**

| 모델 | 추론 강도 | 컨텍스트 상한 |
| --- | --- | --- |
| `claude-sonnet-5` (기본) | 지원 (`low`~`max`) | 936,000 |
| `claude-opus-5` | 지원 | 936,000 |
| `gpt-5.6-sol` · `gpt-5.5` | 지원 | 922,000 |
| `claude-haiku-4.5` | **미지원** | 136,000 |

⚠️ **추론 강도를 지원하지 않는 모델이 있다**(`claude-sonnet-4.5`·`claude-opus-4.5`·`claude-haiku-4.5`). 그런 모델로 바꿀 때 `--effort` 를 함께 주면 값이 무시된다. 또 CLI가 받는 `none`·`minimal` 은 `claude-sonnet-5` 의 지원 목록에 없다 — 강도를 낮출 때는 `low` 까지만 쓴다.

## 4. 비용 — 실측값으로 판단한다

`"OK만 답해라"` 수준의 프롬프트(출력 4토큰)를 조건만 바꿔 실행한 결과다. 크레딧은 `session-store.db` 의 `total_nano_aiu` 원값이다. **측정은 강도 `medium` 기준이므로 기본 강도 `high` 의 절대값은 이보다 높다** — 조건 간 배율과 캐시 효과를 읽는 용도로 쓴다.

| 실행 조건 | 입력 토큰 | 크레딧 (캐시 미적중 → 적중) |
| --- | --- | --- |
| 프로젝트 루트, 플래그 없음 | 56.2k | 14.06 |
| `/tmp`, 플래그 없음 | 25.3k | 6.33 → **2.26** |
| 프로젝트 루트, `--disable-builtin-mcps --no-custom-instructions` | 34.2k | 8.57 → **4.81** |
| 프로젝트 하위 폴더, `--disable-builtin-mcps` (캐시 거의 전량 적중) | 54.3k | **1.16** |
| 〃, `gpt-5.6-sol` | 34.2k | 8.55 → **0.75** |

**비용은 작업 난이도가 아니라 프리픽스 크기 × 캐시 적중이 정한다.** 출력 4토큰짜리 호출도 위 값이 그대로 나간다. 따라서 "가벼운 job이니까 싸겠지"는 성립하지 않는다.

- **프리픽스를 줄인다** — `--disable-builtin-mcps`(GitHub MCP 도구 정의 제거), `--no-custom-instructions`(`AGENTS.md` 제거). 프로젝트의 `.agents/skills/` 스킬 설명문도 프리픽스에 실린다. 프로젝트 컨텍스트가 필요 없는 작업이면 **작업 디렉터리 자체를 임시 폴더로 두는 것**이 가장 크게 줄인다(56.2k → 25.3k).
- **캐시를 살린다** — 플래그 조합과 작업 디렉터리를 **고정해** 반복 호출한다. 조합을 바꾸면 그 회차는 캐시가 깨져 약 2배가 된다(4.81 → 8.57).
- ⏱ **프롬프트 캐시 수명은 300초다**(`session.usage_checkpoint` 이벤트의 `cacheTtlSeconds` — 실측). 위임을 여러 건 시킬 계획이면 **5분 안에 몰아서** 돌린다. 사이가 벌어지면 매번 미적중 가격(위 표의 왼쪽 값)을 낸다.
- `--max-ai-credits` 는 **최소 30**이고 소프트 캡이다 — 응답이 반환된 뒤에야 초과를 알 수 있어 한 번은 넘길 수 있고, 그다음 호출이 차단된다.

## 5. 결과 처리

- **응답 원문을 보존해 보고한다.** 요약하면서 위임 에이전트가 낸 경고·실패·미해결 항목을 지우지 않는다.
- **L2·L3로 돌렸으면 보고 전에 실제 변경분을 직접 확인한다** — `git status --short` 와 `git diff`. 위임한 에이전트의 자기 보고를 그대로 옮기지 않는다.
- 소모 크레딧을 놓쳤으면(`-s` 로 통계를 숨겼거나 백그라운드 실행) 세션 기록에서 꺼낸다:

```bash
sqlite3 -header -column ~/.copilot/session-store.db \
  "select model, input_tokens, output_tokens, cache_read_tokens,
          round(total_nano_aiu/1e9, 2) as credits, duration_ms
   from assistant_usage_events order by id desc limit 5;"
```

`total_nano_aiu / 1e9` 이 화면에 표시되는 크레딧과 같다(검증: `2255170000` → 2.26).

- 세션 전문이 필요하면 `--share=<path>` 로 마크다운을 남긴다. 이어서 시키려면 종료 시 출력되는 `--resume=<session-id>` 를 쓴다.
- 보고 말미에 **모델·소요 시간·소모 크레딧·실제 변경 파일 수**를 함께 적는다.

## 6. 함정

- **프로젝트 루트에서 돌리면 `.agents/skills/` 와 `AGENTS.md` 가 자동 로드된다.** 프로젝트 규칙이 필요한 작업에는 이점이지만, 프리픽스가 두 배 이상 커진다(25.3k → 56.2k). 작업 성격에 맞게 고른다.
- 종료 후 찍히는 `Shell cwd was reset to ...` 는 정상 출력이며 오류가 아니다.
- CLI 도움말은 `--allow-all-tools` 를 "비대화 모드에 필수"라고 적지만, **실측상 `--allow-tool` 만으로도 비대화 실행이 된다.** 등급을 올릴 이유로 삼지 않는다.
- 세션·설정을 격리해야 하면 `COPILOT_HOME=<dir>` 로 홈을 바꾼다. 이 경우 §5의 크레딧 조회 경로도 그 홈 아래 `session-store.db` 가 된다.
- BYOK(자체 모델 엔드포인트)는 `COPILOT_PROVIDER_BASE_URL` 계열 환경변수로 붙지만, **모델 호출 인증만 우회할 뿐 GitHub 인증 자체를 없애지는 않는다.** 이 스킬의 기본 경로는 아니다.

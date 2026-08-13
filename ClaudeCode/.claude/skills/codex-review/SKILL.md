---
name: codex-review
description: |
  Claude가 작성한 계획·문서·코드를 OpenAI codex CLI(gpt-5.6 계열)로 넘겨 다른 모델 계보의 시각으로 검증받는 스킬. 작성자와 같은 모델이 자기 산출물을 다시 읽으면 자기 결론을 확인하는 방향으로 읽으므로, 모델 자체를 바꿔 지적을 받아온다. 읽기 전용 샌드박스를 강제해 검증 중 파일이 변경되지 않도록 하고, codex 원문 지적을 보존한 채 등급별로 정리해 보고한다.
  트리거: "코덱스로 검증해줘", "코덱스로 리뷰", "codex로 봐줘", "다른 모델로 검증", "다른 모델로 리뷰해줘", "GPT로 교차 검증", "codex review", "review with codex", "cross-check with GPT".
  검증 결과는 보고까지만 하고 반영은 사용자 승인 후에 한다. 같은 모델(Claude) 안에서 도는 3회차 블라인드 재검증은 blind-reverify 담당이며, 이 스킬은 모델 계보를 바꾸는 검증만 한다. 일반 코드 작성·질의응답에는 트리거하지 않는다.
version: 1.2.0
---

# codex-review — codex CLI 교차 검증

Claude가 쓴 것을 Claude가 검토하면 **자기 결론을 확인하는 방향으로 읽는다.** 이 스킬은 검증자를 다른 모델 계보(OpenAI gpt-5.6)로 바꿔 그 편향을 우회한다.

## 1. 실행 전 확인

**codex CLI 기본 설정이 위험하다.** `~/.codex/config.toml`의 sandbox 기본값은 `danger-full-access`, approval은 `never`다. 플래그 없이 호출하면 검증만 시켰는데 파일을 고칠 수 있다. 따라서 이 스킬의 모든 호출은 **샌드박스를 반드시 `read-only`로 강제한다.** 예외 없다. 다만 **전달 방법이 호출 경로마다 다르다** — 자유 프롬프트는 `-s read-only`, `review` 서브커맨드는 `-c sandbox_mode="read-only"`. §4를 그대로 따른다.

`codex` 명령이 없으면 중단하고 사용자에게 알린다 — 설치를 임의로 진행하지 않는다.

## 2. 파라미터

| 항목 | 기본값 | 선택지 |
| --- | --- | --- |
| 모델 | `gpt-5.6-sol` | `gpt-5.6-sol` · `gpt-5.6-terra` · `gpt-5.6-luna` |
| 추론 강도 | `high` | `low` · `medium` · `high` · `xhigh` |
| 샌드박스 | `read-only` | **고정 — 변경 금지** |

사용자가 "terra로", "effort 낮춰서" 같이 말하면 그 값으로 바꾸고, 아무 말이 없으면 기본값을 쓴다.

샌드박스 값(`read-only`·`workspace-write`·`danger-full-access`)은 codex가 검증해 오타 시 즉시 오류를 낸다. 반면 effort는 그렇지 않다.

⚠️ **effort 값은 codex가 검증하지 않는다.** `-c model_reasoning_effort=` 에 잘못된 문자열(`extra-high` 등)을 주면 오류 없이 조용히 빈 응답이 돌아온다. 위 표의 값만 쓰고, 사용자가 "extra high"라고 말하면 `xhigh`로 옮긴다.

## 3. 대상 판별

사용자가 대상을 지정하지 않으면 **미커밋 변경분 전체**(staged + unstaged + untracked)를 대상으로 한다. 명시하면 그것을 따른다 — 특정 파일, 특정 커밋(`--commit <SHA>`), 브랜치 대비(`--base <branch>`).

**대상을 지정받았으면 그대로 진행한다.** 아래 규모 확인은 미커밋 변경분을 대상으로 삼는 경우에만 한다.

실행 전에 `git status --short`로 대상 규모를 확인한다. 변경 파일이 30건을 넘거나 이번 작업과 무관한 파일이 섞여 있으면, 전부 넘기지 말고 **이번 작업으로 바뀐 파일만 범위로 좁혀 사용자에게 알린 뒤 진행한다.** 무관한 변경까지 검증하면 토큰만 쓰고 지적의 신호 대 잡음비가 떨어진다.

## 4. 호출

변경분 리뷰 — codex의 리뷰 전용 서브커맨드를 쓴다. **`review` 서브커맨드는 `-s` 플래그를 받지 않는다**(`error: unexpected argument '-s'`). 샌드박스는 `-c sandbox_mode=` 로 준다.

```bash
time codex exec review --uncommitted -c sandbox_mode="read-only" \
  -m gpt-5.6-sol -c model_reasoning_effort="high" \
  -o /tmp/codex-review.md < /dev/null
```

파일·계획서 검증 — 자유 프롬프트로 기준을 명시한다. 이쪽은 `-s`가 동작한다.

```bash
time codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="high" \
  -o /tmp/codex-review.md \
  "<대상>을 검토해줘. 검토 기준: (1) ... (2) ... 파일은 읽기만 하고 수정하지 마. 한국어로 지적사항만 간결히." \
  < /dev/null
```

**호출 규칙.**

- `< /dev/null` 을 반드시 붙인다. `codex exec`는 stdin을 추가 입력으로 읽으려 대기하므로 없으면 멈춘다.
- git 저장소 밖에서 돌릴 때만 `--skip-git-repo-check`를 추가한다. 저장소 안에서는 불필요하다.
- Bash 도구 timeout을 넉넉히(600000ms 이상) 준다. `high`·`xhigh`는 응답이 느리다 — 220줄 파일 1건에 `high`로 3분 35초가 걸린 실측치가 있다.
- 명령 앞에 `time` 을 붙여 소요 시간을 남긴다. 보고에 함께 적는다.
- 프롬프트에 **"파일은 읽기만 하고 수정하지 마"** 를 명시한다. `read-only` 샌드박스가 이미 강제하지만, 지시를 함께 주면 codex가 수정 시도로 시간을 낭비하지 않는다.

**출력은 `-o` 파일을 정본으로 읽는다.** codex는 스트리밍 중에 지적을 한 번, 통계 뒤에 최종본으로 또 한 번 출력하므로 `tail -N`으로 자르면 사본이 중간에서 잘려 지적을 놓친다. `-o, --output-last-message <FILE>` 는 최종 메시지만 파일로 떨어뜨린다(`exec`·`exec review` 둘 다 지원). 터미널 출력은 진행 확인용으로만 보고, 보고는 이 파일을 읽어서 쓴다.

## 4-1. 구조화 출력 (`--output-schema`)

지적을 산문이 아니라 **고정 필드로 받는다.** `--output-schema schema/findings.json` 을 붙이면 `-o` 파일이 JSON으로 떨어져, 등급·경로·라인·재현조건이 누락 없이 온다. 산문 응답을 옮겨 적는 과정이 사라지므로 **기본으로 사용한다.**

```bash
time codex exec -s read-only -m gpt-5.6-sol -c model_reasoning_effort="high" \
  --output-schema <스킬폴더>/schema/findings.json \
  -o /tmp/codex-review.json \
  "<대상>을 검토해줘. 검토 기준: (1) ... (2) ... 파일은 읽기만 하고 수정하지 마." \
  < /dev/null
```

스키마 구조는 `{summary, findings[]}` 이고 각 finding은 `severity`(상/중/하) · `file` · `line` · `issue` · `repro` · `suggestion` 이다.

⚠️ **스키마는 strict 모드로 검증된다.** `properties`에 있는 키는 **전부 `required`에 넣어야** 하고 `additionalProperties: false` 여야 한다. 하나라도 빠지면 실행이 400으로 죽는다 — `Invalid schema ... 'required' is required to be supplied and to be an array including every key in properties`. 선택 항목을 만들고 싶으면 required에 넣되 "없으면 빈 문자열"로 설명에 적는다.

자유 서술이 필요한 검증(설계 판단·계획 검토 등)에는 스키마를 빼고 §4의 자유 프롬프트 형태를 쓴다.

## 5. 결과 처리

**보고까지만 하고 멈춘다. 반영은 사용자 승인 후에 한다.**

codex의 지적을 원문 그대로 보존한 채 등급별 표로 정리하고, 각 건에 대해 다음을 함께 적는다.

- **판단** — 타당한지, 근거가 약한지, 이미 의도된 것인지
- **출처** — 그 지적이 이번 작업으로 생긴 것인지, 원래 있던 문제를 codex가 발견한 것인지
- **사실 확인이 필요한 건** — 저장소만으로 진위를 못 정하는 지적(업무 주기·조직 사실 등)은 고치지 말고 사용자에게 확인을 요청한다

⚠️ **자기 채점 금지.** 내가 쓴 것을 검증받는 상황이므로, 불리한 지적을 "사소함"으로 눌러 요약하지 않는다. 판단을 덧붙이되 codex의 원래 표현을 지우지 않는다.

보고 말미에 **실제 변경 0건**임을 명시하고, **소요 시간·소모 토큰**을 함께 적는다. 구조화 출력을 썼으면 JSON의 `summary`도 함께 전달한다.

## 6. 알려진 잡음

- 실행 로그에 `ERROR rmcp::transport::worker ... invalid_token`(Atlassian MCP 인증 만료)이 찍힐 수 있다. 리뷰 결과와 무관하므로 보고에 옮기지 않는다. 다만 codex로 Confluence·Jira를 다루는 작업은 이 상태에서 실패한다.
- `hook: PostToolUse Failed` 류 출력도 codex 훅 설정 문제이며 리뷰 결과에 영향이 없다.

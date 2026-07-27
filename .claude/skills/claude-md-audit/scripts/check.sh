#!/usr/bin/env bash
# CLAUDE.md 불변조건 검사 — 후보 추출기
#
# 규칙 파일 안에서 (1) 같은 위험 판정을 가리키는 서로 다른 표현,
# (2) 같은 대상에 걸린 서로 다른 길이·수치 상한, (3) 정의된 용어의 사용처를 뽑는다.
#
# 이 스크립트는 판정하지 않는다. 사전에 등록한 패턴만 매칭하므로 새로 생긴
# 동의어는 놓치고, 두 규칙이 같은 대상을 가리키는지는 사람이 대조해야 한다.
# 0건은 "통과"가 아니라 "등록된 패턴에서는 발견 없음"이다.
#
# usage: check.sh <path-to-CLAUDE.md>

set -uo pipefail

FILE="${1:-}"
if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  echo "usage: check.sh <path-to-CLAUDE.md>" >&2
  exit 2
fi

WIDTH=118

section() {
  printf '\n=== %s ===\n' "$1"
}

hits() {
  grep -nE "$1" "$FILE" 2>/dev/null | cut -c1-$WIDTH || true
}

count() {
  grep -cE "$1" "$FILE" 2>/dev/null || echo 0
}

# (1) 위험 판정을 표현하는 비정의 문구 — 정의 용어로 통일되지 않고 남은 것들
RISK_PROSE='hard to undo|costly to redo|costs only [a-z]+ to redo|minutes to redo|wastes? real work|irreversible|blast radius|safety risk|sent outside|anything costlier'

# (2) 길이·문장 수·분량 상한
LIMITS='a sentence or two|in a sentence|(one|two|three|four) or (two|three|four) sentences|in one line|one line|under [0-9]+|at most [0-9]+|no more than [0-9]+|[0-9]+ (lines|words|sentences)'

# (3) 정의된 위험 용어의 사용처
DEFINED='high-stakes|low-stakes'

section "1. 위험 판정 — 비정의 표현 ($(count "$RISK_PROSE")건)"
hits "$RISK_PROSE"
cat <<'NOTE'

  → 2건 이상이면 서로 같은 판정을 가리키는지 대조한다. 같은 판정이라면
    한 곳에 정의를 두고 나머지는 그 용어를 참조하게 만드는 편이 낫다.
    역할이 다르면(판정 vs 순위 매기기) 남겨두고, 남긴 이유를 보고에 쓴다.
NOTE

section "2. 길이·수치 상한 ($(count "$LIMITS")건)"
hits "$LIMITS"
cat <<'NOTE'

  → 같은 대상(응답 전체 / caveat / push back / 보고 한 줄)에 둘 이상이
    걸려 있으면 불변조건 위반이다. 숫자가 다르면 매 턴 어느 쪽을 따를지
    판단하게 되고, 그 판단은 매번 다르게 나온다.
NOTE

section "3. 정의 용어 사용처 ($(count "$DEFINED")건)"
hits "$DEFINED"
cat <<'NOTE'

  → 정의문이 대상으로 삼은 것(task/answer/action)과 각 사용처가 붙는 대상이
    문법적으로 맞는지 본다. 정의가 task를 대상으로 쓰였는데 assumption이나
    change에 붙어 있으면 타입이 어긋난 것이다.
NOTE

printf '\n'

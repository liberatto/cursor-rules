#!/bin/bash
# GOALDRIVE: Goal-Driven Execution 지시문 자동 주입
# 키워드 매칭: fix

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | jq -r '.prompt // empty')

# 키워드 매칭 (case-insensitive)
if echo "$PROMPT" | grep -qiE 'fix'; then
  INSTRUCTION='[Goal-Driven Execution] 이 작업을 검증 가능한 목표로 변환하고, 다단계 작업은 아래 형식의 계획을 먼저 제시하세요: 1. [Step] → verify: [check] 2. [Step] → verify: [check] 구현 → 자가 검증(self-validation) → 수정을 반복하세요.'

  printf '%s' "$INSTRUCTION"
  exit 0
else
  exit 0
fi

#!/bin/bash
# VERIFYFLAG: verify 키워드 감지 시 마커 파일 생성

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | jq -r '.prompt // empty')

if echo "$PROMPT" | grep -qiE 'verify'; then
  touch /tmp/.claude_verify_needed
fi
exit 0

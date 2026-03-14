#!/bin/bash
# VERIFYGATE: verify 마커 존재 시 실행/테스트 미완료면 종료 차단

if [ -f /tmp/.claude_verify_needed ]; then
  rm /tmp/.claude_verify_needed
  echo '{"decision": "block", "reason": "Unit Test, Integration Test, E2E Test 까지 완료 했는지 확인하고 완료하지 않았다면 모든 테스트로 체계적으로 검증하세요. 실패 시 수정-검증-테스트를 반복하고 최종 결과를 보여주세요."}'
fi
exit 0

#!/bin/bash
# FINALGATE: 매 프롬프트 직전 Final Gate 리마인더 1줄을 컨텍스트에 주입
# 목적: 긴 세션에서 CLAUDE.md(v3.9+) Final Gate 지시 감쇠 보정
# 배포 대상: ~/.claude/settings.json > hooks.UserPromptSubmit (글로벌, 전 프로젝트 적용)
#   — 이 스크립트가 원본(SoT)이며, 글로벌 settings에는 아래 echo 1줄이 인라인으로 배포됨
# 의존성: Final Gate 항목명을 정의한 글로벌 CLAUDE.md(v3.9+) 필요. 훅 없이 문서만 배포하는 것은 무방

echo '[Final Gate] Complete / Sourced / Labeled on every reply; add Attacked / Risk-weighted / Deliverable when the answer is costly to redo or hard to reverse.'
exit 0

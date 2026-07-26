# Claude Desktop 전역 프롬프트

Claude Desktop(claude.ai 포함)의 Chat과 Cowork에 주입할 전역 프롬프트 원본. `~/.claude/CLAUDE.md`(v4.0)의 규칙 중 각 환경에서 유효한 것만 이식한 파생본이다.

## 배포 위치

| 파일 | 주입 위치 | 적용 범위 |
|---|---|---|
| `CHAT-PREFERENCES.md` | Settings → Instructions for Claude (프로필 개인 선호) | 계정 전체 — 모든 대화 |
| `COWORK-INSTRUCTIONS.md` | Settings → Cowork → Global instructions | 모든 Cowork 세션 |

파일 본문을 그대로 복사해 해당 입력란에 붙여넣는다.

## 설계 원칙

- **Chat판**: 실행·테스트가 불가능한 대화 환경. "Verify by Execution" 계열 규칙은 제외하고 인식론 라벨링(certain/likely/assumed)·전제 검증·Answer-first 구조·Rule 12 완결성·Rule 11 자기 공격만 이식.
- **Cowork판**: 실제 파일을 만지는 에이전트 환경. Claude Code 규칙의 축약판 — 사전 사고(Rule 1)·계획+단계별 검증(Rule 4)·최소 변경(Rule 2·3)·파일 안전(Rule 10)·가짜 진행 금지(Rule 6)·보고 규율.
- 두 파일 모두 영어 규칙 + 존댓말 지시 — `~/.claude/CLAUDE.md`와 동일한 패턴.

## 유의사항

- 개인 선호 입력란의 공식 글자수 제한은 미공표. 매 대화 토큰으로 로드되므로 500단어 이내 권장(커뮤니티 가이드 기준, 두 파일 모두 ~400단어).
- Cowork는 폴더 선택 시 **folder instructions**(폴더별 컨텍스트, Claude가 세션 중 스스로 갱신 가능)가 별도로 있다 — 프로젝트별 규칙은 거기에 두고, 전역 지침은 범용으로 유지한다.
- 원본 규칙(`~/.claude/CLAUDE.md`) 개정 시 이 파생본도 함께 점검한다.

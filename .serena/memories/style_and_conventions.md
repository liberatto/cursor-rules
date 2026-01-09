# 스타일 및 컨벤션
- 응답/코멘트: 모든 설명과 주석을 자연스러운 한국어로 작성.
- 코딩 스타일: Python은 snake_case 함수/변수, PascalCase 클래스, UPPER_CASE 상수. Java camelCase 함수/변수, PascalCase 클래스. 기타 언어는 커뮤니티 표준. 명확한 의도 드러나는 이름 사용.
- 문서/파일 규칙: 기본 마크다운(.md) 사용, 설정은 JSON/YAML/TOML 등 적절한 포맷. 파일·폴더명은 소문자+언더스코어(snake_case), 하이픈 대신 언더스코어 권장.
- 주석/문서화: 복잡한 로직·설계 결정에 대해 상세 주석 또는 docstring 요구. 변경 이유와 내용을 문서/커밋으로 남길 것.
- 오류 처리: 예외를 예상하고 try-except 등으로 명확한 에러 메시지 제공.
- Cursor rule 작성 가이드(`cursor_rules.mdc`): frontmatter( description/globs/alwaysApply ) 포함, 굵은 글씨 주요 포인트, 예제 코드 제공, DO/DON'T 예시와 실제 코드 참조 권장, 규칙 간 교차참조 유지.
- 폴더 구조 가이드(`folder-structure.mdc`): reports/debug/test/docs/dev 폴더 용도 및 파일 예시, snake_case 명명, 개발 흐름에 맞춰 문서/테스트/디버그 파일을 배치하도록 권장.
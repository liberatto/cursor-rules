# 프로젝트 개요
- 목적: `.mdc` 규칙 문서와 가이드(계획, 연구, 리포트 작성 등) 모음. 개발/운영 시 참고용 규칙 저장소이며 코드베이스는 거의 없음.
- 기술 스택: 문서 중심 저장소. Serena 활성화를 위해 추가한 최소 Python 파일(`serena_placeholder.py`) 외에 실행되는 애플리케이션, 테스트/빌드 구성은 없음.
- 현재 구조(루트): `_CoreRule.mdc`, `cursor_rules.mdc`, `folder-structure.mdc`, 여러 요청/플랜/리포트 관련 `.mdc`, `README.md`, `serena_placeholder.py`, `chats.db`(git 제외). `taskmaster/` 하위에 워크플로우 문서.
- 기대 구조(가이드): `folder-structure.mdc`에서 정의한 `reports/`, `debug/`, `test/`(pytest), `docs/`, `dev/` 폴더 활용 규칙 존재. 현재는 폴더가 없고 문서로만 가이드가 제공됨.
- 운영 환경: macOS(Darwin).
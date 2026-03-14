---
allowed-tools: *
argument-hint: "<test description>"
description: Conduct systematic testing based on the given test description.
---

# Test Helper

## 📋 Input

`$ARGUMENTS`

---

사용자가 지시한 description에 따라 체계적인 테스트를 진행하는 헬퍼입니다:

1. **테스트 계획 수립**: description 분석 후 테스트 전략 및 범위 결정
2. **스모크 테스트 (Smoke Test/Sanity test)**: 기본적인 동작 여부를 빠르게 확인
3. **테스트 환경 구성**: 필요한 테스트 프레임워크 및 의존성 설정
4. **테스트 케이스 작성**: 단위/통합/E2E 테스트 케이스 구현
5. **테스트 실행 및 검증**: 자동화된 테스트 실행 및 결과 분석
6. **결과 보고**: 테스트 커버리지, 실패 케이스, 개선 사항 리포트

## 테스트 유형별 예시

### 스모크 테스트 (Smoke Test)

- 전체 테스트 전에 기본적인 동작을 빠르게 확인
- CLI/터미널 기반 테스트
  - `기본 실행 여부 확인` (예시: python main.py)
  - `인터랙티브 명령어 테스트` (실행 후 간단한 입력/출력 확인)
  - `서버 시작 여부 확인` (프로세스 실행 및 포트 바인딩)
  - `헬스체크 엔드포인트 테스트` (예시: GET /health, /status)

### 단위 테스트 (Unit Test)

- `함수별 입출력 검증 테스트`
- `클래스 메서드 동작 테스트`
- `예외 처리 시나리오 테스트`

### 통합 테스트 (Integration Test)

- `API 엔드포인트 연동 테스트`
- `데이터베이스 연결 및 쿼리 테스트`
- `외부 서비스 연동 테스트`

### E2E 테스트 (End-to-End Test)

- `사용자 플로우 시나리오 테스트`
- `인터랙티브 테스트(CLI, GUI, API)`
- `런타임 환경에서 사용자 시뮬레이션 테스트`
- `브라우저 자동화 테스트`
- `전체 워크플로우 검증 테스트`

### 성능 테스트 (Performance Test)

- `응답 시간 및 처리량 측정`
- `메모리 사용량 모니터링`
- `부하 테스트 및 스트레스 테스트`

### 보안 테스트 (Security Test)

- `인증/인가 시스템 검증`
- `입력 값 검증 및 XSS 방지`
- `데이터 암호화 및 보안 헤더 검증`

## 테스트 프레임워크 지원

### Python

- pytest, unittest, nose2
- Mock/패치 기반 테스트
- Coverage 분석

### JavaScript/Node.js

- Jest, Mocha, Jasmine
- Cypress, Playwright (E2E)
- Supertest (API 테스트)

### Java

- JUnit, TestNG
- Mockito, Spring Test
- Selenium (UI 테스트)

### 테스트 시 참고 사항

- 기본 자체 CLI 명령어 활용
- 효율적 테스트를 위한 MCP 도구 활용 가능
- 테스트 종료 후 임시 생성한 테스트 코드 삭제

체계적인 테스트 전략을 통해 코드 품질과 신뢰성을 보장합니다.

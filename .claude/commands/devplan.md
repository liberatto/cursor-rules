---
Usage `/plan <TASK_DESCRIPTION>`
argument-hint: [TASK_DESCRIPTION]
description: 사용자가 제시한 작업에 대해 체계적이고 실행 가능한 계획을 수립합니다
model: sonnet
---

사용자가 제시한 작업에 대해 체계적이고 실행 가능한 계획을 수립하고 문서를 생성합니다:

## 📋 계획 수립 과정

### 1. **요구사항 분석 (Requirement Analysis)**
- 작업 목표와 범위 명확화
- 기능적/비기능적 요구사항 분류
- 제약사항 및 의존성 식별
- 우선순위 설정

### 2. **기술적 설계 (Technical Design)**
- 아키텍처 및 설계 패턴 결정
- 필요한 기술 스택 및 라이브러리 선택
 . 최신 검증된 기술 및 best practice 적용, web 검색, MCP 도구 활용
- 데이터 모델 및 API 설계
- 성능 및 확장성 고려사항

### 3. **구현 계획 (Implementation Plan)**
- **📁 파일 구조**: 수정/생성할 파일 목록
- **🔧 함수 설계**: 핵심 함수명과 역할 (1-3문장)
- **⚡ 알고리즘**: 주요 로직 및 데이터 플로우
- **🔗 통합 지점**: 기존 코드와의 연결 방법

### 4. **검증 전략 (Validation Strategy)**
- **🧪 테스트 케이스**: 테스트명과 검증 내용 (5-10단어)
- **📊 성능 지표**: 측정할 메트릭과 목표값
- **🔍 검토 체크리스트**: 코드 품질 및 보안 검토 항목
- **🚀 배포 전략**: 단계별 릴리스 계획

### 5. **위험 관리 (Risk Management)**
- **⚠️ 잠재적 위험**: 기술적 리스크 식별
- **🛡️ 완화 방안**: 위험 대응 전략 및 대안
- **📈 모니터링**: 진행 상황 추적 방법

## 🎯 계획서 구성

### **개요 (Overview)**
> 작업의 핵심 목표와 기대 효과를 간결하게 요약

### **요구사항 및 Task Definition**
> Requirements: List of requirements for the task
> Concise task definition 

### **구현 상세**
```
📁 수정 파일:
- file1.py: 주요 비즈니스 로직 구현
- file2.js: UI 컴포넌트 개발
- config.yaml: 설정 파일 업데이트

🔧 핵심 함수:
- process_data(): 입력 데이터 검증 및 변환 처리
- handle_request(): API 요청 라우팅 및 응답 생성
- validate_input(): 사용자 입력 유효성 검사

🧪 테스트 케이스:
- test_valid_input: 정상 입력값 처리 검증
- test_error_handling: 예외 상황 처리 확인
- test_performance: 성능 기준치 달성 여부

🔍 Checkpoints:
- Action points for step by step implementation with [ ] checkboxes for marking them done.

```

구현을 시작하지 말고 계획 파일만 `PLAN_{주제/날짜/시간}.md` 문서로 만들어 docs/ 폴더에 저장합니다. 

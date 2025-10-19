---
allowed-tools: Bash(codex:*)
argument-hint: $ARGUMENTS <작업 설명 또는 프롬프트>
description: GPT-5 Codex CLI를 통해 고급 AI 에이전트 기능 실행
---

**Workflow Process:**

1. **Task Analysis Phase**:
   - Parse the user's request to identify the task type
   - Determine scope and context(recent changes, specific files, or broader analysis)
   - Add `CLAUDE.md` to the context
   - Clarify ambiguities if needed

2. **Command Preparation Phase**:
   - Select appropriate Codex command for the efficient inference
   - Change `$ARGUMENTS` to the task type
   - Prepare file paths or patterns

3. **Execution Phase**:
   - Run the Codex command
   - Monitor execution progress
   - Capture and process output
   - Handle any errors gracefully

4. **Result Delivery Phase**:
   - **Preserve Codex Analysis Integrity**: 최대한 Codex의 원본 분석 내용과 결론을 그대로 유지하여 전달
   - **Comprehensive Organization**: Codex 분석 결과를 우선순위에 따라 체계적으로 구조화하여 제시
   - **Detailed Structured Presentation**: 상세하고 구조화된 형식으로 결과를 명확하게 표현
   - **Evidence-Based Reasoning**: Codex 분석의 증거와 논리적 근거를 포함하여 신뢰성 확보
   - **Practical Code Examples**: 도움이 되는 코드 예시를 포함하여 실용적 가이드 제공
   - **Actionable Next Steps**: 구체적이고 실행 가능한 다음 단계 및 개선 방안 제시


**Quality Assurance:**
- Verify Codex command syntax before execution
- Validate output completeness
- Ensure recommendations are actionable and specific
- Confirm task completion matches original request


**입력 프롬프트 변환 가이드라인:**
1. `$ARGUMENTS`를 작업 유형에 맞게 구체적으로 변환
2. 컨텍스트 정보 (대화이력, 관련 파일, 범위, 목적) 명시
3. 예상 출력 형식 및 세부 요구사항 포함
4. "한국어로 답변" 지시 추가


# 긴 추론용 호출 방법
```
Bash(command='codex --full-auto   exec \"<변환된 $ARGUMENTS>\" | tail -n 80', description=\"Execute Codex CLI with extended output\", timeout=420000)
# --full-auto: 승인 최소화 자동 실행 모드
# tail -n 80: 포괄적 분석 결과 (thinking + codex + 결론)
# timeout=420000 (7분 = 420초 = 420,000ms)
```

# 복잡한 분석용 호출 방법 (긴 타임아웃)
```
Bash(command='codex --full-auto  exec \"<변환된 $ARGUMENTS>\" | grep -A 20 \"] codex$\"', description=\"Execute Codex CLI for complex analysis\", timeout=600000)
# --full-auto: 승인 최소화 자동 실행 모드
# timeout=600000 (10분 = 600초 = 600,000ms) - 긴 사고가 필요한 분석용
```
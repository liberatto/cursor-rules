
## 🤖 Codex CLI 사용 가이드

> OpenAI Codex CLI를 활용한 코드 리뷰 및 분석 (2026-01-16 세션에서 학습)

### 설치 확인

```bash
which codex  # /opt/homebrew/bin/codex
codex --help
```

### 주요 명령어

| 명령 | 용도 | 비고 |
|------|------|------|
| `codex exec` | 일반 실행 (분석, 질문 등) | 가장 범용적 |
| `codex review` | Git 변경사항 리뷰 | git 저장소 전용 |
| `codex` | 대화형 세션 | 인터랙티브 |

### ⚠️ 주의사항 (세션에서 발견된 이슈)

1. **`-q` 옵션 없음**: `codex -q "prompt"` ❌ → `codex exec "prompt"` ✅
2. **Git 저장소 필수**: 비-git 디렉토리에서는 `--skip-git-repo-check` 필요
3. **`codex review` 제한**: Git 변경사항만 리뷰 (특정 파일 분석은 `codex exec` 사용)

### 사용 예시

#### 파일 분석 (비-git 저장소)

```bash
cd /path/to/project
codex exec "파일명.py를 읽고 코드 품질을 분석해주세요" \
  --full-auto \
  --skip-git-repo-check \
  -o /tmp/review-result.txt
```

#### Git 변경사항 리뷰

```bash
# 특정 브랜치 대비
codex review --base main "보안 취약점 중심으로 리뷰"

# 커밋되지 않은 변경사항
codex review --uncommitted

# 특정 커밋
codex review --commit abc123
```

#### 대화형 세션

```bash
codex "프로젝트 구조를 분석해주세요"
```

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `--full-auto` | 자동 승인 모드 (샌드박스 내) |
| `--skip-git-repo-check` | Git 저장소 검사 스킵 |
| `-o <file>` | 마지막 메시지를 파일로 저장 |
| `-m <model>` | 모델 지정 (기본: gpt-5.2-codex) |
| `--json` | JSONL 형식 출력 |

### Claude Code에서 Codex 호출 패턴

```bash
# 권장 패턴
codex exec "<한국어 프롬프트>" \
  --full-auto \
  --skip-git-repo-check \
  -o /tmp/codex-output.txt 2>&1
```

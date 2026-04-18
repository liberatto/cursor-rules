# VPN/ZTNA 환경에서 Claude Code TLS 설정

> 작성일: 2026-03-13 | 최종 수정: 2026-04-07

---

## 문제

VPN/ZTNA 환경에서 Claude Code 실행 시 Anthropic API 연결 실패.

- VPN/ZTNA가 MITM 방식으로 SSL 트래픽을 가로채면서 자체 인증서를 사용
- Node.js는 OS 인증서 저장소를 사용하지 않고 자체 CA 번들만 신뢰
- 회사 ZTNA 인증서가 Node.js CA 번들에 없으므로 TLS 검증 오류 발생

---

## 해결 방법

### 방법 1 — TLS 검증 비활성화 (빠른 우회)

`~/.zshrc` 또는 `~/.bash_profile`에 추가:

```bash
export NODE_TLS_REJECT_UNAUTHORIZED=0
```

⚠️ **보안 경고**: 모든 TLS 검증을 비활성화하므로 MITM 공격에 취약해짐

| 영향 받음 (Node.js 기반) | 영향 없음 |
|---|---|
| Claude Code | 브라우저 (Chrome, Safari 등) |
| npm, npx, yarn | Python, Java, Go 앱 |
| VS Code 일부 기능 | curl, wget |
| Electron 앱 (Slack, Discord 등) | git (libcurl 기반) |
| MCP 서버 (Node.js 실행) | Docker |

경고 메시지를 숨기려면 함께 설정:

```bash
export NODE_NO_WARNINGS=1
```

**Claude Code에만 한정**하려면 글로벌 export 대신 alias로 제한:

```bash
alias claude='NODE_TLS_REJECT_UNAUTHORIZED=0 claude'
```

---

### 방법 2 — 루트 인증서 등록 (권장 ✅)

회사 ZTNA 루트 인증서를 Node.js에 추가 등록하는 방법. TLS 검증을 유지하면서 회사 인증서만 추가 신뢰한다.

#### Step 1: 루트 인증서 내보내기

**브라우저에서 내보내기 (Chrome 기준)**:

1. 아무 HTTPS 사이트 접속 → 주소창 자물쇠 아이콘 클릭
2. "인증서" → 인증서 체인 최상단의 **루트 CA** 선택
3. 상세 정보 → "내보내기" → PEM 형식(`.pem` 또는 `.crt`)으로 저장

**macOS Keychain에서 내보내기**:

1. Keychain Access 앱 실행 → "시스템" 키체인 선택
2. 회사 루트 CA 인증서 찾기 (예: `Kt Corporation Root CA`)
3. 우클릭 → "내보내기" → `.pem` 형식 선택

#### Step 2: 안정적인 경로에 복사

```bash
mkdir -p ~/.config/certs
cp ~/Downloads/회사인증서.pem ~/.config/certs/company-root-ca.pem
```

> Downloads 폴더는 정리 시 삭제될 수 있으므로 별도 경로에 보관

#### Step 3: 인증서 유효성 확인

```bash
openssl x509 -in ~/.config/certs/company-root-ca.pem -noout -subject -issuer -dates
```

출력 예시:

```
subject=CN=Kt Corporation Root CA
issuer=CN=Kt Corporation Root CA
notBefore=Jul 11 08:08:30 2024 GMT
notAfter=Jul 11 08:08:30 2026 GMT
```

#### Step 4: 환경변수 등록

`~/.zshrc`에 추가:

```bash
export NODE_EXTRA_CA_CERTS="$HOME/.config/certs/company-root-ca.pem"
```

적용: 새 터미널 열기 또는 `source ~/.zshrc`

#### Step 5: 연결 테스트

ZTNA 켠 상태에서 Claude Code 실행하여 정상 연결 확인.

---

### 방법 1 → 방법 2 전환 시

기존 설정을 즉시 삭제하지 말고 주석 처리하여 롤백 가능하게 유지:

```bash
# [비활성화] NODE_EXTRA_CA_CERTS로 대체 — 효과 없으면 주석 해제하여 복원
# export NODE_TLS_REJECT_UNAUTHORIZED=0
# export NODE_NO_WARNINGS=1

# 루트 인증서 등록
export NODE_EXTRA_CA_CERTS="$HOME/.config/certs/company-root-ca.pem"
```

연결 확인 후 문제없으면 주석 처리된 라인 제거.

---

## 비교

| | 방법 1: TLS 비활성화 | 방법 2: 인증서 등록 |
|---|---|---|
| **보안** | ❌ 모든 TLS 검증 해제 | ✅ TLS 검증 유지 |
| **영향 범위** | 모든 Node.js 앱 | 지정 인증서만 추가 신뢰 |
| **설정 난이도** | 한 줄 추가 | 인증서 내보내기 필요 |
| **인증서 만료 관리** | 불필요 | 만료 시 재발급 필요 |
| **권장** | 임시 우회용 | 상시 사용 권장 ✅ |

---

## 인증서 만료 및 갱신

로컬에 저장한 `.pem` 파일은 회사 루트 CA 갱신 시 **자동 갱신되지 않는다**. 수동으로 교체해야 한다.

### 만료일 확인

```bash
openssl x509 -in ~/.config/certs/company-root-ca.pem -noout -enddate
```

### 갱신 절차

1. 브라우저에서 새 루트 인증서 내보내기 (방법 2의 Step 1과 동일)
2. 기존 파일 교체:

```bash
cp ~/Downloads/새인증서.pem ~/.config/certs/company-root-ca.pem
```

3. 새 터미널 열어 연결 확인 (환경변수 경로가 동일하므로 `.zshrc` 수정 불필요)

### 갱신 시점 판단

- 회사 ZTNA 루트 CA는 보통 3~5년 주기로 갱신
- 갱신 시 ZTNA 클라이언트 업데이트와 함께 IT팀 공지가 나올 가능성이 높음
- **증상**: 정상 사용 중 갑자기 Claude Code 연결이 실패하면 인증서 만료를 먼저 의심

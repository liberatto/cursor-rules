# 사내망 SSL/TLS 인증서 오류 해결 가이드

> **마지막 갱신**: 2026-06-02 15:24
> KT 사내망은 보안장비가 HTTPS 트래픽을 가로채 회사 인증서로 다시 서명하는 **TLS 인터셉션**을 한다. 이때 패키지 도구(`pip`·`uv` 등)가 회사 인증서를 "모르는 발급자"로 거부하면서 설치·실행이 실패한다. 도구별 대응책이 다르다.

## 한눈에 보기

| 도구 | 오류 메시지 | 해결책 | 방식 |
|---|---|---|---|
| **pip** | `SSL: CERTIFICATE_VERIFY_FAILED` | `pip-system-certs` 설치 | 패키지 (한 번) |
| **uv** | `invalid peer certificate: UnknownIssuer` | `--native-tls` 플래그 | 옵션 (매번) 또는 환경변수 (영구) |

> 💡 둘 다 뿌리는 **같은 문제**(사내망 TLS 인터셉션)다. 해결 원리도 동일 — "도구가 **OS 인증서 저장소**(회사 인증서가 등록된 곳)를 보게 만들기". 단 도구가 달라 해법은 서로 갈아끼울 수 없다.

---

## 1. pip — `pip-system-certs`

`pip`의 인증서 검증을 OS 인증서 저장소로 영구 리다이렉트하는 패키지다.

```bash
# 일반 venv에 설치
python -m pip install pip-system-certs

# 예: Azure CLI 내장 파이썬에 설치
/opt/homebrew/Cellar/azure-cli/<ver>/libexec/bin/python -m pip install pip-system-certs
```

> 📎 일반 가상환경이든 특정 도구 내장 파이썬(Azure CLI 등)이든 **방식은 동일**하다 — 해당 파이썬의 `pip`으로 설치하면 된다.

📌 **언제 필요한가**
- `SSL: CERTIFICATE_VERIFY_FAILED` 오류 발생 시
- 사내 프록시/내부 인증서 환경에서 `pip install` 실패할 때

📌 **설치 횟수**
- 한 번만 설치하면 유지됨
- 단, 해당 파이썬 환경을 완전 삭제 후 재설치 시 다시 실행 필요

📌 **가상환경별 설치 필요 여부**
- `pip-system-certs`는 **파이썬 인스턴스(venv)마다 개별 설치**가 필요하다
- SSL 오류가 발생한 가상환경에만 설치하면 충분
- 문제가 없는 환경에서는 설치 불필요

---

## 2. uv — `--native-tls`

`uv`는 Rust 기반이라 기본적으로 **자체 내장 인증서 저장소(rustls)** 를 써서 OS(macOS 키체인)에 등록된 회사 인증서를 안 본다. `--native-tls`는 "내장 저장소 말고 **OS 저장소를 써라**"고 지시하는 플래그다.

```bash
uv sync --native-tls              # 의존성 설치
uv run --native-tls train.py      # 스크립트 실행
```

📌 **언제 필요한가**
- `invalid peer certificate: UnknownIssuer` 오류 발생 시
- 사내망에서 `uv sync`·`uv run`이 실패할 때

📌 **매번 붙이기 번거롭다면 (영구 적용)**
셸 프로파일(`~/.zshrc` 등)에 환경변수를 박아두면 플래그 없이 동작한다.

```bash
export UV_NATIVE_TLS=1
```

📌 **외부망에서는?**
- 핸드폰 핫스팟 등 외부망은 TLS 인터셉션이 없으므로 플래그 없이도 그냥 동작
- 즉 `--native-tls`는 **사내망일 때만 필수**

---

## 부록 — 동작 원리

```
패키지 도구가 서버(PyPI 등)에 HTTPS 연결
        │
        ▼
KT 사내망 보안장비가 트래픽을 가로채 회사 인증서로 재서명
        │
        ▼
도구: "이 인증서, 내가 아는 신뢰 발급기관이 아닌데?"  → ❌ 거부
        │
        ▼
[해결] 도구가 OS 인증서 저장소(회사 인증서 등록됨)를 보게 전환
        │
        ▼
        ✅ 회사 인증서를 신뢰 → 정상 동작
```

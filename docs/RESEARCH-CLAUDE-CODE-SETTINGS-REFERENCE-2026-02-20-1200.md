# Claude Code `settings.json` 설정 레퍼런스

> **문서 유형**: Research Report
> **작성일**: 2026-02-20
> **대상 버전**: Claude Code (2026-02 기준)
> **스키마**: `https://json.schemastore.org/claude-code-settings.json`

---

## 1. 설정 파일 계층 구조

### 파일 위치 및 역할

| 파일 | 위치 | Git 추적 | 역할 |
|---|---|---|---|
| `settings.json` | `~/.claude/` | ❌ | 사용자 전역 설정 (모든 프로젝트 적용) |
| `settings.json` | `.claude/` | ✅ | 프로젝트 공유 설정 (팀원과 공유) |
| `settings.local.json` | `.claude/` | ❌ | 프로젝트 로컬 오버라이드 (개인 설정) |
| `managed-settings.json` | 시스템 경로* | ✅ | 관리자 정책 (최고 우선순위, 오버라이드 불가) |

*시스템 경로:
- macOS: `/Library/Application Support/ClaudeCode/`
- Linux/WSL: `/etc/claude-code/`
- Windows: `C:\Program Files\ClaudeCode\`

### 우선순위 (높음 → 낮음)

```
1. managed-settings.json (관리자)       ← 최고 우선순위
2. 명령줄 인자 (--model, --append-system-prompt 등)
3. .claude/settings.local.json (프로젝트 로컬)
4. .claude/settings.json (프로젝트)
5. ~/.claude/settings.json (사용자 전역) ← 최저 우선순위
```

### 설정 병합 규칙

| 타입 | 병합 동작 |
|---|---|
| 배열 (예: `availableModels`) | 병합 후 중복 제거 |
| 객체 (예: `permissions`) | 높은 우선순위 설정이 완전 대체 |
| 스칼라 (String, Boolean, Number) | 높은 우선순위 값 사용 |

---

## 2. 설정 키 상세

### A. 모델 설정 (Model Configuration)

| 키 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `model` | String | `"default"` | 사용할 모델 (별칭 또는 정확한 모델명) |
| `availableModels` | Array | - | `/model` 명령에서 선택 가능한 모델 목록 제한 |
| `alwaysThinkingEnabled` | Boolean | `false` | 세션 시작 시 Extended Thinking 기본 활성화 |
| `effortLevel` | String | `"high"` | 적응형 추론 노력 수준 |

**모델 별칭:**

| 별칭 | 매핑 대상 | 용도 |
|---|---|---|
| `default` | 구독별 상이 (Pro/Max: Opus, API: Sonnet) | 자동 선택 |
| `opus` | Claude Opus 4.6 | 복잡한 추론, 계획 |
| `sonnet` | Claude Sonnet 4.6 | 일상적 코딩 |
| `haiku` | Claude Haiku | 빠르고 단순한 작업 |
| `opusplan` | 계획: Opus, 실행: Sonnet | 비용 효율 최적화 |
| `sonnet[1m]` | Sonnet + 1M 토큰 컨텍스트 | 대규모 코드베이스 |

**effortLevel 값:**

| 값 | 설명 |
|---|---|
| `"low"` | 빠른 응답, 간단한 작업에 적합 |
| `"medium"` | 균형 잡힌 추론 |
| `"high"` | 최대 추론 노력 (기본값) |

```json
{
  "model": "opus",
  "availableModels": ["opus", "sonnet", "haiku"],
  "alwaysThinkingEnabled": true,
  "effortLevel": "medium"
}
```

---

### B. 권한 및 보안 (Permissions)

| 키 | 타입 | 설명 |
|---|---|---|
| `permissions.allow` | Array | 자동 승인되는 도구 사용 패턴 |
| `permissions.ask` | Array | 실행 전 확인 필요 패턴 |
| `permissions.deny` | Array | 완전 차단 패턴 |
| `permissions.additionalDirectories` | Array | 작업 디렉토리 범위 확장 경로 |
| `permissions.defaultMode` | String | 기본 권한 모드 |
| `permissions.disableBypassPermissionsMode` | String | 권한 우회 모드 비활성화 |

**패턴 문법:**

```
도구명                     → "Read" (해당 도구의 모든 작업)
도구명(패턴)               → "Bash(git *)" (특정 명령 패턴)
도구명(경로 glob)          → "Read(./secrets/**)" (경로 패턴)
```

**평가 순서**: deny → ask → allow (첫 매칭 규칙이 최종 결정)

**defaultMode 값:**

| 값 | 설명 |
|---|---|
| `"acceptEdits"` | 파일 편집 자동 승인, 기타 도구는 확인 |
| `"askForEachEdit"` | 모든 편집에 확인 요청 |
| `"askForEachTool"` | 모든 도구 사용에 확인 요청 |

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Read"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./secrets/**)"
    ],
    "additionalDirectories": ["../shared-lib/"],
    "defaultMode": "acceptEdits",
    "disableBypassPermissionsMode": "disable"
  }
}
```

---

### C. 샌드박싱 (Sandbox)

| 키 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `sandbox.enabled` | Boolean | `false` | Bash 명령 샌드박싱 활성화 |
| `sandbox.autoAllowBashIfSandboxed` | Boolean | `true` | 샌드박싱된 명령 자동 승인 |
| `sandbox.excludedCommands` | Array | `[]` | 샌드박스를 우회하는 명령 |
| `sandbox.allowUnsandboxedCommands` | Boolean | `true` | 명령별 샌드박싱 비활성화 허용 |
| `sandbox.enableWeakerNestedSandbox` | Boolean | `false` | 약한 중첩 샌드박스 활성화 |

**네트워크 설정 (`sandbox.network`):**

| 키 | 타입 | 설명 |
|---|---|---|
| `network.allowedDomains` | Array | 화이트리스트 도메인 (예: `["github.com", "*.npmjs.org"]`) |
| `network.allowUnixSockets` | Array | 허용 Unix 소켓 경로 |
| `network.allowAllUnixSockets` | Boolean | 모든 Unix 소켓 허용 (보안 위험) |
| `network.allowLocalBinding` | Boolean | 127.0.0.1/::1 로컬 바인딩 허용 (macOS 전용) |
| `network.httpProxyPort` | Number | HTTP 프록시 포트 |
| `network.socksProxyPort` | Number | SOCKS 프록시 포트 |

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"],
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowLocalBinding": false
    }
  }
}
```

> **주의**: `allowUnixSockets`로 Docker 소켓(`/var/run/docker.sock`) 허용 시 호스트 시스템 전체 접근이 가능해짐

---

### D. 환경 변수 (env)

`env` 객체에 key-value 쌍으로 설정. Claude Code 프로세스에 환경 변수로 주입됨.

```json
{
  "env": {
    "ANTHROPIC_MODEL": "claude-opus-4-6",
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  }
}
```

**주요 환경 변수 레퍼런스:**

| 변수 | 용도 |
|---|---|
| `ANTHROPIC_API_KEY` | API 인증 키 |
| `ANTHROPIC_MODEL` | 기본 모델 지정 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus 별칭이 매핑되는 모델명 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet 별칭이 매핑되는 모델명 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku 별칭이 매핑되는 모델명 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | 서브에이전트(Task 도구) 모델 |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | OpenTelemetry 메트릭 활성화 |
| `OTEL_METRICS_EXPORTER` | OTEL 메트릭 내보내기 방식 (예: `"otlp"`) |
| `DISABLE_TELEMETRY` | 텔레메트리 비활성화 |
| `DISABLE_AUTOUPDATER` | 자동 업데이트 비활성화 |
| `CLAUDE_CODE_SIMPLE` | 최소 모드 (Bash + 파일 도구만 사용) |
| `MAX_THINKING_TOKENS` | Extended Thinking 토큰 예산 |
| `CLAUDE_CODE_USE_BEDROCK` | AWS Bedrock 사용 |
| `CLAUDE_CODE_USE_FOUNDRY` | Microsoft Foundry 사용 |
| `DISABLE_PROMPT_CACHING` | 프롬프트 캐싱 전역 비활성화 |
| `DISABLE_PROMPT_CACHING_OPUS` | Opus만 캐싱 비활성화 |
| `DISABLE_PROMPT_CACHING_SONNET` | Sonnet만 캐싱 비활성화 |
| `DISABLE_PROMPT_CACHING_HAIKU` | Haiku만 캐싱 비활성화 |

---

### E. 출력 및 UI (Output & Interface)

| 키 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `outputStyle` | String | `"default"` | 응답 스타일 |
| `language` | String | `"english"` | UI 언어 |
| `showTurnDuration` | Boolean | `true` | 턴 실행 시간 표시 |
| `terminalProgressBarEnabled` | Boolean | `true` | 터미널 진행률 바 |
| `prefersReducedMotion` | Boolean | `false` | 애니메이션 축소 (접근성) |

**Output Style 옵션:**

| 스타일 | 설명 |
|---|---|
| `"default"` | 소프트웨어 엔지니어링 효율 최적화 (간결한 응답) |
| `"explanatory"` | 코드 패턴과 설계 결정 설명 추가 (deprecated) |
| `"learning"` | 협업 학습 모드, `TODO(human)` 마커 사용 |
| 커스텀명 | `.claude/output-styles/` 또는 `~/.claude/output-styles/`의 Markdown 파일명 |

**커스텀 Output Style 파일 구조:**

```markdown
---
name: My Custom Style
description: 커스텀 스타일 설명
keep-coding-instructions: false
---

# Custom Instructions
응답 방식 커스텀 지시...
```

#### 스피너 커스텀

| 키 | 타입 | 설명 |
|---|---|---|
| `spinnerTipsEnabled` | Boolean | 로딩 중 팁 표시 여부 |
| `spinnerVerbs.mode` | String | `"replace"` (기본 동사 대체) 또는 `"append"` (추가) |
| `spinnerVerbs.verbs` | Array | 커스텀 동사 목록 |
| `spinnerTipsOverride.tips` | Array | 커스텀 팁 문자열 목록 |
| `spinnerTipsOverride.excludeDefault` | Boolean | 기본 팁 제외 여부 |

```json
{
  "spinnerTipsEnabled": true,
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Pondering", "Crafting", "Architecting"]
  },
  "spinnerTipsOverride": {
    "excludeDefault": false,
    "tips": ["Tip: Use /compact to save context window"]
  }
}
```

---

### F. 상태 라인 (statusLine)

터미널 하단에 표시되는 상태 정보. 외부 스크립트 실행 결과를 표시.

| 키 | 타입 | 설명 |
|---|---|---|
| `statusLine.type` | String | `"command"` (외부 명령 실행) |
| `statusLine.command` | String | 실행할 스크립트 경로 |

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

---

### G. 파일 제안 (fileSuggestion)

`@` 멘션 시 파일 자동완성에 사용할 커스텀 명령.

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

---

### H. Git 및 Attribution

| 키 | 타입 | 설명 |
|---|---|---|
| `attribution.commit` | String | 자동 커밋 메시지 템플릿 |
| `attribution.pr` | String | PR 생성 시 추가 텍스트 |
| `respectGitignore` | Boolean | 파일 선택 시 `.gitignore` 존중 여부 |

```json
{
  "attribution": {
    "commit": "Generated with Claude Code",
    "pr": "Generated with Claude Code"
  },
  "respectGitignore": true
}
```

---

### I. 훅 (Hooks)

도구 실행 전/후에 셸 스크립트를 자동 실행하는 시스템.

| 키 | 타입 | 설명 |
|---|---|---|
| `hooks` | Object | 훅 정의 (이벤트별 명령 배열) |
| `disableAllHooks` | Boolean | 모든 훅 비활성화 |
| `allowManagedHooksOnly` | Boolean | 관리자 정의 훅만 실행 허용 |
| `allowManagedPermissionRulesOnly` | Boolean | 관리자 권한 규칙만 적용 |

**훅 이벤트 종류:**

| 이벤트 | 시점 |
|---|---|
| `PreToolUse` | 도구 실행 전 |
| `PostToolUse` | 도구 실행 후 |
| `Notification` | 알림 발생 시 |
| `Stop` | 에이전트 턴 종료 시 |
| `SubagentStop` | 서브에이전트 턴 종료 시 |

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to run bash command'"
          }
        ]
      }
    ]
  }
}
```

---

### J. API 및 인증 (API & Authentication)

| 키 | 타입 | 설명 |
|---|---|---|
| `apiKeyHelper` | String | API 키를 동적으로 생성하는 스크립트 경로 |
| `otelHeadersHelper` | String | OTEL 헤더 생성 스크립트 경로 |
| `forceLoginMethod` | String | 강제 로그인 방식 (`"claudeai"`, `"anthropic"`) |
| `forceLoginOrgUUID` | String | 특정 조직 UUID로 로그인 강제 |
| `awsAuthRefresh` | String | AWS SSO 로그인 명령 |
| `awsCredentialExport` | String | AWS 자격증명 export 스크립트 경로 |

```json
{
  "apiKeyHelper": "/bin/generate_temp_api_key.sh",
  "forceLoginMethod": "claudeai",
  "awsAuthRefresh": "aws sso login --profile myprofile"
}
```

---

### K. MCP 서버 설정

| 키 | 타입 | 설명 |
|---|---|---|
| `enableAllProjectMcpServers` | Boolean | 프로젝트의 모든 MCP 서버 일괄 활성화 |
| `enabledMcpjsonServers` | Array | 활성화할 MCP 서버명 목록 |
| `disabledMcpjsonServers` | Array | 비활성화할 MCP 서버명 목록 |
| `allowedMcpServers` | Array | 허용된 MCP 서버 (객체 배열) |
| `deniedMcpServers` | Array | 거부된 MCP 서버 (객체 배열) |

```json
{
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": ["github", "memory"],
  "disabledMcpjsonServers": ["filesystem"]
}
```

---

### L. 플러그인 및 마켓플레이스

| 키 | 타입 | 설명 |
|---|---|---|
| `enabledPlugins` | Object | 플러그인 활성화 상태 (`{"name@source": true}`) |
| `extraKnownMarketplaces` | Object | 추가 마켓플레이스 정의 |
| `strictKnownMarketplaces` | Array | 엄격한 마켓플레이스 화이트리스트 |

**마켓플레이스 소스 타입:**

| source | 설명 | 예시 |
|---|---|---|
| `"github"` | GitHub 저장소 | `{"source": "github", "repo": "org/repo", "ref": "main"}` |
| `"git"` | Git URL | `{"source": "git", "url": "https://gitlab.example.com/tools.git"}` |
| `"url"` | HTTP URL | `{"source": "url", "url": "https://plugins.example.com/marketplace.json"}` |
| `"npm"` | npm 패키지 | `{"source": "npm", "package": "@acme-corp/plugins"}` |
| `"file"` | 로컬 파일 | `{"source": "file", "path": "/path/to/marketplace.json"}` |
| `"directory"` | 로컬 디렉토리 | `{"source": "directory", "path": "/opt/claude-plugins"}` |
| `"hostPattern"` | 호스트 패턴 | `{"source": "hostPattern", "hostPattern": "^github\\.example\\.com$"}` |

---

### M. 팀 실행 (Teammate Mode)

| 키 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `teammateModeMode` | String | `"auto"` | 에이전트 팀 실행 모드 |
| `preferences.tmuxSplitPanes` | Boolean | - | tmux split panes 모드 사용 |

**teammateModeMode 값:**

| 값 | 동작 |
|---|---|
| `"auto"` | tmux 세션 내에서는 split panes, 그 외 in-process |
| `"tmux"` | 항상 tmux split panes로 팀원 실행 |
| `"in-process"` | 동일 프로세스에서 팀원 실행 |

---

### N. 기타 설정

| 키 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `plansDirectory` | String | `"~/.claude/plans"` | PLAN 파일 저장 디렉토리 |
| `cleanupPeriodDays` | Number | `30` | 세션 기록 보관 기간(일). 0이면 저장 비활성화 |
| `autoUpdatesChannel` | String | `"latest"` | 업데이트 채널 |
| `companyAnnouncements` | Array | - | 세션 시작 시 표시할 공지사항 |
| `$schema` | String | - | JSON 스키마 URL (에디터 자동완성용) |

**autoUpdatesChannel 값:**

| 값 | 설명 |
|---|---|
| `"latest"` | 최신 릴리스 (버그 가능성 있음) |
| `"stable"` | 약 1주일 전 릴리스 (문제 버전 자동 필터링) |

---

## 3. 전체 설정 예시

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  "model": "opus",
  "availableModels": ["opus", "sonnet", "haiku"],
  "effortLevel": "high",

  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Bash(python:*)",
      "Read"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)"
    ],
    "additionalDirectories": ["../shared/"],
    "defaultMode": "acceptEdits"
  },

  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  },

  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  },

  "outputStyle": "default",
  "language": "korean",
  "spinnerTipsEnabled": true,
  "showTurnDuration": true,
  "terminalProgressBarEnabled": true,

  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  },

  "plansDirectory": ".plan",
  "cleanupPeriodDays": 30,
  "autoUpdatesChannel": "latest",

  "teammateModeMode": "auto",
  "preferences": {
    "tmuxSplitPanes": true
  },

  "enabledMcpjsonServers": ["github"],
  "enabledPlugins": {
    "Notion@claude-plugins-official": true
  }
}
```

---

## 4. 주의사항 및 알려진 이슈

| 항목 | 내용 |
|---|---|
| `alwaysThinkingEnabled` | 일부 버전에서 무시되어 매 세션 수동 활성화 필요 |
| `respectGitignore` | 파일 선택 시에만 적용, 다른 컨텍스트에서는 무시될 수 있음 |
| `cleanupPeriodDays: 0` | "정리 비활성화"가 아닌 "기록 저장 완전 비활성화"로 동작 |
| MCP 설정 | `.claude/settings.local.json`의 MCP 설정이 git worktree 사용 시 무작동 가능 |
| Unix 소켓 | Docker 소켓 허용 시 호스트 시스템 전체 접근 가능 (보안 위험) |
| 권한 객체 병합 | 다중 레벨에서 `permissions` 정의 시 병합이 아닌 **완전 대체** |

---

## 5. 참고 자료

- [Claude Code 공식 문서 - Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
- [JSON Schema Store - claude-code-settings.json](https://json.schemastore.org/claude-code-settings.json)

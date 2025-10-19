# Local Memory - 지식, 세션, 메모리 관리 및 검색 실행

Usage: `/mem $ACTION $ARGS`

---
allowed-tools: mcp__local-memory__store_memory, mcp__local-memory__search_memories, mcp__local-memory__update_memory, mcp__local-memory__delete_memory, mcp__local-memory__get_memory_by_id, mcp__local-memory__search_by_tags, mcp__local-memory__search_by_date_range, mcp__local-memory__ask_question, mcp__local-memory__analyze_memories, mcp__local-memory__summarize_memories, mcp__local-memory__get_related_memories, mcp__local-memory__discover_relationships, mcp__local-memory__create_relationship, mcp__local-memory__map_memory_graph, mcp__local-memory__analyze_temporal_patterns, mcp__local-memory__track_learning_progression, mcp__local-memory__detect_knowledge_gaps, mcp__local-memory__categorize_memory, mcp__local-memory__create_category, mcp__local-memory__list_categories, mcp__local-memory__get_category_stats, mcp__local-memory__list_sessions, mcp__local-memory__get_session_stats, mcp__local-memory__create_domain, mcp__local-memory__list_domains, mcp__local-memory__get_domain_stats
argument-hint: $ACTION [store|search|analyze|categorize|relate], $ARGS [content|tags|importance|domain|query|tags|limit|question|context_limit|analyze_memories|track_learning_progression|detect_knowledge_gaps|categorize_memory|create_category|list_categories|get_category_stats|list_sessions|get_session_stats|create_domain|list_domains|get_domain_stats]
description: Local Memory MCP를 활용한 지능형 메모리 관리 시스템 - AI 기반 검색, 분석, 관계 맵핑 지원

---

## 🚀 핵심 기능 (자주 사용)

### 1️⃣ 메모리 저장
```python
result = mcp__local-memory__store_memory(
    content="저장할 내용",
    tags=["태그1", "태그2"],
    importance=8,
    domain="프로젝트명"
)
# ⭐ result의 UUID 반드시 기록 (수정/삭제시 필요)
```

### 2️⃣ 정보 검색
```python
# 자연어 검색
mcp__local-memory__search_memories(query="검색어", limit=10)

# 태그 검색
mcp__local-memory__search_by_tags(tags=["태그명"])

# AI 질의응답
mcp__local-memory__ask_question(question="질문", context_limit=5)
```

## ⚠️ UUID 관리 (중요)

### 🔴 문제: MCP 도구는 UUID를 반환하지 않음
- `search_memories()`, `search_by_tags()` 등은 UUID 미반환
- 메모리 수정/삭제 시 UUID 필수

### ✅ 해결책: API 서버 사용

#### 1. API 서버 자동 시작 스크립트
```bash
# API 응답 없으면 자동으로 daemon 시작
if ! curl -s http://localhost:3002/api/v1/health > /dev/null; then
  echo "API 서버 응답 없음. Daemon 시작 중..."
  local-memory start
  sleep 2
fi
```

#### 2. UUID 조회 및 삭제
```bash
# UUID 검색
curl -s "http://localhost:3002/api/v1/memories/search?query=검색어&limit=10" | \
  jq '.data[]?.memory.id'

# 메모리 삭제
curl -X DELETE "http://localhost:3002/api/v1/memories/UUID"
```

#### 3. DB 직접 접근 (필요시)
- 위치: `~/.local-memory/unified-memories.db`
- SQLite로 직접 쿼리 가능
```bash
sqlite3 ~/.local-memory/unified-memories.db \
  "SELECT id FROM memories WHERE content LIKE '%검색어%';"
```

## 📋 작업 패턴

### 프로젝트 정보 기록
1. `store_memory` → UUID 기록
2. `search_memories` → 관련 정보 검색
3. `analyze_memories` → 패턴 분석

### 메모리 정리
1. API로 UUID 확인
2. `delete_memory(id="UUID")` 또는 API DELETE
3. 일괄 삭제는 API 또는 DB 사용

## 🛠️ 주요 도구 목록

### 기본 관리
- `store_memory` ⭐ (UUID 반환 - 기록 필수!)
- `update_memory` (UUID 필요)
- `delete_memory` (UUID 필요)
- `get_memory_by_id` (UUID 필요)

### 검색 & 분석
- `search_memories` ⭐ 자연어 검색
- `search_by_tags` ⭐ 태그 검색
- `ask_question` ⭐ AI 질의응답
- `analyze_memories` 패턴 분석
- `summarize_memories` 요약

### 고급 기능
- `get_related_memories` 관련 메모리
- `track_learning_progression` 학습 추적
- `detect_knowledge_gaps` 지식 격차
- `create_domain` 도메인 생성
- `list_sessions` 세션 목록

## 💡 Agent 체크리스트

### ✅ 저장 시
- [ ] content, tags, importance, domain 설정
- [ ] **UUID 즉시 기록** (나중에 못 찾음)

### ✅ 검색 시
- [ ] `search_memories` 우선 사용
- [ ] UUID 필요하면 API 사용

### ✅ 삭제/수정 시
- [ ] API로 UUID 먼저 확인
- [ ] daemon 실행 여부 체크
- [ ] MCP 도구로 작업 수행

## 🎯 midmnlu 프로젝트 도메인
```python
mcp__local-memory__create_domain(
    name="midmnlu_project",
    description="kt midm, embedding 모델 활용한 finetune, lora, nlu 프로젝트"
)
```

## 🔧 패키지 설치 및 업데이트
```bash
# 최신 버전으로 업데이트
npm update -g local-memory-mcp
# 현재 버전 확인
pm list -g local-memory-mcp
# 상태 확인
local-memory status
# 데몬 실행 여부 확인 후 미 실행 시 실행
local-memory start
```

---

**📌 핵심 원칙: 저장 시 UUID 기록, 검색 시 API 활용, daemon 자동 시작**
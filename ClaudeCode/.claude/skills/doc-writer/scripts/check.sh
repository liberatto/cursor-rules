#!/usr/bin/env bash
# doc-writer 점검 — 한국어 문서 작성 원칙(references/writing-principles.md §6~§8) 위반을 수치로 검출
# 사용: scripts/check.sh <문서.md>
#
# 적용 대상 = 한국어로 쓰는 모든 문서 타입(협업·이해). NOTE(개인 메모)에는 강제하지 않는다.
# 신규 작성과 기존 문서 갱신에 같은 규칙을 적용한다 — 갱신에서는 이번에 고친 줄만 보면 된다
# (문체 규약은 소급 적용하지 않는다 · writing-principles §7 서두).
#
# 주의: 회피 예시를 그대로 인용한 줄·코드블록 안의 매칭은 오탐일 수 있다. 출력 줄을 보고 본문만 판단한다.
set -uo pipefail

SRC="${1:?문서 경로 필요}"
[ -f "$SRC" ] || { echo "파일 없음: $SRC" >&2; exit 1; }

# 아래 문체 축에서만 YAML 프론트매터를 제외한다 — revisions 에 회피 표현이 그대로 인용돼 오탐을 만든다.
# 구조 축(§6)은 성격이 반대라 스크립트 끝에서 원본을 그대로 읽는다.
# 원본 줄번호를 보존해야 하므로 삭제 대신 공백 줄로 치환한다.
F="$(mktemp)"; trap 'rm -f "$F"' EXIT
awk 'NR==1 && $0=="---" {fm=1; print ""; next}
     fm==1 && $0=="---" {fm=0; print ""; next}
     fm==1 {print ""; next}
     {print}' "$SRC" > "$F"

cnt() { grep -cE "$1" "$F" 2>/dev/null || true; }
hit() { grep -nE "$1" "$F" 2>/dev/null | head -"${2:-10}" | cut -c1-170 || true; }

# ── §7.1 평서형 종결 — 존댓말 금지 ─────────────────────────────
POLITE='(합니다|입니다|습니다|됩니다|드립니다|하세요|해요|이에요|예요)'

# ── §7.3 구어·감정 표현 회피 (어휘 표) ─────────────────────────
# 오탐이 큰 낱말(잡다·무기한·뿌리내리다 등)은 조사까지 붙여 좁힌다.
COLLOQ='깔았|깔아서|박는다|박아|박힌|박혀|못박|잡는다|잡았다|건드리|손대|풀리지|뒤집(히|어|은|는다)|되돌리|되돌린|가르다|가르고|가른다|가르는|갈라 |갈랐|갈리다|갈리는|갈린다|갈리면|갈리므로|(두|세|네|여러) 갈래|무너지|터진다|터졌|가려지|스쳐 지나|숨을 공간|희미해|흔들리|부풀|낡다|낡은|낡아|오염시|굴리|굴린다|감으로 |쥐여|얹다|얹어|얹으|얹은|뜯어고치|바닥부터|무기(로|가|는|를) |판정승|손색없|계보|족보|뿌리(가|를|는|에) |DNA|유전자|태생|떠받치|잡아내|막힌다|막히면|막혀|채워지|게임체인저|패러다임|판을 바꾸|붙는 자리|붙는 지점|걸리는 자리|자리를 차지|무게가 (커|실)'

# ── §7.3 비유 (신호·색 / 물리·재난 / 의인화 / 공간·부착) ────────
# 낱말만으로는 전부 잡히지 않는다 — 아래는 반복 출현이 확인된 형태만 등재하고,
# 나머지는 마지막의 수동 통독 항목으로 넘긴다.
METAPHOR='빨간불|초록으로|녹색 신호|붕괴(한|하|된)|폭락|거짓말을|속는다|놓인다|논리가 선다|그릇|입구가 없|무게를 싣|서 있다|선 다음'

# ── §7.4 격식 한자어 ───────────────────────────────────────────
# `강구`·`함의`는 인명(박강구)·복합어(포함의)에 부분 일치하므로 어미까지 붙여 좁힌다.
HANJA='구동(하|되|을)|제고(하|를|가)|강구(하|한|할|해)|도모(하|한|할)|모색(하|한|할)|관건(이|은|을)|용이(하|성)|지양(하|한|할)|(^|[^가-힣])함의'

# ── §7.5 영어 직역체 ───────────────────────────────────────────
# `성립한다(holds)`는 §7.3 이 권장 표현으로 지정한 낱말이라 등재하지 않는다(규칙 충돌).
TRANS='1급 \(|배타적이지 않|오버킬|swap|따라감|닫혔다|닫는다|원시체'

# ── §7.13 설득·수사 문장 ───────────────────────────────────────
RHET='반드시 |매우 |훨씬 |획기적|홀로 서지|그래서\?|말할 것도 없'

# ── 이해 준비 점검 1번 — 개인 절대경로 ─────────────────────────
ABSPATH='/(Users|home)/[a-zA-Z0-9._-]+/'

# ── §8.3-3 산문 안 화살표 체인 (코드블록·표 밖) ─────────────────
ARROW_N=$(awk '/^```/{c=!c} !c && $0 !~ /^\s*\|/ && $0 !~ /^\s*[-*] / && /→.*→/ {n++} END{print n+0}' "$F")

echo "■ doc-writer 점검: $SRC ($(wc -l < "$F" | tr -d ' ')줄, 프론트매터 제외)"
echo
echo "[존댓말 종결 §7.1]     $(cnt "$POLITE")건";   hit "$POLITE"
echo "[구어·감정 어휘 §7.3]  $(cnt "$COLLOQ")건";   hit "$COLLOQ"
echo "[비유 §7.3]           $(cnt "$METAPHOR")건"; hit "$METAPHOR"
echo "[격식 한자어 §7.4]     $(cnt "$HANJA")건";    hit "$HANJA" 6
echo "[영어 직역체 §7.5]     $(cnt "$TRANS")건";    hit "$TRANS" 6
echo "[설득·수사 §7.13]      $(cnt "$RHET")건";     hit "$RHET" 6
echo "[개인 절대경로]        $(cnt "$ABSPATH")건";  hit "$ABSPATH" 6
echo "[산문 화살표 체인 §8.3] ${ARROW_N}건"

# ── §6.1 자기 절 번호 참조 = 전체 § − 외부 문서 § ───────────────
ALL=$(grep -oE '§[0-9]+(\.[0-9]+)?' "$F" 2>/dev/null | wc -l | tr -d ' ')
EXT=$(grep -oE '(대상 문서|[A-Za-z_.-]+\.md) §[0-9]+(\.[0-9]+)?' "$F" 2>/dev/null | wc -l | tr -d ' ')
echo "[자기 절 번호 참조 §6.1] $((ALL - EXT))건 (전체 ${ALL} − 외부 ${EXT})"

# ── §6 프론트매터 구조 ─────────────────────────────────────────
# 검색 표면이 성립하는지만 본다 — 필수 필드·열거값·한 줄 완결·별칭 개수.
# 폴더 위치는 보지 않는다: `_archive/` 는 종료된 문서와 잠시 보류한 문서를 함께 담으므로
# 경로에서 status 를 추정하면 되살려 쓰는 문서를 낡았다고 잘못 판정한다(§6 status 항목).
FM_N=0; FM_OUT=""; FM_SKIP=""
fm_bad() { FM_N=$((FM_N+1)); FM_OUT="${FM_OUT}   · $1
"; }

if [ "$(head -1 "$SRC")" != "---" ]; then
  fm_bad "프론트매터 없음 — NOTE 외에는 §6 형식으로 둔다"
else
  FM_END=$(awk 'NR>1 && /^---[[:space:]]*$/{print NR; exit}' "$SRC")
  if [ -z "$FM_END" ]; then
    fm_bad "닫는 --- 없음"
  else
    FM=$(sed -n "2,$((FM_END-1))p" "$SRC")
    FM_TYPE=$(printf '%s\n' "$FM" | grep -m1 '^type:' | sed 's/^type:[[:space:]]*//;s/[[:space:]]*$//')
    if printf '%s' "$FM_TYPE" | grep -qiE '^note$'; then
      FM_SKIP="NOTE — 구조 검사 생략(§6)"
    else
      for k in type audience keywords created status description; do
        printf '%s\n' "$FM" | grep -q "^${k}:" || fm_bad "필수 필드 누락 — ${k}"
      done

      printf '%s' "$FM_TYPE" | grep -qE '^(prd|plan|adr|handoff|research|strategy|analysis|report|documentation|guide|reference|note)$' \
        || fm_bad "type 열거값 이탈 — '${FM_TYPE}' (소문자 12종 중 하나)"

      FM_ST=$(printf '%s\n' "$FM" | grep -m1 '^status:' | sed 's/^status:[[:space:]]*//')
      printf '%s' "$FM_ST" | grep -qE '^(draft|active|superseded|rejected|archived)([[:space:]]|$)' \
        || fm_bad "status 문두 이탈 — '${FM_ST}' (열거값으로 시작하고 부연은 ' — ' 뒤에)"

      FM_KW=$(printf '%s\n' "$FM" | grep -m1 '^keywords:' | sed 's/^keywords:[[:space:]]*//')
      if [ -n "$FM_KW" ]; then
        printf '%s' "$FM_KW" | grep -qE '^\[.*\]$' || fm_bad "keywords 형식 — 인라인 배열 [a, b, c] 로 둔다"
        KWN=$(printf '%s' "$FM_KW" | sed 's/^\[//;s/\]$//' | tr ',' '\n' | grep -c '[^[:space:]]')
        [ "$KWN" -ge 3 ] || fm_bad "keywords ${KWN}개 — 3~6개로 둔다(정식명·약어·식별자)"
      fi

      DL=$(grep -n '^description:' "$SRC" | head -1 | cut -d: -f1)
      if [ -n "$DL" ]; then
        sed -n "${DL}p" "$SRC" | grep -qE '^description:[[:space:]]*[|>]' \
          && fm_bad "description 블록 스타일(|·>) — grep 이 첫 줄만 가져간다"
        sed -n "$((DL+1))p" "$SRC" | grep -qE '^([a-zA-Z_-]+:|---[[:space:]]*$)' \
          || fm_bad "description 다음 줄로 이어짐 — 한 줄로 끝낸다"
      fi
    fi
  fi
fi


# YAML 파싱 가능 여부 — grep 축이 잡지 못하는 결함(값 안의 `: `·선두 `*`·백틱·따옴표 미이스케이프).
# python3+PyYAML 이 없으면 조용히 건너뛴다(이 검사만 빠지고 나머지 축은 그대로 돈다).
if [ -z "$FM_SKIP" ] && command -v python3 >/dev/null 2>&1; then
  YERR=$(python3 -c '
import io,sys
try: import yaml
except ImportError: sys.exit(0)
s=io.open(sys.argv[1],encoding="utf-8").read().split("\n")
if not s or s[0].strip()!="---": sys.exit(0)
e=[i for i in range(1,len(s)) if s[i].strip()=="---"]
if not e: sys.exit(0)
try: yaml.safe_load("\n".join(s[1:e[0]]))
except Exception as ex: print(str(ex).split("\n")[0])
' "$SRC" 2>/dev/null)
  [ -n "$YERR" ] && fm_bad "YAML 파싱 실패 — ${YERR}"
fi

if [ -n "$FM_SKIP" ]; then
  echo "[프론트매터 구조 §6]   ${FM_SKIP}"
else
  echo "[프론트매터 구조 §6]   ${FM_N}건"
  [ -n "$FM_OUT" ] && printf '%s' "$FM_OUT"
fi

echo
echo "■ 모든 축 0건 확인 후 마감."
echo "■ 스크립트가 잡지 못하는 것 — 저장 전에 직접 통독한다."
echo "   · 비유: 낱말 목록으로 걸리지 않는 형태가 남는다."
echo "     판단 기준(§7.3) = 이 문장을 영문 릴리스 노트·API 문서로 번역해도 자연스러운가."
echo "   · 도식(§8.3): 소속·이동·전후를 말로만 설명한 문단은 빠진 도식이다."
echo "   · 확실성 표시: 추정·미확인·원문 부재를 확인 사실과 같은 어조로 적지 않았는가."

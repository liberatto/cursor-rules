#!/usr/bin/env bash
# report-style 점검 — 하우스 스타일 위반을 수치로 검출
# 사용: scripts/check.sh <원고.md> [--exec]
#   --exec = 임원·부문 보고 레이어(엠대시 빈도 가드 추가)
# 주의: 회피 예시·코드블록·인용(>) 안의 매칭은 오탐일 수 있음 — 출력 줄을 보고 본문만 판단.
set -uo pipefail

SRC="${1:?원고 경로 필요}"
LAYER="${2:-}"
[ -f "$SRC" ] || { echo "파일 없음: $SRC" >&2; exit 1; }

# 아래 문체 축에서만 YAML 프론트매터를 제외한다 — 개정 이력에 회피 표현이 그대로 인용돼 오탐을 만든다.
# 구조 축(§3.1)은 성격이 반대라 스크립트 끝에서 원본을 그대로 읽는다.
# 원본 줄번호를 보존해야 하므로 삭제 대신 공백 줄로 치환한다.
F="$(mktemp)"; trap 'rm -f "$F"' EXIT
awk 'NR==1 && $0=="---" {fm=1; print ""; next}
     fm==1 && $0=="---" {fm=0; print ""; next}
     fm==1 {print ""; next}
     {print}' "$SRC" > "$F"

cnt() { grep -cE "$1" "$F" 2>/dev/null || true; }
hit() { grep -nE "$1" "$F" 2>/dev/null | head -"${2:-15}" | cut -c1-170 || true; }

NOUN='(합니다|습니다|입니다|했다|한다|이다|된다|것이다)[.。]?$'
POLITE='드립니다|바랍니다|주시기|감사합니다'
HANJA='구동|제고|강구|도모|모색|기저|추이|관건|용이|지양|지향|상정|주지(시|의)|수급|비등|기제|소관|준용|전건|환류|포괄(하|되|적)|선택지'
XREF='전략문서 §|계획문서 §|상세는 §|→ §[0-9]|\(§[0-9].*참조\)'
# 1인칭·소속 대명사 (§2.9.1) — 제3자가 주체를 특정 못 함. 우리나라·우리말은 제외
PRONOUN='(^|[^가-힣])(우리[ ]?(팀|측|Agent|과제|담당)?[ 은는이가의를와]|저희|당사|자사)'
# 타 조직 거리 지칭 (§2.9.3)
OTHERORG='상대[ ]?(측|팀|조직|추진|솔루션|채택|기관)'
# 혈통·생물 비유 명사 (§2.8) — 유형·패턴·계열·구조로 교체
METAPHOR='계보|족보|(같은|한|동일) 뿌리|DNA를|유전자(를|적)|태생적'
# 물성·분할 비유 동사 (§2.8) — 정의·구성·정리·확정 / 나눔·분리·구분으로 교체. 오탐 적은 항목만 등재
# 가르다·갈리다 계열은 `가르치다`(가-르-치)와 자형이 달라 오탐 없음 — 저장소 전수 대조로 확인
COLLOQ='굳히|굳혀|굳힘|굳힐|굳혔|가르고|가른다|가르는|가른 |갈라 |갈랐|갈리다|갈리는|갈린다|갈리면|갈렸|갈림|(두|세|네|여러) 갈래'

echo "■ report-style 점검: $SRC ($(wc -l < "$F" | tr -d ' ')줄, 프론트매터 제외)"
echo
echo "[명사형 종결 위반] $(cnt "$NOUN")건";   hit "$NOUN"
echo
echo "[공손도]          $(cnt "$POLITE")건";  hit "$POLITE" 8
echo "[한자어]          $(cnt "$HANJA")건";   hit "$HANJA" 8
echo "[자립성 cross-ref] $(cnt "$XREF")건";   hit "$XREF" 8
echo "[#### 과깊이]      $(cnt '^####')건"
echo "[1인칭·소속 대명사] $(cnt "$PRONOUN")건"; hit "$PRONOUN" 8
echo "[타 조직 거리 지칭] $(cnt "$OTHERORG")건"; hit "$OTHERORG" 8
echo "[혈통·생물 비유]   $(cnt "$METAPHOR")건"; hit "$METAPHOR" 8
echo "[물성·분할 비유 동사] $(cnt "$COLLOQ")건"; hit "$COLLOQ" 8

# 타 팀 명칭 인벤토리 — 축약형이 섞였는지 사람이 판단하도록 목록만 제시 (§2.9.2)
TEAMS=$(grep -oE '[A-Za-z가-힣]+팀' "$F" 2>/dev/null | sort | uniq -c | sort -rn | head -12 | tr '\n' ';' || true)
echo "[팀 명칭 인벤토리]  ${TEAMS:-없음}"
echo "  ↳ 같은 조직의 축약형·전체 명칭이 함께 보이면 전체 명칭으로 통일 (§2.9.2)"

# ── §3.1 프론트매터 구조 ───────────────────────────────────────
# 필수 필드·keywords 형식·description 한 줄 완결만 본다.
# `type`·`status` 는 본 스킬이 열린 값으로 두므로(§3.1 — `active`·`draft`·`archived` 등) 열거 검사를 넣지 않는다.
FM_N=0; FM_OUT=""
fm_bad() { FM_N=$((FM_N+1)); FM_OUT="${FM_OUT}   · $1
"; }

if [ "$(head -1 "$SRC")" != "---" ]; then
  fm_bad "프론트매터 없음 — §3.1 형식으로 최상단에 둔다"
else
  FM_END=$(awk 'NR>1 && /^---[[:space:]]*$/{print NR; exit}' "$SRC")
  if [ -z "$FM_END" ]; then
    fm_bad "닫는 --- 없음"
  else
    FM=$(sed -n "2,$((FM_END-1))p" "$SRC")
    for k in type audience keywords created status description; do
      printf '%s\n' "$FM" | grep -q "^${k}:" || fm_bad "필수 필드 누락 — ${k}"
    done

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

# YAML 파싱 가능 여부 — grep 축이 잡지 못하는 결함(값 안의 `: `·선두 `*`·백틱·따옴표 미이스케이프).
# python3+PyYAML 이 없으면 조용히 건너뛴다(이 검사만 빠지고 나머지 축은 그대로 돈다).
if command -v python3 >/dev/null 2>&1; then
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

echo "[프론트매터 구조 §3.1] ${FM_N}건"
[ -n "$FM_OUT" ] && printf '%s' "$FM_OUT"

if [ "$LAYER" = "--exec" ]; then
  # 엠대시: 표 셀(^|)·섹션 제목(^#) 예외는 빼고 본문만
  EM=$(grep -vE '^\s*\||^#' "$F" | grep -o '—' | wc -l | tr -d ' ')
  LN=$(wc -l < "$F" | tr -d ' ')
  echo
  awk "BEGIN{printf \"[엠대시 빈도(본문)] %d개 / %d줄 = %.1f/100줄 (상한 1)\n\", $EM, $LN, ($LN?$EM/$LN*100:0)}"

  # 정도부사 단독 — 수치 없는 효과 서술 (R6)
  ADV='크게 (개선|향상|단축|증가|감소)|대폭 (개선|향상|단축|확대)|매우 (빠르|우수|효과)|획기적'
  echo "[정도부사 단독]   $(cnt "$ADV")건"; hit "$ADV" 8

  # 제목 수식 분사 — 행위 서술형 제목의 번역체 수식 (R11)
  TITLEMOD='^#+ .*(뒷받침하는|기여하는|촉진하는|견인하는|제고하는)'
  echo "[제목 수식 분사]  $(cnt "$TITLEMOD")건"; hit "$TITLEMOD" 8

  # 볼드 안 어미 — 볼드 경계를 어절에서 끊지 않은 경우 (R2·§8.4)
  BOLDEND='\*\*[^*]{2,}(하여|하고|하는|되어|해서|이며)\*\*'
  echo "[볼드 안 어미]    $(cnt "$BOLDEND")건"; hit "$BOLDEND" 8
fi

echo
echo "■ 모든 축 0건(엠대시는 ≤1/100줄) 확인 후 마감."

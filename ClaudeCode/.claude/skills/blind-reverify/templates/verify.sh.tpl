#!/usr/bin/env bash
# {{대상명}} 재검증 — 객관 게이트
# exit 0 = 3회차 전부 완료·형식 충족. exit 1 = 미완(사유 출력).
# 사용: bash {{작업폴더}}/scripts/verify.sh
#
# ⚠️ 작성 직후 산출물 0개 상태에서 실행해 exit 1이 나오는지 확인할 것.
#    빈 상태에서 통과하면 이 게이트는 아무것도 검사하지 않는 것이다.

set -uo pipefail

# V = 이 스크립트가 든 scripts/ 의 부모 = 작업폴더. 깊이와 무관하게 항상 성립한다.
V="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# 검증 대상 저장소는 절대경로로 지정한다(상대경로는 실행 위치에 따라 깨진다).
# 대상 저장소가 없는 검증이면 빈 문자열로 두면 해당 검사를 건너뛴다.
TARGET_REPO="{{검증 대상 저장소 절대경로 또는 빈 문자열}}"

R1="$V/R1-blind.md"
R2="$V/R2-refutation.md"
R3="$V/R3-final.md"
CO="$V/CORRECTIONS.md"

# 판정 대상 목록 — 근거 라인의 <항목명>과 정확히 일치해야 한다
ITEMS=({{항목1 항목2 항목3 ...}})

# 구분 목록 — 근거 라인의 <구분>. 지표가 없는 대상이면 ("_") 하나만 둔다
DIMS=({{G1 G2 ... 또는 _}})

# 원본이 제기한 결함 식별자 — R3가 전건 판정해야 한다
DEFECTS=({{F1 F2 ... }})

fail=0
note() { printf '  %s\n' "$1"; }
bad()  { printf '❌ %s\n' "$1"; fail=1; }
ok()   { printf '✅ %s\n' "$1"; }

# 근거 라인 형식:  - <항목> | <구분> | <✅|⚠️|❌|➖> | <근거: 백틱 명령 또는 path:line>
count_graded() {
  local f="$1" d="$2" n=0 i
  for i in "${ITEMS[@]}"; do
    grep -qE "^[[:space:]]*-[[:space:]]*${i}[[:space:]]*\|[[:space:]]*${d}[[:space:]]*\|[[:space:]]*(✅|⚠️|❌|➖)" "$f" 2>/dev/null && n=$((n+1))
  done
  echo "$n"
}

count_evidenced() {
  local f="$1" d="$2" n=0 i line
  for i in "${ITEMS[@]}"; do
    line=$(grep -E "^[[:space:]]*-[[:space:]]*${i}[[:space:]]*\|[[:space:]]*${d}[[:space:]]*\|" "$f" 2>/dev/null | head -1)
    [ -z "$line" ] && continue
    if printf '%s' "$line" | grep -qE '`[^`]+`|[A-Za-z0-9_./-]+\.[a-z]+:[0-9]+'; then
      n=$((n+1))                                    # 실행 명령 또는 파일:줄 있음
    elif printf '%s' "$line" | grep -qE '\|[[:space:]]*➖[[:space:]]*\|[[:space:]]*[^[:space:]]'; then
      n=$((n+1))                                    # N/A는 사유 문장만으로 인정
    fi
  done
  echo "$n"
}

check_matrix() {
  local f="$1" label="$2" d graded ev tot_g=0 tot_e=0
  local need=$(( ${#ITEMS[@]} * ${#DIMS[@]} ))
  if [ ! -f "$f" ]; then bad "$label 없음: $(basename "$f")"; return; fi
  for d in "${DIMS[@]}"; do
    graded=$(count_graded "$f" "$d"); ev=$(count_evidenced "$f" "$d")
    tot_g=$((tot_g+graded)); tot_e=$((tot_e+ev))
    [ "$graded" -lt "${#ITEMS[@]}" ] && note "$label $d: 판정 $graded/${#ITEMS[@]}"
    [ "$ev" -lt "$graded" ] && note "$label $d: 근거 누락 $((graded-ev))건"
  done
  if [ "$tot_g" -eq "$need" ] && [ "$tot_e" -eq "$need" ]; then
    ok "$label ${need}칸 판정+근거 완비"
  else
    bad "$label 미완 — 판정 $tot_g/$need, 근거 $tot_e/$need"
  fi
}

echo "=== 1. 산출 파일 존재 ==="
for f in "$R1" "$R2" "$R3" "$CO"; do
  [ -f "$f" ] && ok "$(basename "$f")" || bad "없음: $(basename "$f")"
done

echo
echo "=== 2·3. 판정 칸 + 근거 동반 ==="
check_matrix "$R1" "R1"
check_matrix "$R3" "R3"

echo
echo "=== 4. 원본 결함 전건 처리 ==="
if [ -f "$R3" ]; then
  miss=""
  for d in "${DEFECTS[@]}"; do
    grep -qE "${d}\b.*(확정|정정|반증됨|보류)" "$R3" || miss="$miss $d"
  done
  [ -z "$miss" ] && ok "결함 ${#DEFECTS[@]}건 전건 판정" || bad "판정 누락:$miss"
else
  bad "R3 없음 — 결함 판정 확인 불가"
fi

echo
echo "=== 5. 검증 대상 청결 ==="
if [ -d "$TARGET_REPO" ]; then
  dirty=$(git -C "$TARGET_REPO" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  [ "$dirty" = "0" ] && ok "대상 저장소 변경 0건" || bad "오염 ${dirty}건 — 재현물 원복 필요"
  # 실행이 남기는 산물이 있으면 여기에 추가
  # [ -e "$TARGET_REPO/{{잔존물}}" ] && bad "{{잔존물}} 잔존 — 삭제 필요"
else
  note "대상 저장소 검사 생략 (경로 없음)"
fi

echo
echo "=== 6. 정정 목록 형식 ==="
if [ -f "$CO" ]; then
  rows=$(grep -cE '^\|[^|]+\|[^|]+\|[^|]+\|' "$CO" 2>/dev/null || echo 0)
  cmds=$(grep -cE '`[^`]+`' "$CO" 2>/dev/null || echo 0)
  secs=$(grep -cE '^##+ *[ABC][.．]' "$CO" 2>/dev/null || echo 0)
  if   [ "$rows" -le 2 ]; then bad "표 내용 없음 (정정 0건이면 '정정 없음' 행을 명시할 것)"
  elif [ "$cmds" -eq 0 ]; then bad "재현 명령 없음"
  elif [ "$secs" -lt 3 ]; then bad "A/B/C 구획 분리 안 됨 (현재 ${secs}개)"
  else ok "정정 표 ${rows}행 · 재현 명령 ${cmds}건 · 구획 ${secs}개"
  fi
else
  bad "CORRECTIONS.md 없음"
fi

# ===== 7. 산술 검산 (수치가 있는 산출물이면 반드시 활성화) =====
# 등급 기호에서 점수·밴드를 재계산해 문서 표기와 대조한다.
# 판정만 대조하면 합산 오류가 그대로 남는다 — 실제 발생 사례 있음.
#
# echo
# echo "=== 7. 산술 검산 ==="
# python3 {{작업폴더}}/scripts/recompute.py "$R3" && ok "산술 전건 일치" || bad "산술 불일치"

echo
if [ "$fail" -eq 0 ]; then
  echo "🟢 GATE PASS — 재검증 완료 조건 충족"; exit 0
else
  echo "🔴 GATE FAIL — 위 항목 미충족. 회차 계속"; exit 1
fi

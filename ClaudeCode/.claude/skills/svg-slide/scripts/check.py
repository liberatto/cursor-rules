#!/usr/bin/env python3
"""발표용 SVG 슬라이드 스타일 기계 점검.

사용법:
    python3 check.py <파일.svg> [--executive]

검사 축 (하우스 스타일 SoT = references/presentation-style.md · executive-style.md):
  1. 캔버스        16:9 (viewBox / width / height 비율 일치)
  2. 흰 배경       첫 요소로 캔버스를 덮는 흰 rect
  3. CSS 변수      var(--*) 0건 (발표 도구가 해석 못 해 색이 빠짐)
  4. 한글 폰트     font-family에 한글 폰트 포함
  5. 폰트 하한     본문 15px 이상 (--executive면 16px)
  6. 흰 글자       밝은 배경 위 #fff 텍스트 0건 (어두운 rect 위는 정상)
  7. 액센트 바     제목 앞 세로 바(폭 4~8, 높이 28~56, rx)
  8. 박스 경계     자식 rect stroke가 부모 rect 경계와 겹침 0건 (패딩 12px+)
  9. 여백 균형     한쪽 100px+ 빈 공간 쏠림 없음
 10. 헤더/결론 띠  (--executive 전용) 어두운 띠 존재

종료 코드: 위반 0건이면 0, 있으면 1.
"""
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "{http://www.w3.org/2000/svg}"
HANGUL_FONTS = ("Pretendard", "Apple SD Gothic Neo", "Malgun Gothic",
                "Noto Sans KR", "Nanum", "Spoqa")
CANVAS_MARGIN_LIMIT = 100  # 한쪽에 이 이상 빈 공간이 몰리면 경고
BOX_PADDING_MIN = 12       # 부모-자식 rect 경계 최소 간격

# 흰 글자를 얹어도 되는 "어두운 도형"의 밝기 상한.
# 하우스 팔레트의 흰글자 띠는 레드 #BF6666(밝기 129)·골드 #B3994D(152)까지 올라가고,
# 파스텔 fill은 전부 235 이상이라 그 사이를 가르면 둘을 안전하게 구분한다.
DARK_SHAPE_MAX_LUM = 190
WHITE_TEXT_MIN_LUM = 230   # 이보다 밝은 글자색을 "흰 글자"로 본다


def parse_color(c):
    """#rgb·#rrggbb → (r,g,b). 아니면 None."""
    if not c:
        return None
    c = c.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", c)
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    """0(검정)~255(흰색) 근사 밝기."""
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b


def fnum(el, attr, default=None):
    v = el.get(attr)
    if v is None:
        return default
    try:
        return float(re.sub(r"[^0-9.\-]", "", v) or "nan")
    except ValueError:
        return default


def inherited(el, attr, ancestors):
    """자신 → 조상 순으로 속성 탐색 (SVG 상속 근사)."""
    v = el.get(attr)
    if v:
        return v
    for a in reversed(ancestors):
        v = a.get(attr)
        if v:
            return v
    return None


def collect(root):
    """(element, ancestors) 목록을 문서 순서로."""
    out = []

    def walk(node, chain):
        for child in node:
            out.append((child, list(chain)))
            walk(child, chain + [child])

    out.append((root, []))
    walk(root, [root])
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    executive = "--executive" in sys.argv
    if not args:
        print("usage: check.py <파일.svg> [--executive]")
        return 2

    path = args[0]
    raw = open(path, encoding="utf-8").read()
    root = ET.fromstring(raw)
    nodes = collect(root)
    violations = []
    notes = []

    font_min = 16 if executive else 15
    layer = "임원보고" if executive else "일반 발표"

    # --- 1. 캔버스 16:9 ---
    vb = root.get("viewBox", "")
    parts = vb.split()
    vw = vh = None
    if len(parts) == 4:
        vw, vh = float(parts[2]), float(parts[3])
        if abs(vw / vh - 16 / 9) > 0.01:
            violations.append(f"[캔버스] viewBox 비율이 16:9가 아님 ({vw}×{vh})")
    else:
        violations.append("[캔버스] viewBox 없음 또는 형식 오류")

    w, h = fnum(root, "width"), fnum(root, "height")
    if w and h and abs(w / h - 16 / 9) > 0.01:
        violations.append(f"[캔버스] width/height 비율이 16:9가 아님 ({w}×{h})")

    # --- 2. 흰 배경 사각형 ---
    rects = [(e, anc) for e, anc in nodes if e.tag == SVG_NS + "rect"]
    has_bg = any(
        (fnum(e, "x", 0) or 0) <= 0.5 and (fnum(e, "y", 0) or 0) <= 0.5
        and (fnum(e, "width", 0) or 0) >= (vw or 1280) - 1
        and (fnum(e, "height", 0) or 0) >= (vh or 720) - 1
        and (parse_color(e.get("fill")) or (0, 0, 0)) == (255, 255, 255)
        for e, _ in rects
    )
    if not has_bg:
        violations.append("[배경] 캔버스를 덮는 흰 배경 rect가 없음 (슬라이드 테마색이 비침)")

    # --- 3. CSS 변수 ---
    n_var = len(re.findall(r"var\(--", raw))
    if n_var:
        violations.append(f"[색] CSS 변수 var(--…) {n_var}건 — 16진수 하드코딩 필요")

    # --- 4. 한글 폰트 스택 ---
    fam = raw
    if not any(f in fam for f in HANGUL_FONTS):
        violations.append("[폰트] font-family에 한글 폰트(Pretendard 등) 없음 — 한글이 기본 글꼴로 떨어짐")

    # --- 5·6. 텍스트: 폰트 하한 + 흰 글자 ---
    # 흰 글자를 얹어도 되는 어두운 도형의 bbox 수집.
    # 헤더 띠는 path(위 모서리만 라운드), 번호 노드는 circle로 그리는 일이 많아 셋 다 본다.
    dark_rects = []
    for e, _ in nodes:
        c = parse_color(e.get("fill"))
        if not c or luminance(c) > DARK_SHAPE_MAX_LUM:
            continue
        if e.tag == SVG_NS + "rect":
            x, y = fnum(e, "x", 0) or 0, fnum(e, "y", 0) or 0
            dark_rects.append((x, y, x + (fnum(e, "width", 0) or 0), y + (fnum(e, "height", 0) or 0)))
        elif e.tag == SVG_NS + "path":
            coords = [float(v) for v in re.findall(r"-?\d+\.?\d*", e.get("d", ""))]
            xs, ys = coords[0::2], coords[1::2]
            if xs and ys:
                dark_rects.append((min(xs), min(ys), max(xs), max(ys)))
        elif e.tag in (SVG_NS + "circle", SVG_NS + "ellipse"):
            cx, cy = fnum(e, "cx", 0) or 0, fnum(e, "cy", 0) or 0
            rx = fnum(e, "r", None) or fnum(e, "rx", 0) or 0
            ry = fnum(e, "r", None) or fnum(e, "ry", 0) or 0
            dark_rects.append((cx - rx, cy - ry, cx + rx, cy + ry))

    def on_dark(x, y):
        return any(x0 - 2 <= x <= x1 + 2 and y0 - 6 <= y <= y1 + 6
                   for x0, y0, x1, y1 in dark_rects)

    small_fonts, white_on_light = [], []
    for e, anc in nodes:
        if e.tag not in (SVG_NS + "text", SVG_NS + "tspan"):
            continue
        content = "".join(e.itertext()).strip()
        if not content:
            continue
        fs = inherited(e, "font-size", anc)
        size = None
        if fs:
            try:
                size = float(re.sub(r"[^0-9.]", "", fs))
            except ValueError:
                size = None
        if size is not None and size < font_min:
            small_fonts.append((content[:24], size))
        fill = parse_color(inherited(e, "fill", anc))
        if fill and luminance(fill) > WHITE_TEXT_MIN_LUM:
            x = fnum(e, "x", None)
            y = fnum(e, "y", None)
            if x is None or y is None:
                for a in reversed(anc):
                    x = x if x is not None else fnum(a, "x", None)
                    y = y if y is not None else fnum(a, "y", None)
            if x is not None and y is not None and not on_dark(x, y):
                white_on_light.append((content[:24], x, y))

    if small_fonts:
        detail = ", ".join(f"'{t}'({s}px)" for t, s in small_fonts[:5])
        violations.append(
            f"[폰트] {layer} 하한 {font_min}px 미만 텍스트 {len(small_fonts)}건 — {detail}"
            + (" …" if len(small_fonts) > 5 else "")
            + "  → 폰트를 낮추지 말고 배치 재설계·통합·분할"
        )
    if white_on_light:
        detail = ", ".join(f"'{t}'@({x:.0f},{y:.0f})" for t, x, y in white_on_light[:5])
        violations.append(f"[가독성] 밝은 배경 위 흰 글자 {len(white_on_light)}건 — {detail}")

    # --- 7. 타이틀 액센트 바 ---
    has_bar = any(
        3 <= (fnum(e, "width", 0) or 0) <= 9
        and 26 <= (fnum(e, "height", 0) or 0) <= 60
        and e.get("rx") is not None
        and (fnum(e, "y", 999) or 999) < 120
        for e, _ in rects
    )
    if not has_bar:
        violations.append("[타이틀] 제목 앞 액센트 바(6×44~48·rx3) 없음")

    # --- 7b. 헤더 구분선 (헤더/본문 경계) ---
    # 없으면 본문 첫 박스가 헤더처럼 읽혀 제목 영역의 끝이 흐릿해진다.
    canvas_w = vw or 1280
    header_divider = False
    for e, _ in nodes:
        if e.tag == SVG_NS + "line":
            y1, y2 = fnum(e, "y1", None), fnum(e, "y2", None)
            x1, x2 = fnum(e, "x1", None), fnum(e, "x2", None)
            if None in (x1, x2, y1, y2):
                continue
            if abs(y1 - y2) <= 1 and 80 <= y1 <= 130 and (x2 - x1) >= canvas_w * 0.8:
                header_divider = True
        elif e.tag == SVG_NS + "rect":
            y = fnum(e, "y", None)
            bh, bw = fnum(e, "height", None), fnum(e, "width", None)
            if None in (y, bh, bw):
                continue
            if bh <= 3 and 80 <= y <= 130 and bw >= canvas_w * 0.8:
                header_divider = True
    if not header_divider:
        violations.append(
            "[헤더] 타이틀 아래 헤더 구분선 없음 — 풀폭 가로선(y≈98, #E1E4EA)으로 헤더/본문을 가를 것")

    # --- 8. 박스 경계 겹침 (부모 안 자식 rect 패딩) ---
    boxes = []
    for e, _ in rects:
        x, y = fnum(e, "x", None), fnum(e, "y", None)
        bw, bh = fnum(e, "width", None), fnum(e, "height", None)
        if None in (x, y, bw, bh) or bw <= 0 or bh <= 0:
            continue
        if bw >= (vw or 1280) - 1 and bh >= (vh or 720) - 1:
            continue  # 배경
        boxes.append((x, y, bw, bh, e))

    overlaps = []
    for cx, cy, cw, ch, ce in boxes:
        if ce.get("stroke") in (None, "none"):
            continue  # stroke 없는 자식은 경계 겹침 문제 없음
        for px, py, pw, ph, pe in boxes:
            if pe is ce:
                continue
            inside = (px - 2 <= cx and py - 2 <= cy
                      and cx + cw <= px + pw + 2 and cy + ch <= py + ph + 2)
            if not inside or (pw * ph) <= (cw * ch) * 1.2:
                continue
            pads = (cx - px, py and cy - py, (px + pw) - (cx + cw), (py + ph) - (cy + ch))
            left, top, right, bottom = cx - px, cy - py, (px + pw) - (cx + cw), (py + ph) - (cy + ch)
            # 헤더 띠 예외: 상단에 붙은 같은 폭 띠는 정상 구성
            is_header_band = top <= 2 and abs(left) <= 2 and abs(right) <= 2
            if is_header_band:
                continue
            tight = [n for n, v in (("좌", left), ("상", top), ("우", right), ("하", bottom))
                     if v < BOX_PADDING_MIN]
            if tight:
                overlaps.append((cx, cy, cw, ch, "·".join(tight)))
            break
    if overlaps:
        detail = ", ".join(f"rect({x:.0f},{y:.0f},{w:.0f}×{h:.0f}) {side} 패딩부족"
                           for x, y, w, h, side in overlaps[:5])
        violations.append(f"[박스] 부모 경계와 패딩 {BOX_PADDING_MIN}px 미만 자식 {len(overlaps)}건 — {detail}")

    # --- 9. 여백 균형 ---
    if boxes and vw and vh:
        max_bottom = max(y + bh for _, y, _, bh, _ in [(b[0], b[1], b[2], b[3], b[4]) for b in boxes])
        max_right = max(x + bw for x, _, bw, _, _ in boxes)
        if vh - max_bottom > CANVAS_MARGIN_LIMIT:
            violations.append(
                f"[여백] 하단 빈 공간 {vh - max_bottom:.0f}px (>{CANVAS_MARGIN_LIMIT}) — 콘텐츠를 펼쳐 캔버스를 채울 것")
        if vw - max_right > CANVAS_MARGIN_LIMIT + 40:
            notes.append(f"우측 빈 공간 {vw - max_right:.0f}px — 의도된 여백인지 확인")

    # --- 10. 임원: 헤더 띠 + 결론 띠 ---
    if executive:
        if not dark_rects:
            violations.append("[임원] 어두운 헤더 띠·결론 띠 없음 — 임원보고 불변 골격")
        else:
            bottom_band = any(y0 > (vh or 720) * 0.72 for _, y0, _, _ in dark_rects)
            if not bottom_band:
                violations.append("[임원] 하단 결론 띠(진남색 #3A4A6B) 없음 — 그 장의 결론을 한 줄로 못 박을 것")

    # --- 결과 ---
    print(f"■ {path}  ({layer} 레이어 · 폰트 하한 {font_min}px)")
    if violations:
        print(f"\n❌ 위반 {len(violations)}건\n")
        for v in violations:
            print(f"  - {v}")
    else:
        print("\n✅ 위반 0건 — 마감 가능")
    if notes:
        print("\n⚠️  확인 권고")
        for n in notes:
            print(f"  - {n}")
    print("\n(스크립트는 좌표만 본다 — 글자 폭·한글 렌더는 브라우저로 눈으로 확인할 것)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())

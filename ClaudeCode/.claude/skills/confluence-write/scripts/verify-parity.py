#!/usr/bin/env python3
"""로컬 마크다운 ↔ Confluence 라이브 본문 정합 검증.

사용: python verify-parity.py <local.md> <live.html>
  - live.html  = getConfluencePage(contentFormat="html")의 body 문자열을 저장한 파일
  - local.md   = 텍스트 SoT인 로컬 원본(.md)

출력:
  [매크로]  라이브 도식 파일·펼치기 제목·임베드 인벤토리 + 로컬 참조와의 누락 대조
  [본문]    포맷 마크업·매크로 식별자를 양쪽에서 제거한 뒤 토큰 단위 difflib 유사도
            (1.0000 = 단어 한 톨까지 동일). 실질 차이는 한 줄씩 출력.

원리: 매크로(도식·펼치기)는 read 시 텍스트가 비어 나오므로 '식별자(파일명·제목)'로
대조하고, 본문은 굵게/불릿/구분선 등 표현 차이를 정규화로 지운 뒤 내용만 비교한다.
"""
import re, sys, html, unicodedata, difflib

def clean(t):
    t = html.unescape(t); t = unicodedata.normalize("NFC", t)
    for a, b in [("−","-"),("–","-"),("—","-"),("→","->"),("↔","<->"),
                 ("’","'"),("‘","'"),("“",'"'),("”",'"')]:
        t = t.replace(a, b)
    return t

def live_text(live):
    s = live
    # 펼치기 전체는 매크로 콘텐츠(라이브 큐레이션) → 본문 텍스트 비교에서 제외.
    # 로컬은 펼치기를 한 줄 placeholder로 대표하므로 내부 텍스트는 인벤토리로만 검증.
    s = re.sub(r'<details\b.*?</details>', '', s, flags=re.S)
    s = re.sub(r'<figcaption>.*?</figcaption>', '', s, flags=re.S)  # 도식 캡션
    s = re.sub(r'<div[^>]*data-media-type[^>]*>.*?</div>', '', s, flags=re.S)  # 도식 파일명
    s = re.sub(r'<iframe.*?</iframe>', '', s, flags=re.S)
    s = re.sub(r'^\s*<h2>제목.*?</h2>', '', s, flags=re.S)          # 선두 제목 라인
    s = re.sub(r'<[^>]+>', ' ', s)
    return clean(s)

def local_text(loc):
    # 본문만: 첫 본문 헤딩부터. 매크로 placeholder/도식 라벨/동기화 노트 줄 제외.
    m = re.search(r'^##\s', loc, flags=re.M)
    body = loc[m.start():] if m else loc
    keep = []
    for ln in body.splitlines():
        s = ln.strip()
        if s.startswith("> 📂") or "🔗" in s or s.startswith("*(도식") or s.startswith("🎨"):
            continue
        keep.append(ln)
    t = clean("\n".join(keep))
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)  # md 링크 → 표시 텍스트

def toks(t):
    t = re.sub(r'[*`#|>]', ' ', t)
    t = t.replace('-', ' ').replace('=', ' ')          # 불릿·구분선·강조 잔재 무시
    return [w for w in re.split(r'\s+', t) if w and w != '---']

def main(local_path, live_path):
    loc = open(local_path, encoding="utf-8").read()
    live = open(live_path, encoding="utf-8").read()

    # --- 매크로 인벤토리 ---
    live_figs = re.findall(r'>\s*([\w\-]+\.(?:svg|png|mp4))\s*<', live)
    live_exp  = [x.strip() for x in re.findall(r'<summary>(.*?)</summary>', live, flags=re.S)]
    live_emb  = sorted(set(re.findall(r'/wiki/x/(\w+)', live)))
    loc_figs  = set(re.findall(r'([\w\-]+\.(?:svg|png|mp4))', loc))
    print("=== 매크로 인벤토리 ===")
    print(f"[도식] live={len(live_figs)}  local참조={len(loc_figs)}")
    print("  로컬엔 있고 라이브에 없음:", sorted(loc_figs - set(live_figs)) or "없음")
    print("  라이브엔 있고 로컬에 없음:", sorted(set(live_figs) - loc_figs) or "없음")
    print(f"[펼치기] live={len(live_exp)}:")
    for x in live_exp: print("    -", x)
    print(f"[임베드] live={live_emb}")

    # --- 본문 토큰 diff ---
    A, B = toks(local_text(loc)), toks(live_text(live))
    sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
    diffs = [(tag, " ".join(A[i1:i2]), " ".join(B[j1:j2]))
             for tag, i1, i2, j1, j2 in sm.get_opcodes()
             if tag != "equal" and (A[i1:i2] or B[j1:j2])]
    print(f"\n=== 본문 텍스트 ===\n로컬토큰={len(A)} 라이브토큰={len(B)}  유사도={sm.ratio():.4f}")
    print("실질 차이:", len(diffs), "건")
    for t, L, R in diffs:
        print(f"  - [{t}] L:{L[:90]!r}  R:{R[:90]!r}")
    return 0 if not diffs and not (loc_figs - set(live_figs)) else 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))

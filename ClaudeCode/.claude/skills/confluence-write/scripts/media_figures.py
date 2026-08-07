#!/usr/bin/env python3
"""Confluence media 헬퍼 — 첨부 업로드 후 본문 재구성을 돕는다.

두 하위 명령:
  extract  게시된 페이지 body(html)에서 각 첨부의 (data-id, data-collection, filename)을
           문서 순서대로 뽑아 JSON으로 출력. 브라우저 업로드→게시 후 getConfluencePage
           결과를 여기에 물려 data-id를 회수한다.
  build    (data-id, filename) 목록을 media-single figure HTML로 조립. 폭·정렬 지정 가능.
           figure가 많을 때 손으로 쓰다 UUID를 훼손하는 사고를 막는다.

사용:
  # 1) 게시된 body에서 media 목록 회수 (stdin 또는 --in)
  python media_figures.py extract --in body.html            # → media.json
  getConfluencePage ... | python media_figures.py extract    # stdin도 가능

  # 2) 회수한 목록으로 figure HTML 생성 (원하는 폭으로)
  python media_figures.py build --in media.json --width 760  # → figures.html

data-id·data-collection은 실제 첨부를 가리키는 불변 식별자다. extract가 뽑은 값을
build가 그대로 되돌려 쓰므로 왕복이 안전하다. 절대 손으로 바꾸지 않는다.
"""
import argparse
import html
import json
import re
import sys

# <div data-type="media" ...>filename</div> 블록 단위로 파싱한다.
MEDIA_DIV = re.compile(r'<div\b[^>]*\bdata-type="media"[^>]*>(.*?)</div>', re.S)
ATTR = lambda name, s: (re.search(r'\b' + name + r'="([^"]*)"', s) or [None, None])[1]


def read_input(path):
    return open(path, encoding="utf-8").read() if path else sys.stdin.read()


def extract(args):
    text = read_input(args.infile)
    items = []
    for m in MEDIA_DIV.finditer(text):
        block = m.group(0)
        inner = m.group(1)
        items.append({
            "id": ATTR("data-id", block),
            "collection": ATTR("data-collection", block),
            "name": html.unescape(re.sub(r"<[^>]+>", "", inner)).strip(),
            "width": ATTR("data-width", block),
            "height": ATTR("data-height", block),
        })
    # 대량 업로드는 편집기가 파일을 비동기 삽입해 문서 순서가 뒤섞이거나 일부가 누락된다.
    # 파일명에 0-패딩 순번 접두사(01-,02-…)를 붙였다면 name 기준 정렬로 순서를 복원한다.
    if args.sort_name:
        items.sort(key=lambda x: (x.get("name") or ""))
    out = json.dumps(items, ensure_ascii=False, indent=2)
    print(out)
    print(f"[extract] {len(items)} media 노드 회수", file=sys.stderr)
    # 완결·중복 점검 — 누락(게시 전 드롭)·중복(재업로드)을 조기 발견한다.
    names = [it.get("name") for it in items]
    dups = sorted({n for n in names if n and names.count(n) > 1})
    if dups:
        print(f"[extract] ⚠ 중복 파일명 {len(dups)}건: {', '.join(dups)}", file=sys.stderr)
    if args.expect is not None and len(items) != args.expect:
        print(f"[extract] ⚠ 기대 {args.expect}개와 불일치({len(items)}개) — 누락분 재업로드 필요",
              file=sys.stderr)


FIG = ('<figure data-type="media-single" data-layout="{layout}" '
       'data-width="{width}" data-width-type="pixel">'
       '<div data-type="media" data-media-type="file" data-id="{id}" '
       'data-collection="{collection}" data-width="{iw}" data-height="{ih}">{name}</div></figure>')


def build(args):
    items = json.loads(read_input(args.infile))
    figs = []
    for it in items:
        if not it.get("id") or not it.get("collection"):
            print(f"[build] 경고: id/collection 없는 항목 건너뜀 → {it.get('name')}", file=sys.stderr)
            continue
        figs.append(FIG.format(
            layout=args.layout, width=args.width,
            id=it["id"], collection=it["collection"],
            iw=it.get("width") or 1280, ih=it.get("height") or 720,
            name=html.escape(it.get("name", ""))))
    print("".join(figs))
    print(f"[build] {len(figs)} figure 생성 (width={args.width}, layout={args.layout})", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description="Confluence media figure 헬퍼")
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("extract", help="body html에서 media (id,name) 회수")
    pe.add_argument("--in", dest="infile", help="입력 파일(없으면 stdin)")
    pe.add_argument("--sort-name", action="store_true",
                    help="문서 순서 대신 name(파일명) 기준 정렬 — 대량 업로드는 삽입 순서가 "
                         "뒤섞이므로 0-패딩 순번 접두사 파일명으로 정렬 회수")
    pe.add_argument("--expect", type=int, default=None,
                    help="기대 미디어 개수 — 불일치 시 stderr 경고(누락 조기 발견)")
    pe.set_defaults(func=extract)

    pb = sub.add_parser("build", help="media 목록 → figure html")
    pb.add_argument("--in", dest="infile", help="media.json(없으면 stdin)")
    pb.add_argument("--width", type=int, default=760, help="figure 표시 폭 px (기본 760)")
    pb.add_argument("--layout", default="center",
                    choices=["center", "wide", "full-width", "align-start", "align-end"],
                    help="figure 정렬 (기본 center)")
    pb.set_defaults(func=build)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

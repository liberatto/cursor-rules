#!/usr/bin/env python3
"""로컬 마크다운 → Confluence 본문(HTML+ / ADF) 변환기.

`updateConfluencePage(contentFormat:"html")`에 그대로 실을 수 있는 HTML을 만든다.
노드가 수십 개인 원고를 손으로 조립하면 UUID·속성이 훼손되므로 이 스크립트를 쓴다
(authoring.md Part A 2단계). 게시 **전** 단계이며, 게시 **후** 라이브 대조는
verify-parity.py가 맡는다 — 둘은 겹치지 않는다.

사용:
  python md2confluence.py <원고.md> -o body.html --page-id <페이지id> \
         --file-ids <fileids.json>
  python md2confluence.py <원고.md> -o body.adf.json --page-id <id> --format adf

  --file-ids = {"FIG-01-….svg": "<fileId>", …}. 도식이 있으면 필수이며, 매핑에 없는
  도식을 만나면 중단한다. fileId 회수는 authoring.md Part B 5단계 참조.

손실 게이트(항상 실행): 원고의 불릿(`- `)·`<br>` 개수가 생성 결과의 listItem·hardBreak
개수와 일치해야 한다. 불일치면 파일을 쓰지 않고 중단한다 — 중첩 목록과 굵은 글씨 안
`<br>`에서 실제로 유실 버그가 났던 자리다.

하우스 규약(SKILL.md §표기 규약·authoring.md):
  panel   `### Executive Summary`=success · `> **ReAct**`=note (--no-panel-promote로 해제)
  expand  `### [참고] …` 절을 통째로 펼치기로, 제목에 `📂 ` 접두
  table   attrs.width = --table-width (기본 900, 도식과 좌우 경계 정렬)
  media   mediaSingle{layout:center, widthType:pixel} + media div 안에 파일명 수록
  제외    문서 제목(`# `) · 메타 blockquote(목적·보고 대상·버전) · 구분선(`---`)
"""
import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from media_figures import FIG  # figure HTML 템플릿은 한 곳에서만 정의한다

TOKEN = re.compile(r"\*\*(.+?)\*\*|`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|(<br>)")


def strip_frontmatter(md):
    return md.split("---\n", 2)[2] if md.startswith("---\n") else md


# --- 마크다운 → ADF ---------------------------------------------------------

def inline(s):
    """마크다운 인라인 → ADF inline 노드 목록."""
    nodes, pos = [], 0

    def push(text, marks=None):
        if text:
            n = {"type": "text", "text": text}
            if marks:
                n["marks"] = marks
            nodes.append(n)

    for m in TOKEN.finditer(s):
        push(s[pos:m.start()])
        bold, code, ltext, lhref, br = m.groups()
        if bold is not None:
            # 굵은 글씨 안에도 <br>·`code`가 들어갈 수 있어 재귀 처리한다.
            for n in inline(bold):
                if n["type"] == "text":
                    n.setdefault("marks", []).append({"type": "strong"})
                nodes.append(n)
        elif code is not None:
            push(code, [{"type": "code"}])
        elif ltext is not None:
            push(ltext, [{"type": "link", "attrs": {"href": lhref}}])
        elif br is not None:
            nodes.append({"type": "hardBreak"})
        pos = m.end()
    push(s[pos:])
    return nodes or [{"type": "text", "text": " "}]


def para(s):
    return {"type": "paragraph", "content": inline(s)}


def build_table(rows, width):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]
    out = [{"type": "tableRow", "content": [
        {"type": "tableHeader", "attrs": {"colspan": 1, "rowspan": 1}, "content": [para(c)]}
        for c in head]}]
    for row in body:
        out.append({"type": "tableRow", "content": [
            {"type": "tableCell", "attrs": {"colspan": 1, "rowspan": 1}, "content": [para(c)]}
            for c in row]})
    return {"type": "table", "attrs": {"layout": "default", "width": width}, "content": out}


def build_list(items):
    """(들여쓰기, 텍스트) → 중첩 bulletList. 입력 1건 = listItem 1건을 보장한다."""
    root = {"type": "bulletList", "content": []}
    lists = {0: root}                      # 레벨 → 그 레벨의 bulletList
    for ind, text in items:
        lvl = ind // 2
        target = None
        if lvl > 0:
            parent = lists.get(lvl - 1)
            if parent and parent["content"]:
                item = parent["content"][-1]
                sub = next((c for c in item["content"] if c["type"] == "bulletList"), None)
                if sub is None:
                    sub = {"type": "bulletList", "content": []}
                    item["content"].append(sub)
                target = sub
        if target is None:                 # 부모가 없으면 최상위로 승격
            lvl, target = 0, root
        lists[lvl] = target
        for k in [k for k in lists if k > lvl]:
            del lists[k]
        target["content"].append({"type": "listItem", "content": [para(text)]})
    return root


def convert(md, opt):
    body = strip_frontmatter(md)
    lines = body.split("\n")
    doc, expand = [], None
    stats = {"heading": 0, "table": 0, "mediaSingle": 0, "expand": 0,
             "panel": 0, "blockquote": 0, "bulletList": 0}
    pend_list, pend_table = [], []
    i, seen_meta = 0, False

    def sink():
        return expand["content"] if expand is not None else doc

    def flush():
        nonlocal pend_list, pend_table
        if pend_list:
            sink().append(build_list(pend_list))
            stats["bulletList"] += 1
            pend_list = []
        if pend_table:
            sink().append(build_table(pend_table, opt.table_width))
            stats["table"] += 1
            pend_table = []

    def close_expand():
        nonlocal expand
        if expand is not None:
            doc.append(expand)
            expand = None

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if s.startswith("|"):
            pend_table.append(s)
            i += 1
            continue
        if pend_table:
            flush()

        m = re.match(r"^(\s*)- (.+)$", ln)
        if m:
            pend_list.append((len(m.group(1)), m.group(2)))
            i += 1
            continue
        if pend_list:
            flush()

        if not s or s == "---" or s.startswith("# "):
            i += 1
            continue

        m = re.match(r"^!\[[^\]]*\]\((?:figures/)?([^)]+)\)$", s)
        if m:
            name = m.group(1)
            if name not in opt.file_ids:
                sys.exit(f"[중단] 미매핑 도식: {name} — --file-ids에 추가할 것")
            sink().append({
                "type": "mediaSingle",
                "attrs": {"layout": "center", "width": 900, "widthType": "pixel"},
                "content": [{"type": "media", "attrs": {
                    "id": opt.file_ids[name], "type": "file", "collection": opt.collection,
                    "alt": name, "width": 1280, "height": 720}}]})
            stats["mediaSingle"] += 1
            i += 1
            continue

        if opt.panel_promote and s == "### Executive Summary":
            close_expand()
            inner = [{"type": "heading", "attrs": {"level": 2},
                      "content": [{"type": "text", "text": "Executive Summary"}]}]
            i += 1
            bullets = []
            while i < len(lines) and not lines[i].startswith("---"):
                t = lines[i].strip()
                if t.startswith("- "):
                    # 라이브 게시본 관행: 불릿과 중복되는 선행 체크 문자 제거
                    bullets.append((0, re.sub(r"^√\s*", "", t[2:])))
                elif t:
                    if bullets:                     # 문단이 다시 나오면 목록을 닫는다
                        inner.append(build_list(bullets))
                        bullets = []
                    inner.append(para(t))
                i += 1
            if bullets:
                inner.append(build_list(bullets))
            doc.append({"type": "panel", "attrs": {"panelType": "success"}, "content": inner})
            stats["panel"] += 1
            stats["heading"] += 1
            continue

        if s.startswith("### [참고]"):
            close_expand()
            expand = {"type": "expand", "attrs": {"title": "📂 " + s[4:].strip()},
                      "content": []}
            stats["expand"] += 1
            i += 1
            while i < len(lines) and (not lines[i].strip() or
                                      lines[i].strip().startswith("> Confluence 펼치기")):
                i += 1
            continue

        if s.startswith("### ") or s.startswith("## "):
            close_expand()
            lvl = 3 if s.startswith("### ") else 2
            doc.append({"type": "heading", "attrs": {"level": lvl},
                        "content": inline(s[lvl + 1:])})
            stats["heading"] += 1
            i += 1
            continue

        if s.startswith("> "):
            text = s[2:]
            if text.startswith(("**목적**", "**보고 대상**", "**버전**")):
                seen_meta = True
                i += 1
                continue
            if opt.panel_promote and text.startswith("**ReAct**"):
                sink().append({"type": "panel", "attrs": {"panelType": "note"},
                               "content": [para(text)]})
                stats["panel"] += 1
            else:
                sink().append({"type": "blockquote", "content": [para(text)]})
                stats["blockquote"] += 1
            i += 1
            continue

        sink().append(para(s))
        i += 1

    flush()
    close_expand()
    if opt.meta_gate and not seen_meta:
        sys.exit("[중단] 메타 blockquote 미발견 — 구조 가정 불일치 "
                 "(메타가 없는 원고면 --no-meta-gate)")
    return {"version": 1, "type": "doc", "content": doc}, stats


# --- ADF → Confluence HTML+ -------------------------------------------------

def esc(t):
    return html.escape(t, quote=False).replace('"', "&#34;").replace("'", "&#39;")


def inline_html(nodes):
    out = []
    for n in nodes:
        if n["type"] == "hardBreak":
            out.append("<br />")
            continue
        t = esc(n.get("text", ""))
        for mk in n.get("marks", []):
            if mk["type"] == "strong":
                t = f"<strong>{t}</strong>"
            elif mk["type"] == "code":
                t = f"<code>{t}</code>"
            elif mk["type"] == "link":
                t = f'<a href="{mk["attrs"]["href"]}">{t}</a>'
        out.append(t)
    return "".join(out)


def block(n):
    ty = n["type"]
    if ty == "paragraph":
        return f"<p>{inline_html(n.get('content', []))}</p>"
    if ty == "heading":
        lv = n["attrs"]["level"]
        return f"<h{lv}>{inline_html(n.get('content', []))}</h{lv}>"
    if ty == "bulletList":
        return "<ul>" + "".join(block(c) for c in n["content"]) + "</ul>"
    if ty == "listItem":
        return "<li>" + "".join(block(c) for c in n["content"]) + "</li>"
    if ty == "blockquote":
        return "<blockquote>" + "".join(block(c) for c in n["content"]) + "</blockquote>"
    if ty == "panel":
        return (f'<div data-type="panel-{n["attrs"]["panelType"]}">'
                + "".join(block(c) for c in n["content"]) + "</div>")
    if ty == "expand":
        return (f'<details><summary>{esc(n["attrs"]["title"])}</summary>'
                + "".join(block(c) for c in n["content"]) + "</details>")
    if ty == "table":
        return (f'<table data-layout="{n["attrs"]["layout"]}" data-width="{n["attrs"]["width"]}"><tbody>'
                + "".join(block(c) for c in n["content"]) + "</tbody></table>")
    if ty == "tableRow":
        return "<tr>" + "".join(block(c) for c in n["content"]) + "</tr>"
    if ty in ("tableHeader", "tableCell"):
        tag = "th" if ty == "tableHeader" else "td"
        return f"<{tag}>" + "".join(block(c) for c in n["content"]) + f"</{tag}>"
    if ty == "mediaSingle":
        # media div 안 파일명이 없으면 다음 회차 media_figures.py extract가 매핑을
        # 못 하고 verify-parity.py의 도식 인벤토리 대조도 성립하지 않는다.
        a, m = n["attrs"], n["content"][0]["attrs"]
        return FIG.format(layout=a["layout"], width=a["width"], id=m["id"],
                          collection=m["collection"], iw=m["width"], ih=m["height"],
                          name=esc(m.get("alt", "")))
    sys.exit(f"[중단] 미지원 노드: {ty}")


def to_html(adf):
    return "\n".join(block(c) for c in adf["content"])


# --- 손실 게이트 ------------------------------------------------------------

def loss_gate(src, adf):
    """원고의 불릿·<br> 개수가 생성 결과에 그대로 나타나는지 확인한다."""
    body = strip_frontmatter(src)
    got = {}

    def walk(n):
        got[n["type"]] = got.get(n["type"], 0) + 1
        for x in n.get("content", []):
            walk(x)
    walk(adf)

    checks = [("listItem", len(re.findall(r"(?m)^\s*- ", body)), got.get("listItem", 0)),
              ("hardBreak", body.count("<br>"), got.get("hardBreak", 0))]
    for name, want, have in checks:
        print(f"  {name}: 기대 {want} / 생성 {have} {'OK' if want == have else '불일치'}",
              file=sys.stderr)
    if [c for c in checks if c[1] != c[2]]:
        sys.exit("[중단] 손실 게이트 실패")


def main():
    p = argparse.ArgumentParser(
        description="로컬 마크다운 → Confluence 본문(HTML+ / ADF)",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("source", help="원고 .md")
    p.add_argument("-o", "--out", required=True, help="출력 파일")
    p.add_argument("--page-id", required=True,
                   help="대상 페이지 id — media collection(contentId-<id>)에 쓰인다. "
                        "다른 페이지 값을 쓰면 남의 첨부를 가리켜 이미지가 전멸한다")
    p.add_argument("--file-ids", help="{파일명: fileId} JSON — 도식이 있으면 필수")
    p.add_argument("--format", choices=["html", "adf"], default="html",
                   help="출력 형식 (기본 html — updateConfluencePage용)")
    p.add_argument("--table-width", type=int, default=900,
                   help="표 폭 px (기본 900 — 도식과 좌우 경계 정렬)")
    p.add_argument("--no-panel-promote", dest="panel_promote", action="store_false",
                   help="Executive Summary·ReAct 패널 승격 해제(일반 헤딩·인용으로 처리)")
    p.add_argument("--no-meta-gate", dest="meta_gate", action="store_false",
                   help="메타 blockquote 미발견 시 중단하지 않음")
    opt = p.parse_args()

    opt.collection = f"contentId-{opt.page_id}"
    opt.file_ids = json.load(open(opt.file_ids, encoding="utf-8")) if opt.file_ids else {}

    src = open(opt.source, encoding="utf-8").read()
    adf, stats = convert(src, opt)
    loss_gate(src, adf)

    with open(opt.out, "w", encoding="utf-8") as f:
        if opt.format == "adf":
            json.dump(adf, f, ensure_ascii=False)
        else:
            f.write(to_html(adf))
    print(f"[{opt.format}] {opt.out} — {stats}", file=sys.stderr)


if __name__ == "__main__":
    main()

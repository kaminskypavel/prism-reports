#!/usr/bin/env python3
"""Build <reports_dir>/index.html (Daylight style) and give every report a back link to it.

Usage:
  python3 ~/.claude/templates/reports-index.py <reports_dir> [--topics topics.json] [--title Designs] [--fixed]
  python3 ~/.claude/templates/reports-index.py <docs_dir> --hub

--title names the index and its back links (default "Reports": "All reports").
--hub builds <dir>/index.html as a hub instead: one tile per index this script built below <dir>
(up to 3 levels down), with its item count and latest date. Once a hub exists, every normal run
below it adds an "All <hub folder>" link to the index it builds and refreshes the hub.
--fixed pins the back link to a corner instead of placing it in the page flow
(bottom-left corner, so it clears the mockup's own header) for design mockups and prototypes
whose own layout must not shift. Pages built from a prism template (a .wrap column with a .cta)
always get the link first in their content column instead, so it lines up with the page.

Reports are <dir>/*.html and <dir>/*/index.html (one level down). For each report:
  title  <title>, else the first <h1>
  date   <meta name="report-date" content="YYYY-MM-DD HH:MM">, else the YYYY-MM-DD prefix of the file or
         folder name plus the time the file or folder was created (when that is the same day). The result
         is written back as the meta tag, so the order survives a git checkout.
  topic  <meta name="report-topic" content="...">, else "Unsorted"
A report with <meta name="report-index" content="skip"> is left out.
--topics takes {"<file path relative to reports_dir>": "<topic>"} and writes the meta tag into
reports that lack one (a one-time retrofit). Every report without a link of class
"report-back" gets one as the first element of <body>. The index lists reports oldest first.
Safe to rerun after every new report.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

FLOW = "display:inline-block;margin:16px 0 0 16px;"
COLUMN = "display:inline-block;margin:0 0 18px;"
FIXED = "position:fixed;bottom:12px;left:12px;z-index:2147483647;opacity:.92;"
BACK = (
    '<a class="report-back" dir="ltr" href="{href}" target="_blank" rel="noopener" style="{place}'
    "padding:6px 14px;border-radius:999px;background:#141414;color:#fff;text-decoration:none;"
    'font:600 13px/1.4 -apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,sans-serif">&larr; All {label}</a>'
)
HUB = "reports-hub"
MARK = "built by ~/.claude/templates/reports-index.py"
GRADIENTS = [("#6366f1", "#4338ca"), ("#14b8a6", "#0f766e"), ("#3b82f6", "#1e3a8a"), ("#f59e0b", "#b45309"), ("#f97316", "#c2410c"), ("#ec4899", "#be185d")]
TOPIC_COLORS = ["#0f766e", "#7c3aed", "#b45309", "#be185d", "#2563eb", "#c2410c", "#0e7490", "#525252"]


def meta(src: str, name: str) -> str | None:
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', src, re.I) or re.search(
        rf'<meta\s+content="([^"]*)"\s+name="{name}"', src, re.I
    )
    return html.unescape(m.group(1)) if m else None


def set_head_meta(src: str, name: str, value: str) -> str:
    """Replace the meta tag's content, or add the tag to <head>."""
    pat = re.compile(rf'(<meta\s+name="{name}"\s+content=")[^"]*(")|(<meta\s+content=")[^"]*("\s+name="{name}")', re.I)
    m = pat.search(src)
    if not m:
        return add_head_meta(src, name, value)
    v = html.escape(value, quote=True)
    new = f"{m.group(1)}{v}{m.group(2)}" if m.group(1) else f"{m.group(3)}{v}{m.group(4)}"
    return src[: m.start()] + new + src[m.end() :]


def created(path: Path) -> datetime:
    st = path.stat()
    return datetime.fromtimestamp(getattr(st, "st_birthtime", st.st_mtime))


def report_date(src: str, rel: str, f: Path, root: Path) -> str:
    """YYYY-MM-DD HH:MM when known, else YYYY-MM-DD."""
    d = meta(src, "report-date") or ""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", d):
        return d
    day = d[:10] if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d[:10]) else (re.match(r"(\d{4}-\d{2}-\d{2})", rel) or [None, ""])[1]
    born = created(root / rel.split("/")[0] if "/" in rel else f)
    if not day:
        return born.strftime("%Y-%m-%d %H:%M")
    return born.strftime("%Y-%m-%d %H:%M") if born.strftime("%Y-%m-%d") == day else day


def add_head_meta(src: str, name: str, value: str) -> str:
    tag = f'<meta name="{name}" content="{html.escape(value, quote=True)}">'
    m = re.search(r"<head[^>]*>", src, re.I)
    return src[: m.end()] + "\n" + tag + src[m.end() :] if m else tag + src


def find_hub(root: Path) -> Path | None:
    """Nearest folder above root, up to the git root, whose index.html is a hub built with --hub."""
    for d in root.parents:
        f = d / "index.html"
        if f.is_file() and meta(f.read_text(errors="ignore"), HUB):
            return d
        if (d / ".git").exists():
            return None
    return None


def build_hub(hub: Path) -> None:
    """<hub>/index.html: one tile per index this script built below hub, up to 3 levels down."""
    E = html.escape
    tiles = []
    for f in sorted(p for pat in ("*/index.html", "*/*/index.html", "*/*/*/index.html") for p in hub.glob(pat)):
        src = f.read_text(errors="ignore")
        if MARK not in src:
            continue
        rel = f.parent.relative_to(hub).as_posix()
        n = re.search(r'<span class="badge">(\d+)</span>', src)
        latest = re.search(r"latest ([^·<]*?) ·", src)
        a, b = GRADIENTS[len(tiles) % len(GRADIENTS)]
        tiles.append(
            f'<a class="tile" style="background:linear-gradient(180deg,{a},{b})" href="{E(rel)}/index.html" target="_blank" rel="noopener">'
            f'<span class="v">{E(rel.replace("/", " / ").capitalize())}</span>'
            f'<small>{n.group(1) if n else "?"} item{"" if n and n.group(1) == "1" else "s"} · latest {E(latest.group(1).strip()) if latest else "?"}</small></a>'
        )
    title = hub.name.capitalize()
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="{HUB}" content="1"><title>{E(title)}</title><style>
body{{margin:0;background:#e8e8e4;color:#141414;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-variant-numeric:tabular-nums}}
.wrap{{max-width:1100px;margin:0 auto;padding:40px 32px 80px}}
h1{{font-size:40px;letter-spacing:-.025em;margin:0;line-height:1.1;display:flex;align-items:center;gap:14px}}
.badge{{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:#141414;color:#fff}}
.sub{{color:#55554f;font-size:14px;margin:6px 0 22px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}}
.tile{{min-height:140px;border-radius:12px;padding:14px;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.06)}}
.tile .v{{font-size:26px;font-weight:800;letter-spacing:-.02em;line-height:1.1}}.tile small{{font-size:12.5px;font-weight:500;opacity:.92}}
</style></head><body><div class="wrap">
<h1>{E(title)} <span class="badge">{len(tiles)} indexes</span></h1>
<p class="sub">Every report index in this folder · {MARK} --hub</p>
<div class="tiles">{"".join(tiles)}</div>
</div></body></html>"""
    (hub / "index.html").write_text(page)
    print(f"{hub / 'index.html'}: hub of {len(tiles)} indexes")


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    if "--hub" in sys.argv:
        build_hub(root)
        return
    if (root / "index.html").is_file() and meta((root / "index.html").read_text(errors="ignore"), HUB):
        sys.exit(f"{root / 'index.html'} is a hub: rebuild it with --hub")
    index_title = sys.argv[sys.argv.index("--title") + 1] if "--title" in sys.argv else "Reports"
    place = FIXED if "--fixed" in sys.argv else FLOW
    topics = {}
    if "--topics" in sys.argv:
        topics = json.loads(Path(sys.argv[sys.argv.index("--topics") + 1]).read_text())
    files = sorted(p for p in root.glob("*.html") if p.name != "index.html") + sorted(root.glob("*/index.html"))
    rows = []
    for f in files:
        rel = f.relative_to(root).as_posix()
        src = f.read_text(errors="ignore")
        if meta(src, "report-index") == "skip":
            continue
        changed = False
        if rel in topics and not meta(src, "report-topic"):
            src = add_head_meta(src, "report-topic", topics[rel])
            changed = True
        href = "../index.html" if "/" in rel else "index.html"
        link = BACK.format(href=href, place=place, label=html.escape(index_title.lower()))
        old = re.search(r'<a\s[^>]*class="report-back"[^>]*>.*?</a>', src, re.S)
        wrap = re.search(r'<div\s+class="wrap"[^>]*>', src) if 'class="cta"' in src else None
        if wrap:
            # A prism page: the link sits first in the content column, so it lines up with the page like the index's own link.
            # An existing link keeps its look (Midnight's is white) and only moves.
            link = (old.group(0) if old and f'href="{href}"' in old.group(0) else BACK.format(href=href, place=COLUMN, label=html.escape(index_title.lower())))
            link = link.replace(FLOW, COLUMN).replace(FIXED, COLUMN)
            if not re.search(r'<div\s+class="wrap"[^>]*>\s*' + re.escape(link), src):
                if old:
                    src = src[: old.start()] + src[old.end() :].removeprefix("\n")
                wrap = re.search(r'<div\s+class="wrap"[^>]*>', src)
                src = src[: wrap.end()] + "\n  " + link + src[wrap.end() :]
                changed = True
        elif old and f'href="{href}"' not in old.group(0):
            src = src[: old.start()] + link + src[old.end() :]
            changed = True
        elif not old:
            body = re.search(r"<body[^>]*>", src, re.I)
            if body:
                src = src[: body.end()] + link + src[body.end() :]
                changed = True
        d = report_date(src, rel, f, root)
        if meta(src, "report-date") != d:
            src = set_head_meta(src, "report-date", d)
            changed = True
        if changed:
            f.write_text(src)
        t = re.search(r"<title>(.*?)</title>", src, re.S | re.I) or re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S | re.I)
        title = html.unescape(re.sub(r"<[^>]+>|\s+", " ", t.group(1))).strip() if t else f.stem
        rows.append({"href": rel, "title": title, "date": d, "topic": meta(src, "report-topic") or "Unsorted"})

    rows.sort(key=lambda r: (r["date"], r["title"]))
    names = sorted({r["topic"] for r in rows}, key=lambda t: (-sum(r["topic"] == t for r in rows), t))
    color = {t: TOPIC_COLORS[i % len(TOPIC_COLORS)] for i, t in enumerate(names)}
    E = html.escape
    pills = '<button class="on" data-t="">All <b>{}</b></button>'.format(len(rows)) + "".join(
        f'<button data-t="{E(t)}"><i style="background:{color[t]}"></i>{E(t)} <b>{sum(r["topic"] == t for r in rows)}</b></button>' for t in names
    )
    trs = "".join(
        f'<tr data-t="{E(r["topic"])}"><td class="d">{E(r["date"])}</td><td dir="auto"><a href="{E(r["href"])}" target="_blank" rel="noopener">{E(r["title"])}</a></td>'
        f'<td><span class="tp" style="background:{color[r["topic"]]}">{E(r["topic"])}</span></td></tr>'
        for r in rows
    )
    newest = rows[-1]["date"] if rows else ""
    hub = find_hub(root)
    up = BACK.format(href=os.path.relpath(hub / "index.html", root), place="display:inline-block;margin:0 0 14px;", label=E(hub.name.lower())) if hub else ""
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(index_title)}</title><style>
body{{margin:0;background:#e8e8e4;color:#141414;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-variant-numeric:tabular-nums}}
.wrap{{max-width:1100px;margin:0 auto;padding:40px 32px 80px}}
h1{{font-size:40px;letter-spacing:-.025em;margin:0;line-height:1.1;display:flex;align-items:center;gap:14px}}
.badge{{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:#141414;color:#fff}}
.sub{{color:#55554f;font-size:14px;margin:6px 0 22px}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}}
.pills button{{border:0;cursor:pointer;font:600 13.5px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:7px 14px;border-radius:999px;background:#f7f7f4;color:#141414}}
.pills button.on{{background:#141414;color:#fff}}.pills i{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px}}.pills b{{opacity:.6;margin-left:4px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.06)}}
th,td{{text-align:left;padding:11px 14px;border-bottom:1px solid #cfcfc9;vertical-align:middle}}tr:last-child td{{border-bottom:0}}
th{{font-size:12px;color:#55554f;text-transform:uppercase;letter-spacing:.05em}}td.d{{color:#55554f;white-space:nowrap;width:150px}}
td a{{color:#141414;font-weight:600;text-decoration:none}}td a:hover{{color:#2440e8}}tr:hover td{{background:#f7f7f4}}
.tp{{display:inline-block;color:#fff;font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px;white-space:nowrap}}
</style></head><body><div class="wrap">{up}
<h1>{E(index_title)} <span class="badge">{len(rows)}</span></h1>
<p class="sub">Oldest first · latest {E(newest)} · {MARK}</p>
<div class="pills">{pills}</div>
<table><tr><th>Date</th><th>Report</th><th>Topic</th></tr>{trs}</table>
</div><script>
document.querySelectorAll(".pills button").forEach(b=>b.onclick=()=>{{
document.querySelectorAll(".pills button").forEach(x=>x.classList.toggle("on",x===b));
document.querySelectorAll("tr[data-t]").forEach(r=>r.hidden=!!b.dataset.t&&r.dataset.t!==b.dataset.t)}});
</script></body></html>"""
    (root / "index.html").write_text(page)
    print(f"{root / 'index.html'}: {len(rows)} reports, {len(names)} topics")
    if hub:
        build_hub(hub)


if __name__ == "__main__":
    main()

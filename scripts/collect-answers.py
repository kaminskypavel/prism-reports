#!/usr/bin/env python3
"""Serve a decision page on localhost, open it in the browser, and wait for its answers.

The page sees the server (GET /__prism) and turns Copy results into Send results: one click posts the answers here
and closes the tab. The answers print to stdout and the server exits, so an agent that runs this as a background
command gets them the moment the user sends, with no copy and paste. Only the page's folder is served, on 127.0.0.1.
Images pasted into the page's notes come as JSON; they are saved to a temp folder (they are input, not part of the page)
and each "[image: paste-1.png]" in the answers becomes its full path, so the agent can open it. A pasted TIFF or HEIC
is converted to PNG on paste (POST /__prism/png, macOS sips), so its thumbnail shows in any browser.

Usage: python3 collect-answers.py <page.html> [--timeout SECONDS] [--no-open]
"""
import argparse
import base64
import http.server
import json
import shutil
import subprocess
import pathlib
import sys
import tempfile
import threading
import time
import urllib.parse
import webbrowser

ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
ap.add_argument("page")
ap.add_argument("--timeout", type=float, default=4 * 3600, help="give up after this many seconds (default 4 hours)")
ap.add_argument("--no-open", action="store_true", help="print the URL only, do not open a browser")
args = ap.parse_args()
page = pathlib.Path(args.page).resolve()
if not page.is_file():
    sys.exit(f"Not a file: {page}")
answers = []


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(page.parent), **kw)

    def log_message(self, *a):
        pass

    def reply(self, code):
        self.send_response(code)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/__prism":
            return self.reply(204)
        super().do_GET()

    def do_POST(self):
        if self.path not in ("/__prism", "/__prism/png"):
            return self.reply(404)
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path == "/__prism/png":  # a pasted TIFF or HEIC that Chrome cannot draw comes back as PNG (macOS sips), for its thumbnail
            with tempfile.TemporaryDirectory() as d:
                src, dst = pathlib.Path(d, "in"), pathlib.Path(d, "out.png")
                src.write_bytes(body)
                ok = bool(shutil.which("sips")) and subprocess.run(["sips", "-s", "format", "png", str(src), "--out", str(dst)], capture_output=True).returncode == 0 and dst.is_file()
                data = dst.read_bytes() if ok else b""
            self.send_response(200 if ok else 415)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        if not self.headers.get("Content-Type", "").startswith("application/json"):
            answers.append(body.decode("utf-8"))  # older pages post plain text
        else:
            d = json.loads(body)
            text, images = d["text"], d.get("images") or []
            if images:
                out = pathlib.Path(tempfile.gettempdir()) / "prism-notes" / f"{page.stem}-{time.strftime('%Y%m%d-%H%M%S')}"
                out.mkdir(parents=True, exist_ok=True)
                for im in images:
                    f = out / pathlib.Path(im["name"]).name  # a bare file name, never a path from the page
                    f.write_bytes(base64.b64decode(im["data"]))
                    text = text.replace(f"[image: {im['name']}]", f"[image: {f}]")
            answers.append(text)
        self.reply(204)
        threading.Thread(target=server.shutdown).start()


server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
url = f"http://127.0.0.1:{server.server_port}/{urllib.parse.quote(page.name)}"
print(f"Waiting for answers: {url}", file=sys.stderr, flush=True)
if not args.no_open:
    webbrowser.open(url)
timer = threading.Timer(args.timeout, server.shutdown)
timer.daemon = True
timer.start()
server.serve_forever()
if not answers:
    sys.exit(f"No answers within {args.timeout:.0f}s.")
print(answers[0], flush=True)

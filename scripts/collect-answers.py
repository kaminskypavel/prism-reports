#!/usr/bin/env python3
"""Serve a prism page on localhost, open it in the browser (once per chat), and wait for its answers.

The page sees the server (GET /__prism) and turns Copy results into Send results: one click posts the answers here.
The answers print to stdout and the server exits, so an agent that runs this as a background command gets them the
moment the user sends, with no copy and paste. Only the page's folder is served, on 127.0.0.1.
One chat, one tab: each page gets its own fixed port, and the open tab polls GET /__prism/stamp and reloads itself when
the file changes or a new server starts. So a new round only rewrites the file; once the server has exited, run this
again and the same tab picks it up (no new tab opens while one is polling). A server already on the port gets
POST /__prism/quit and hands over.
Images pasted into the page's notes come as JSON; they are saved to a temp folder (they are input, not part of the page)
and each "[image: paste-1.png]" in the answers becomes its full path, so the agent can open it. A pasted TIFF or HEIC
is converted to PNG on paste (POST /__prism/png, macOS sips), so its thumbnail shows in any browser.

Usage: python3 collect-answers.py <page.html> [--timeout SECONDS] [--no-open]
"""
import argparse
import base64
import http.server
import os
import json
import shutil
import subprocess
import pathlib
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
import zlib

ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
ap.add_argument("page")
ap.add_argument("--timeout", type=float, default=4 * 3600, help="give up after this many seconds (default 4 hours)")
ap.add_argument("--no-open", action="store_true", help="print the URL only, do not open a browser")
args = ap.parse_args()
page = pathlib.Path(args.page).resolve()
if not page.is_file():
    sys.exit(f"Not a file: {page}")
answers = []
boot = f"{os.getpid()}-{time.time_ns()}"
polled = threading.Event()


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
        if self.path == "/__prism/stamp":  # the open tab polls this and reloads when it changes
            polled.set()
            data = f"{boot}:{page.stat().st_mtime_ns if page.exists() else 0}".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        super().do_GET()

    def do_POST(self):
        if self.path == "/__prism/quit":  # a newer server for this page takes the port; its tab reloads onto it
            answers.append(None)
            self.reply(204)
            return threading.Thread(target=server.shutdown).start()
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


def bind():
    port = 41000 + zlib.crc32(str(page).encode()) % 2000  # the same port for the same page, so its open tab finds the next server
    for i in range(20):
        try:
            return http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
        except OSError:
            if i == 0:  # an older server for this page (or anything else) holds the port: ask it to hand over
                try:
                    urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{port}/__prism/quit", b""), timeout=2)
                except OSError:
                    break
            time.sleep(0.1)
    return http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)


server = bind()
url = f"http://127.0.0.1:{server.server_port}/{urllib.parse.quote(page.name)}"
print(f"Waiting for answers: {url}", file=sys.stderr, flush=True)
if not args.no_open:  # a tab already open on this page polls within a second or two: it reloads itself, so no new tab
    threading.Thread(target=lambda: polled.wait(3) or webbrowser.open(url), daemon=True).start()
timer = threading.Timer(args.timeout, server.shutdown)
timer.daemon = True
timer.start()
server.serve_forever()
if not answers:
    sys.exit(f"No answers within {args.timeout:.0f}s.")
if answers[0] is None:
    sys.exit("Handed over to a newer server for this page; its output has the answers.")
print(answers[0], flush=True)

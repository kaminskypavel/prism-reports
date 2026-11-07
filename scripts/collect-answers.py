#!/usr/bin/env python3
"""Serve a decision page on localhost, open it in the browser, and wait for its answers.

The page sees the server (GET /__prism) and turns Copy results into Send results: one click posts the answers here
and closes the tab. The answers print to stdout and the server exits, so an agent that runs this as a background
command gets them the moment the user sends, with no copy and paste. Only the page's folder is served, on 127.0.0.1.

Usage: python3 collect-answers.py <page.html> [--timeout SECONDS] [--no-open]
"""
import argparse
import http.server
import pathlib
import sys
import threading
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
        if self.path != "/__prism":
            return self.reply(404)
        answers.append(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))
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

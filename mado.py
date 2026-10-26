#!/usr/bin/env python3
"""mado — one file, in the browser, edited in its live preview.

Usage:  ./mado notes.md [--port 8787] [--no-browser]
Zero dependencies. Python 3 standard library only.
"""
import argparse, json, mimetypes, sys, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
FILE = None  # the single file being edited

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def json(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/file":
            return self.json({"name": FILE.name, "content": FILE.read_text(encoding="utf-8", errors="replace") if FILE.exists() else ""})
        if p in ("/", ""):
            data = (ROOT / "index.html").read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data))); self.send_header("Cache-Control", "no-store")
            self.end_headers(); self.wfile.write(data); return
        self.send_error(404)
    def do_POST(self):
        if urlparse(self.path).path != "/api/file": return self.send_error(404)
        try: payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except Exception: return self.json({"error": "bad json"}, 400)
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text(payload.get("content", ""), encoding="utf-8")
        self.json({"ok": True})

def main():
    global FILE
    ap = argparse.ArgumentParser(prog="mado", description="Edit one markdown file in its live preview")
    ap.add_argument("file", nargs="?", default="note.md", help="the markdown file to edit (default: note.md)")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    FILE = Path(a.file).expanduser()
    if not FILE.exists():
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text("# " + FILE.stem + "\n\nStart writing.\n", encoding="utf-8")
    FILE = FILE.resolve()
    for port in range(a.port, a.port + 20):
        try: srv = ThreadingHTTPServer(("127.0.0.1", port), Handler); break
        except OSError: continue
    else: print("mado: no free port", file=sys.stderr); sys.exit(1)
    url = f"http://127.0.0.1:{port}/"
    print(f"mado  {FILE.name}\n      {url}\n      Ctrl+C to stop")
    if not a.no_browser: threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nmado stopped")

if __name__ == "__main__": main()

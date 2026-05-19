"""
BrewCha — Local dev server.

PyScript needs to be served over HTTP (file:// will not load the .py module).
Run this script with the venv's Python:

    .\\venv\\Scripts\\python.exe serve.py

Then open: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Make stdout safe for Windows consoles that default to cp1252
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Prevent aggressive caching during development
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[BrewCha] {fmt % args}\n")


def main():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        try:
            print(f"\n BrewCha is brewing at {url}")
        except UnicodeEncodeError:
            print(f"\n  [BrewCha] is brewing at {url}")
        print(f"      Serving from: {DIRECTORY}")
        print(f"      Press Ctrl+C to stop.\n")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Stopping server. Salamat!")


if __name__ == "__main__":
    main()

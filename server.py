#!/usr/bin/env python3
"""
Tiny local dev server for a presentation-maker deck.

Serves the deck (and all its media/HTML assets) as static files, plus a
small in-memory /api/state endpoint that lets a speaker-notes page
(notes.html) stay in sync with whatever slide is showing on deck.html --
even when the notes page is open on a totally different device (phone or
tablet) on the same wifi network.

This is the piece that lets you keep the notes off your laptop screen
entirely, so you can screen-share your ENTIRE screen for the whole talk
(one continuous share, no re-sharing when you cut to a live demo) without
ever risking the notes leaking onto the shared screen.

Usage:
    cd into the folder containing deck.html, then:
        python3 server.py [port]

    It will print two URLs:
      - a localhost URL to open the deck in a browser on THIS machine
      - a LAN URL to open notes.html on your phone/tablet
        (must be on the same wifi network as this machine)

No third-party packages required -- standard library only.
"""

import http.server
import json
import socket
import socketserver
import sys
import threading
import webbrowser

DEFAULT_PORT = 8000

# Shared in-memory state, protected by a lock since GET/POST can race.
_state_lock = threading.Lock()
_state = {
    "index": 0,
    "total": 0,
    "slide": {"title": "Waiting for deck...", "timeBudget": "", "notes": []},
    # Presentation timer, controlled from the notes page (start/pause/reset).
    # elapsed = accumulatedMs + (now - startEpoch) while running.
    "timer": {"running": False, "startEpoch": None, "accumulatedMs": 0},
}


def get_lan_ip():
    """Best-effort guess at this machine's LAN IP (no packets actually sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # keep the terminal quiet; open a browser dev console if you need traffic

    def do_GET(self):
        if self.path == "/api/state":
            with _state_lock:
                body = json.dumps(_state).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/state":
            length = int(self.headers.get("Content-Length", 0))
            try:
                payload = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                payload = {}
            with _state_lock:
                _state.update(payload)
            self.send_response(204)
            self.end_headers()
            return
        self.send_response(404)
        self.end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    lan_ip = get_lan_ip()
    with socketserver.ThreadingTCPServer(("0.0.0.0", port), Handler) as httpd:
        print(f"Deck (this machine):   http://localhost:{port}/deck.html")
        print(f"Notes (phone/tablet):  http://{lan_ip}:{port}/notes.html")
        try:
            webbrowser.open(f"http://localhost:{port}/deck.html")
        except Exception:
            pass
        httpd.serve_forever()


if __name__ == "__main__":
    main()

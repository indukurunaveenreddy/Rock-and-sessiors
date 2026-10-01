#!/usr/bin/env python3
"""
Lightweight Web Server for Rock Paper Scissors PRO.
Serves the web application using Python's built-in HTTP server.
"""

import http.server
import os
import socketserver
import webbrowser

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def log_message(self, format, *args):
        # Clean logging
        print(f"[{self.log_date_time_string()}] {format % args}")


def start_server():
    os.chdir(WEB_DIR)
    handler = CustomHTTPHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print("  🎮 Rock Paper Scissors PRO - Web Server Running")
        print("             Developed by Naveen Reddy")
        print(f"  🌐 URL: {url}")
        print("  📁 Serving directory:", WEB_DIR)
        print("  🛑 Press Ctrl+C to stop the server.")
        print("=" * 60)

        # Attempt to automatically open browser
        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped gracefully.")


if __name__ == "__main__":
    start_server()

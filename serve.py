#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3333
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    os.chdir(DIRECTORY)
    url = f"http://localhost:{PORT}/index.html"
    print(f"\n🚀 BikinPlan Web Server berjalan di: {url}")
    print("Tekan Ctrl+C untuk menghentikan server.\n")
    
    # Auto open browser
    webbrowser.open(url)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dimatikan.")
            sys.exit(0)

if __name__ == "__main__":
    run()

import http.server
import os
import socket
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_PORT = 8765


def find_port(start_port: int) -> int:
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("Could not find an open local port.")


def main() -> int:
    port = find_port(DEFAULT_PORT)
    handler = http.server.SimpleHTTPRequestHandler

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReusableTCPServer(("127.0.0.1", port), handler) as server:
        url = f"http://127.0.0.1:{port}/"
        print(f"Serving {ROOT} at {url}")
        print("Press Ctrl+C to stop.")

        browser_thread = threading.Thread(target=webbrowser.open, args=(url,), daemon=True)
        browser_thread.start()

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")
            return 0


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(main())

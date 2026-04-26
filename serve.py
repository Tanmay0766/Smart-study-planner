from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import sys

PORT = 8000
ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"


def run(port: int = PORT) -> None:
    if not FRONTEND_DIR.exists():
        raise FileNotFoundError(f"Frontend directory not found: {FRONTEND_DIR}")

    os.chdir(FRONTEND_DIR)
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serving Smart Study Planner UI at http://localhost:{port}")
    print("Press Ctrl+C to stop.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port '{sys.argv[1]}', using default port {PORT}.")
    run(port)

"""Giao diện web local của bản chạy thử. Khởi động bằng python run.py."""

import json
import sys
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit

import tracing
from agent import answer

HOST = "127.0.0.1"
PORT = 8765
MAX_REQUEST_BYTES = 64 * 1024
WEB_ROOT = Path(__file__).with_name("web")
ASSETS = {
    "/": ("index.html", "text/html"),
    "/styles.css": ("styles.css", "text/css"),
    "/demo.js": ("demo.js", "text/javascript"),
}
# Tracing của bộ khung giữ trạng thái theo tiến trình.
ANALYSIS_LOCK = Lock()


class DemoHandler(BaseHTTPRequestHandler):
    def _send(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, payload):
        self._send(status, "application/json", json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def _is_local(self):
        port = self.server.server_port
        hosts = {f"{HOST}:{port}", f"localhost:{port}"}
        host = self.headers.get("Host")
        origin = self.headers.get("Origin")
        if host in hosts and origin in (None, f"http://{host}"):
            return True
        self._json(HTTPStatus.FORBIDDEN, {"error": "Hãy mở demo bằng địa chỉ local của ứng dụng."})
        return False

    def do_GET(self):
        if not self._is_local():
            return
        asset = ASSETS.get(urlsplit(self.path).path)
        if asset is None:
            self._json(HTTPStatus.NOT_FOUND, {"error": "Không tìm thấy trang."})
            return
        name, content_type = asset
        self._send(HTTPStatus.OK, content_type, (WEB_ROOT / name).read_bytes())

    def do_POST(self):
        if not self._is_local():
            return
        if urlsplit(self.path).path != "/api/analyze":
            self._json(HTTPStatus.NOT_FOUND, {"error": "Không tìm thấy thao tác."})
            return
        if self.headers.get_content_type() != "application/json":
            self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Đầu vào phải là JSON."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > MAX_REQUEST_BYTES:
                self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Đầu vào quá dài. Hãy dán ít review hơn."})
                return
            request = json.loads(self.rfile.read(size)) if size > 0 else None
        except (ValueError, UnicodeError):
            request = None
        text = request.get("text") if isinstance(request, dict) else None
        if not isinstance(text, str) or not text.strip():
            self._json(HTTPStatus.BAD_REQUEST, {"error": "Hãy nhập bộ review hoặc yêu cầu cần kiểm tra."})
            return

        try:
            with ANALYSIS_LOCK:
                tracing.begin("app")
                try:
                    result = answer(text.strip())
                finally:
                    summary, _ = tracing.end()
        except Exception as error:
            print(f"Lỗi phân tích: {type(error).__name__}: {error}", file=sys.stderr)
            message = "Phân tích chưa hoàn tất. Kiểm tra cấu hình model trong terminal và thử lại."
            if isinstance(error, RuntimeError) and "HTTP 402" in str(error):
                message = "OpenRouter báo lỗi 402. Hãy kiểm tra số dư và hạn mức của API key."
            self._json(HTTPStatus.BAD_GATEWAY, {"error": message})
            return
        self._json(HTTPStatus.OK, {"output": result["output"], "usage": summary})

    def log_message(self, format, *args):
        pass


def main() -> int:
    try:
        server = ThreadingHTTPServer((HOST, PORT), DemoHandler)
    except OSError as error:
        print(f"Không mở được demo ở cổng {PORT}: {error}", file=sys.stderr)
        return 1
    url = f"http://{HOST}:{PORT}"
    print(f"Demo phân tích review: {url}", flush=True)
    print("Nhấn Ctrl+C để dừng.", flush=True)
    with server:
        if sys.stdin.isatty():
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

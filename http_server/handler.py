from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
import logging
from http_server.router import Router

logger = logging.getLogger(__name__)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    A simple HTTP request handler that routes requests to the appropriate handler based on the path.
    """

    router = Router()

    @classmethod
    def add_route(cls, path, view_func):
        cls.router.add_route(path, view_func)

    def do_GET(self):
        try:
            self._handle_request()
        # Note: This is a broad exception handler, but for server robustness, we need to catch all exceptions.
        except Exception as e:
            logger.exception("Error handling request at path %s: %s", self.path, e)
            self._send_http_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Server Error")

    def _handle_request(self):
        if not self.router:
            logger.debug("No router found")
            self._send_not_found()
            return

        handler = self.router.get_handler(self.path)
        if handler:
            self._process_handler(handler)
        else:
            self._send_not_found()

    def _process_handler(self, handler):
        try:
            content, status = handler(self)
            self._send_http_response(content, status=status)
        except Exception as e:
            logger.exception("Error processing view function at path %s: %s", self.path, e)
            self._send_http_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Server Error")

    def _send_http_response(self, content, status=HTTPStatus.OK, content_type="text/html"):
        self.send_response(status)
        self.send_header("Content-type", f"{content_type}; charset=utf-8")
        self.end_headers()
        if content:
            self.wfile.write(content.encode("utf-8") if isinstance(content, str) else content)

    def _send_http_error(self, status, message=""):
        self.send_error(status, message)
        self.end_headers()

    def _send_not_found(self):
        self._send_http_error(HTTPStatus.NOT_FOUND, "Not Found")

import logging
import signal
import threading
from http.server import HTTPServer
from typing import Type

from http_server.config import ServerConfig
from http_server.handler import SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


class SimpleHTTPServer(HTTPServer):
    """
    A simple HTTP server that runs on a given host and port and uses a given request handler class.
    Based on the HTTPServer class from the Python standard library.

    - host: The host to listen on.
    - port: The port to listen on.
    - handler_cls: The request handler class to use. - RequestHandler

    HTTPServer handles requests synchronously.
    SimpleHTTPServer handles multiple requests simultaneously via threading.
    """

    def __init__(self, config: ServerConfig, handler_cls: Type[SimpleHTTPRequestHandler], handle_signals: bool = True):
        super().__init__((config.host, config.port), handler_cls)
        self.config = config
        self.handle_signals = handle_signals

    def run(self) -> None:
        try:
            logger.info(f"Server starting on {self.config.host}:{self.config.port}")
            server_thread = threading.Thread(target=self.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            if self.handle_signals:
                signal.signal(signal.SIGINT, self.graceful_shutdown)
                signal.signal(signal.SIGTERM, self.graceful_shutdown)

            server_thread.join()

        except OSError as e:
            logger.error(f"Failed to start server: {e}")
            raise

    def graceful_shutdown(self, signum, frame):
        logger.info("Server is shutting down...")
        self.shutdown()
        self.server_close()
        logger.info("Server stopped")

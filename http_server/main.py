import sys
import logging

# Note: We need to import and setup logging before importing any other modules.
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

from app.controller import Application
from database.config import db_config
from http_server.config import server_config
from http_server.handler import SimpleHTTPRequestHandler
from http_server.server import SimpleHTTPServer


logger = logging.getLogger(__name__)


def main():
    try:
        app = Application(db_config.url)
        is_initialized, message = app.setup()
        if not is_initialized:
            raise RuntimeError(message)

        server = SimpleHTTPServer(server_config, SimpleHTTPRequestHandler)
        server.run()

    except RuntimeError as e:
        logger.error(e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Shutting down server ...")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}")
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

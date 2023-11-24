import os
import logging
from typing import Optional
from dotenv import load_dotenv

DEFAULT_HOST_IP = "0.0.0.0"
DEFAULT_PORT = 8080

load_dotenv()

logger = logging.getLogger(__name__)


class ServerConfig:
    """
    Server configuration class that encapsulates the configuration for the HTTP server:
    - host: The host to listen on.
    - port: The port to listen on.
    - protocol_scheme: The protocol scheme (http or https).
    """

    def __init__(
        self,
        host: Optional[str] = DEFAULT_HOST_IP,
        port: Optional[int] = DEFAULT_PORT,
        protocol_scheme: Optional[str] = "http",
    ):
        self.host = host
        self.port = port
        self.protocol_scheme = protocol_scheme
        logger.debug(f"Server is configured to listen on {self.host}:{self.port}")

    @classmethod
    def from_env(cls):
        try:
            host = os.environ.get("HOST", DEFAULT_HOST_IP)
            port = int(os.environ.get("PORT", DEFAULT_PORT))
            protocol_scheme = os.environ.get("PROTOCOL_SCHEME", "http")
            return cls(host, port, protocol_scheme)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize server configuration: {e}")

    def __str__(self) -> str:
        return f"{self.protocol_scheme}://{self.host}:{self.port}"


try:
    server_config = ServerConfig.from_env()
except Exception as err:
    raise RuntimeError(f"Failed to initialize server configuration: {err}")

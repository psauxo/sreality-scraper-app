import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """
    Database configuration class that encapsulates the configuration for the database:
    - user: Database user: postgres by default.
    - password: Database password: postgres by default.
    - host: Database host: localhost by default.
    - port: Database port number: 5432 by default.
    - dbname: Database name: postgres by default.
    """

    def __init__(self, user: str, password: str, host: str, port: str, dbname: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.validate_config()
        self.url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    def validate_config(self):
        if not all([self.user, self.password, self.host, self.port, self.dbname]):
            raise ValueError("Database configuration is incomplete")

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        try:
            user = os.environ.get("POSTGRES_USER", "postgres")
            password = os.environ.get("POSTGRES_PASSWORD", "postgres")
            host = os.environ.get("POSTGRES_HOST", "postgres")
            port = os.environ.get("POSTGRES_PORT", "5432")
            dbname = os.environ.get("POSTGRES_DB", "postgres")

            config = cls(user, password, host, port, dbname)
            config.validate_config()
            return config

        except Exception as e:
            raise RuntimeError(f"Failed to initialize database configuration: {e}")

    def __str__(self) -> str:
        return self.url


try:
    db_config = DatabaseConfig.from_env()
except Exception as err:
    raise RuntimeError(f"Failed to initialize database configuration: {err}")

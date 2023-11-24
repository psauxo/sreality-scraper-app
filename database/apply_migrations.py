import os
import logging

from alembic.config import Config
from alembic import command
from psycopg2 import OperationalError


class AlembicMigrationManager:
    """
    This class is responsible for applying database migrations using Alembic.
    Usage:
        migration_manager = AlembicMigrationManager(DATABASE_URL)
        migration_manager.apply_migrations()
    """

    def __init__(self, database_url: str, alembic_ini_path: str = "alembic.ini"):
        self.database_url = database_url
        self.alembic_ini_path = alembic_ini_path
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.alembic_dir = os.path.join(self.project_root, "database", "migrations")
        self.alembic_ini_path = os.path.join(self.alembic_dir, "alembic.ini")
        self.logger = logging.getLogger(__name__)

    def apply_migrations(self):
        self._check_alembic_directory()
        self._change_to_alembic_directory()
        alembic_cfg = self._configure_alembic()
        self._apply_database_migrations(alembic_cfg)
        self._revert_to_original_directory()

    def _check_alembic_directory(self):
        if not os.path.exists(self.alembic_dir):
            self.logger.error("Alembic directory not found: %s", self.alembic_dir)
            raise FileNotFoundError("Alembic directory not found %s", self.alembic_dir)

    def _change_to_alembic_directory(self):
        os.chdir(self.alembic_dir)
        self.logger.info("Changed to Alembic directory: %s", os.getcwd())

    def _configure_alembic(self):
        alembic_cfg = Config(self.alembic_ini_path)
        alembic_cfg.set_main_option("sqlalchemy.url", self.database_url)
        alembic_cfg.set_main_option("script_location", self.alembic_dir)
        self.logger.debug("Applied database URL to Alembic config: %s", alembic_cfg.__dict__)
        return alembic_cfg

    def _apply_database_migrations(self, alembic_cfg):
        try:
            self.logger.info("Applying database migrations...")
            command.upgrade(alembic_cfg, "head")
            self.logger.debug("Database migrations applied successfully.")
        except OperationalError as e:
            self.logger.error("Operational error: %s", e)
            raise
        except Exception as e:
            self.logger.error("Failed to apply database migrations: %s", e)
            raise

    def _revert_to_original_directory(self):
        os.chdir(self.project_root)
        self.logger.info("Reverted to original directory: %s", os.getcwd())
        self.logger.info("Database migrations applied successfully.")

import logging
from typing import Tuple

from app.views import FlatsForSalePaginatedListView
from database.apply_migrations import AlembicMigrationManager
from database.factory import SQLAlchemySessionFactory
from http_server.handler import SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, db_url: str):
        """
        Initialize the application with database URL and session factory for centralizing the session creation.
        """
        self.MAX_ITEMS_PER_PAGE = 500
        self.database_url = db_url
        self.session_factory = None

    def setup(self) -> Tuple[bool, str]:
        """
        The setup method is used to initialize the application:
            - Apply database migrations
            - Create session factory
            - Set up routes for the HTTP server

        :return: A tuple of success and message. If success is False, the message contains the error.
        """
        success, message = self._create_session_factory()
        if not success:
            return False, message

        success, message = self._apply_migrations()
        if not success:
            return False, message

        success, message = self._setup_routes()
        if not success:
            return False, message

        return True, "Application initialized successfully"

    def _create_session_factory(self) -> Tuple[bool, str]:
        try:
            self.session_factory = SQLAlchemySessionFactory(self.database_url)
            return True, "Session factory created successfully"
        except Exception as e:
            logger.exception("Failed to create session factory: %s", e)
            return False, f"Failed to create session factory: {e}"

    def _apply_migrations(self) -> Tuple[bool, str]:
        try:
            migration_manager = AlembicMigrationManager(self.database_url)
            migration_manager.apply_migrations()
            return True, "Database migrations applied successfully"
        except Exception as e:
            logger.exception("Failed to apply database migrations: %s", e)
            return False, f"Failed to apply database migrations: {e}"

    def _setup_routes(self) -> Tuple[bool, str]:
        try:
            flats_view = FlatsForSalePaginatedListView(self.session_factory, items_per_page=self.MAX_ITEMS_PER_PAGE)
            SimpleHTTPRequestHandler.add_route("/", lambda handler: flats_view.render())
            return True, "Routes set up successfully"
        except Exception as e:
            logger.exception("Failed to set up routes: %s", e)
            return False, f"Failed to set up routes: {e}"

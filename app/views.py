import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import List, Type, Tuple

from database.sql_schema import Flat
from database.services.pagination import QueryPaginationService
from database.factory import SQLAlchemySessionFactory, get_session
from app.services.html_generator import SimpleHTMLPageGenerator

logger = logging.getLogger(__name__)


class HTMLItemView(ABC):
    def __init__(self, session_factory: SQLAlchemySessionFactory, items_per_page: int):
        self.session_factory = session_factory
        self.items_per_page = items_per_page
        self.page_generator = SimpleHTMLPageGenerator(items_per_page)
        self.pagination_service = QueryPaginationService(session_factory, items_per_page)

    @abstractmethod
    def render_template(self, items, page_number: int, total_pages: int) -> str:
        """
        Render items on an HTML page with pagination.
        :param items: List of items to display.
        :param page_number: Current page number.
        :param total_pages: Total number of pages.
        :return: HTML page as a string.
        """
        pass


class FlatsForSalePaginatedListView(HTMLItemView):
    """
    The FlatsForSalePaginatedListView class renders flats for sale on an HTML page with pagination.
    We show 100 flats per page by default.
    """

    def __init__(self, session_factory: SQLAlchemySessionFactory, items_per_page: int):
        super().__init__(session_factory, items_per_page)
        self.items_per_page = items_per_page

    def render_template(self, items: List[Type[Flat]], page_number: int, total_pages: int) -> str:
        """
        Render flats for sale on an HTML page with pagination.
        :param items: The list of flats to display - Query results.
        :param page_number: The current page number.
        :param total_pages: The total number of pages.
        :return:
        """
        return self.page_generator.generate_page(items, page_number)

    def render(self, page_number: int = 1) -> Tuple[str, HTTPStatus]:
        """
        Render flats for sale on an HTML page with pagination. The page number is optional and defaults to 1.
        The page number is passed as a query parameter in the URL.

        The pagination service is used to paginate the query by page number. The session factory is used to create
        a session for querying the database.

        :param page_number: Page number to render. - Optional[int] = 1 by default
        :return:
        """
        try:
            with get_session(self.session_factory) as session:
                flats, total_pages = self.pagination_service.paginate_query(
                    query=session.query(Flat), page_number=page_number
                )
                return self.render_template(flats, page_number, total_pages), HTTPStatus.OK
        except Exception as e:
            logger.error("Failed to render the items: %s", e)
            raise

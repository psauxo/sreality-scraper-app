from typing import List, Tuple
from database.factory import SQLAlchemySessionFactory


class QueryPaginationService:
    """
    The QueryPaginationService class provides a way to paginate database queries.
    """

    def __init__(self, session_factory: SQLAlchemySessionFactory, items_per_page: int):
        self.session_factory = session_factory
        self.items_per_page = items_per_page

    def paginate_query(self, query, page_number: int) -> Tuple[List, int]:
        """
        Paginate a query by page number.
        We calculate the total number of pages and return the items for the given page.
        :param query:
        :param page_number:
        :return:
        """
        total_items = query.count()
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        offset = query.offset((page_number - 1) * self.items_per_page)
        items = offset.limit(self.items_per_page).all()
        return items, total_pages

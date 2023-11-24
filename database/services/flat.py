import logging
from typing import List, Type
from sqlalchemy.orm import Session

from database.sql_schema import Flat
from database.services.base import BaseDatabaseRetriever, BaseDatabaseWriter
from database.factory import SQLAlchemySessionFactory, get_session
from scraper.services.schema import FlatItemModel

logger = logging.getLogger(__name__)


class FlatDataReader(BaseDatabaseRetriever):
    """
    The database service is responsible for handling retrieval of all the flats from the database.
    - retrieve_all_items: retrieves all the flats from the database
    """

    def __init__(self, session_factory: SQLAlchemySessionFactory):
        super().__init__(session_factory)

    def retrieve_all_items(self) -> List[Type[Flat]]:
        with get_session(session_factory=self.session_factory) as session:
            return session.query(Flat).all()


class FlatDataWriter(BaseDatabaseWriter):
    """
    The database service is responsible for handling the database operations for the Flat model.
    - insert_items: inserts a list of Flat objects to the database
    - handle_error: handles database errors

    For optimization purposes, we are using bulk_insert_mappings() method to save all the items at once:
    https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings
    """

    def __init__(self, session_factory: SQLAlchemySessionFactory, bulk_insert_size=100):
        super().__init__(session_factory=session_factory)
        self.bulk_insert_size = bulk_insert_size

    def insert_items(self, items_to_insert: List[FlatItemModel]):
        with get_session(self.session_factory) as session:
            self._insert_items_batched(session, items_to_insert)

    def _insert_items_batched(self, session: Session, items_to_insert: List[FlatItemModel]):
        batch_size = self.bulk_insert_size
        for i in range(0, len(items_to_insert), batch_size):
            batch = items_to_insert[i : i + batch_size]
            mappings = [item.model_dump() for item in batch]
            session.bulk_insert_mappings(Flat, mappings)
            logger.info("Inserted %s items to the database", len(batch))

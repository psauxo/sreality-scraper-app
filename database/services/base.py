import logging
from abc import ABC, abstractmethod
from typing import List
from database.factory import SQLAlchemySessionFactory
from database.sql_schema import Flat

logger = logging.getLogger(__name__)


class BaseDatabaseManager(ABC):
    def __init__(self, session_factory: SQLAlchemySessionFactory):
        self.session_factory = session_factory

    @staticmethod
    def handle_error(e):
        logger.error("Database error: %s", e)
        raise e


class BaseDatabaseRetriever(BaseDatabaseManager):
    @abstractmethod
    def retrieve_all_items(self) -> List[Flat]:
        raise NotImplementedError


class BaseDatabaseWriter(BaseDatabaseManager):
    @abstractmethod
    def insert_items(self, items_to_insert):
        raise NotImplementedError

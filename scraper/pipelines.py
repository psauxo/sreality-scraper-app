import logging

from database.factory import SQLAlchemySessionFactory
from database.services.flat import FlatDataWriter

from scraper.services.schema import FlatItemModel

logger = logging.getLogger(__name__)


class SaveToDatabasePipeline:
    """
    Pipeline that saves the scraped items to the database:
    - title: title of the flat listing
    - image_url: url of the flat listing's image

    For optimization purposes, we are using bulk_create() method to save all the items at once:
    https://docs.sqlalchemy.org/en/20/orm/large_collections.html#bulk-insert-of-new-items

    In init(), we create a new session. This session is then used in process_item() to save the items to the database.
    """

    def __init__(self, session_factory: SQLAlchemySessionFactory, bulk_insert_size=100):
        self.session_factory = session_factory
        self.bulk_insert_size = bulk_insert_size
        self.items_to_insert = []

    @classmethod
    def from_crawler(cls, crawler):
        db_url = crawler.settings.get("DATABASE_URL")
        if not db_url:
            raise ValueError("Database URL not found in settings")
        session_factory = SQLAlchemySessionFactory(db_url)
        return cls(session_factory=session_factory)

    def process_item(self, item, spider):
        if isinstance(item, FlatItemModel):
            self.items_to_insert.append(item)

            if len(self.items_to_insert) >= self.bulk_insert_size:
                self.insert_items()

            return item
        else:
            logger.error("Item ignored: %s. This item is not an instance of PageItem", item)
            return item

    def insert_items(self):
        db_service = FlatDataWriter(self.session_factory)
        db_service.insert_items(self.items_to_insert)
        self.items_to_insert.clear()

    def close_spider(self, spider):
        if self.items_to_insert:
            self.insert_items()

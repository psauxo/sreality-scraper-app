import logging
import uuid
from typing import Optional, List
from pydantic import ValidationError

from scraper.items import PageItem
from scraper.services.extractor import JsonDataExtractor
from scraper.services.schema import FlatItemModel

logger = logging.getLogger(__name__)


class ApiResponseParser:
    """
    ApiResponseParser is a class that contains logic for:
        1. extracting necessary information from a page via the JsonDataExtractor
        2. validating the extracted information via pydantic and creating FlatItemModels

    The parser will stop parsing once it reaches the max_items limit - 500 by default.
    """

    def __init__(self, json_data_extractor: JsonDataExtractor, max_items: int):
        self.json_data_extractor = json_data_extractor
        self.max_items = max_items
        self.items_scraped = 0

    def parse_api_response(self, url: str, json_response: str) -> List[FlatItemModel]:
        """
        Parses a page and returns a list of PageItems.
        :param url: The URL of the page
        :param json_response: JSON response as a string.
        :return: List of FlatItemModels: id, title, image_url - already validated via pydantic
        """

        items = self.json_data_extractor.process_extraction_safely(url=url, json_response=json_response)
        parsed_items = []

        for item in items:
            if self.items_scraped >= self.max_items:
                break

            parsed_item = self.validate_and_create_flat_item(item)
            if parsed_item:
                parsed_items.append(parsed_item)
                self.items_scraped += 1

        return parsed_items

    @staticmethod
    def validate_and_create_flat_item(item: PageItem) -> Optional[FlatItemModel]:
        """
        Creates a PageItem from a dict and validates it via pydantic.
        If the item is invalid, it will log an error and return None.
        :param item: dict containing the item's title and image_url
        :return: PageItem or None
        """
        try:
            return FlatItemModel(id=uuid.uuid4(), title=item["title"], image_url=item["image_url"])
        except ValidationError as e:
            logger.error("Invalid item: %s. Error: %s", item, e)
            return None

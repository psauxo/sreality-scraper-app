import json
from typing import Optional, List

from scraper.error_handler import ScrapyErrorHandler
from scraper.items import PageItem


class JsonDataExtractor:
    """
    JsonDataExtractor is a class that contains logic for extracting necessary information from a JSON response:
        - title: title of the listing (e.g. "2+kk, 50m²")
        - image_url: url of the listing's image
    """

    @staticmethod
    def extract_title(estate: dict) -> Optional[str]:
        name = estate.get("name")
        locality = estate.get("locality")
        price = estate.get("price_czk", {}).get("value_raw")

        title_parts = [name, locality]
        if price:
            title_parts.append(f"{price} CZK")

        return ", ".join(filter(None, title_parts))

    @staticmethod
    def extract_image_url(estate: dict) -> Optional[str]:
        images = estate.get("_links", {}).get("images", [])
        if images:
            return images[0].get("href")
        return None

    def extract_items_from_response(self, json_response: str) -> List[PageItem]:
        """
        Parses a JSON response and returns a list of items with title and image URL.
        :param json_response: JSON response as a string.
        :return: List of items with title and image URL.
        """
        data = json.loads(json_response)
        estates = data.get("_embedded", {}).get("estates", [])

        items = []
        for estate in estates:
            title = self.extract_title(estate)
            image_url = self.extract_image_url(estate)
            if title and image_url:
                items.append(PageItem(title=title, image_url=image_url))
        return items

    def process_extraction_safely(self, url: str, json_response: str) -> List[Optional[PageItem]]:
        """
        Handle the page processing with built-in error handling.
        :param url: URL of the page
        :param json_response: JSON response as a string.
        :return: List of processed PageItems
        """
        try:
            return self.extract_items_from_response(json_response=json_response)
        except Exception as e:
            ScrapyErrorHandler.handle_parsing_error(e=e, url=url)
            return []

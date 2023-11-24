import logging
from typing import Generator

import scrapy

from database.config import db_config
from scraper.services.configuration import ApiUrlConfigService
from scraper.services.parser import ApiResponseParser
from scraper.services.extractor import JsonDataExtractor

logger = logging.getLogger(__name__)


class SrealitySpider(scrapy.Spider):
    """
    The SrealitySpider is a class that contains logic for scraping the sreality.cz website.

    Purpose of this spider is to scrape listings from the sreality.cz website and save them to the database:
    - title: title of the listing (e.g. "2+kk, 50m²")
    - image_url: url of the listing's image

    The spider is able to scrape listings in multiple languages: Czech, English, Russian.
    Languages are supported by the sreality.cz website.

    Once the spider is started, it will scrape the first page and then it will scrape the next page and so on.
    The spider will stop scraping once it reaches the max_items limit (500 by default)

    The spider pass the scraped items to SaveToDatabasePipeline
    which is responsible for saving the items to the database:
    {
        "id": 123e4567-e89b-12d3-a456-426614174000,
        "title": "2+kk, 50m²",
        "image_url": "https://img.sreality.cz/2/1/213/213684/213684831/213684831.1.jpg"
    }
    """

    name = "sreality_spider"
    custom_settings = {
        "DATABASE_URL": db_config.url,
        "ITEM_PIPELINES": {"scraper.pipelines.SaveToDatabasePipeline": 300},
    }

    def __init__(self, language="en", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = language
        self.items_scraped = 0
        self.max_items = 500
        self.json_data_extractor = JsonDataExtractor()
        self.page_parser = ApiResponseParser(json_data_extractor=self.json_data_extractor, max_items=self.max_items)

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        start_url = ApiUrlConfigService.get_start_url()
        yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs):
        logger.debug("Start parsing %s", response.url)

        if response.status != 200 or not response.body:
            logging.error(f"Error while scraping {response.url}. Status code: {response.status}")
            return None

        parsed_items = self.page_parser.parse_api_response(url=response.url, json_response=response.body)
        for item in parsed_items:
            if not self.increment_items_scraped():
                return
            yield item

        if self.items_scraped < self.max_items:
            next_page_url = ApiUrlConfigService.build_next_page_url(response.url)
            if next_page_url:
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                logger.info("No more pages to scrape")

    def increment_items_scraped(self) -> bool:
        """
        Increment the number of items scraped.
        If the number of items scraped is greater than or equal to the max_items limit, then stop scraping.
        :return: bool - True if the spider should continue scraping, False otherwise.
        """
        self.items_scraped += 1
        if self.items_scraped >= self.max_items:
            logger.warning("Reached maximum item limit of %s", self.max_items)
            return False
        return True

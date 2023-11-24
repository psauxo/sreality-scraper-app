from unittest.mock import Mock
from pydantic import HttpUrl
from scraper.services.extractor import JsonDataExtractor
from scraper.services.parser import ApiResponseParser
from scraper.services.schema import FlatItemModel


def test_api_response_parser():
    # Mock JsonDataExtractor
    mock_extractor = Mock(spec=JsonDataExtractor)
    mock_extractor.process_extraction_safely.return_value = [
        {"title": "Flat 1", "image_url": "http://example.com/img1.jpg"},
        {"title": "Flat 2", "image_url": "http://example.com/img2.jpg"},
    ]

    parser = ApiResponseParser(json_data_extractor=mock_extractor, max_items=2)

    json_response = '{"data": "mocked data"}'
    parsed_items = parser.parse_api_response("http://example.com/api", json_response)

    assert len(parsed_items) == 2
    assert all(isinstance(item, FlatItemModel) for item in parsed_items)
    assert parsed_items[0].title == "Flat 1"
    assert parsed_items[0].image_url == HttpUrl("http://example.com/img1.jpg")

    assert parser.items_scraped == 2

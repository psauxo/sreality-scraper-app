import pytest
from scrapy.http import HtmlResponse


@pytest.mark.parametrize(
    "json_response,expected_count",
    [
        (b'{"_embedded": {"estates": [{"title": "Flat 1", "image_url": "http://example.com/img1.jpg"}]}}', 1),
        (b"{}", 0),
    ],
)
def test_parse(sreality_spider, mock_api_response_parser, json_response, expected_count):
    mock_api_response_parser.parse_api_response.return_value = [
        {"title": "Mock Flat", "image_url": "http://example.com/mock.jpg"}
    ] * expected_count

    fake_url = "http://example.com"
    fake_response = HtmlResponse(url=fake_url, body=json_response, encoding="utf-8")

    parsed_items = [item for item in sreality_spider.parse(fake_response) if isinstance(item, dict)]
    assert len(parsed_items) == expected_count, f"Expected {expected_count} items, got {len(parsed_items)}"

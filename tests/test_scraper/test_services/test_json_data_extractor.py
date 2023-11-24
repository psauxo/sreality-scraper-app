import json
from scraper.services.extractor import JsonDataExtractor


def test_json_data_extractor():
    mock_json_response = {
        "_embedded": {
            "estates": [
                {
                    "name": "2+kk, 50m²",
                    "locality": "Prague",
                    "price_czk": {"value_raw": 3000000},
                    "_links": {"images": [{"href": "http://example.com/img1.jpg"}]},
                },
                {
                    "name": "3+kk, 60m²",
                    "locality": "Brno",
                    "price_czk": {"value_raw": 4000000},
                    "_links": {"images": [{"href": "http://example.com/img2.jpg"}]},
                },
            ]
        }
    }

    extractor = JsonDataExtractor()
    json_response_str = json.dumps(mock_json_response)
    items = extractor.extract_items_from_response(json_response_str)

    assert len(items) == 2
    assert items[0]["title"] == "2+kk, 50m², Prague, 3000000 CZK"
    assert items[0]["image_url"] == "http://example.com/img1.jpg"

    assert items[1]["title"] == "3+kk, 60m², Brno, 4000000 CZK"
    assert items[1]["image_url"] == "http://example.com/img2.jpg"

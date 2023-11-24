from app.services.html_generator import SimpleHTMLPageGenerator
from database.sql_schema import Flat


def test_simple_html_page_generator():
    generator = SimpleHTMLPageGenerator(items_per_page=2)

    # Mock items (Flats)
    flats = [
        Flat(title="Flat 1", image_url="http://example.com/img1.jpg"),
        Flat(title="Flat 2", image_url="http://example.com/img2.jpg"),
        Flat(title="Flat 3", image_url="http://example.com/img3.jpg"),
    ]

    # Test with non-empty items
    html = generator.generate_page(flats, 1)
    assert "<h3>🏠 Flat 1</h3>" in html
    assert "<h3>🏠 Flat 2</h3>" in html
    assert 'src="http://example.com/img1.jpg"' in html
    assert 'src="http://example.com/img2.jpg"' in html

    # Test with empty items
    empty_html = generator.generate_page([], 1)
    assert "🕵️ No items to display." in empty_html

    # Test pagination on the second page
    page_2_html = generator.generate_page(flats, 2)
    assert "<h3>🏠 Flat 3</h3>" in page_2_html

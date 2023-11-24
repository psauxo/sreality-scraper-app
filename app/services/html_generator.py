from abc import ABC, abstractmethod
from typing import Sized


class HTMLPageGenerator(ABC):
    def __init__(self, items_per_page: int):
        self.items_per_page = items_per_page

    @abstractmethod
    def generate_page(self, items, page_number: int):
        """
        Generate an HTML page to display the items with pagination.
        :param items: List of items to display. Query results.
        :param page_number: Current page number.
        :return: HTML page as a string.
        """
        pass


class SimpleHTMLPageGenerator(HTMLPageGenerator):
    """
    Simple HTML page generator that displays the items as a list:
    <h2>title</h2>
    <img src="image_url" alt="title" width="300"><br><br>
    <h2>title</h2>
    <img src="image_url" alt="title" width="300"><br><br>
    ...

    For purpose to implement pagination, we can add the following links to the page:
    if page_number > 1:
        html += f'<a href="/page/{page_number - 1}">👈Previous Page</a> '

    if page_number <= total_pages:
        html += f'<a href="/page/{page_number + 1}">👉Next Page</a>'

    <a href="/page/1">Previous Page</a>
    <a href="/page/3">Next Page</a>
    """

    def generate_page(self, items: Sized, page_number: int) -> str:
        total_items = len(items)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page

        start_idx = (page_number - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        items_to_display = items[start_idx:end_idx]

        if not items_to_display:
            return "<html><body>🕵️ No items to display.</body></html>"

        html = "<html><body>"
        current_page = page_number
        html += f"<h1>🏠 Flats for Sale (Page {current_page} of {total_pages})</h1>"
        html += f"<h2>#️⃣ Total Items: {total_items} | Items per Page: {self.items_per_page}</h2>"
        html += "<hr>"

        for item in items_to_display:
            html += f"<h3>🏠 {item.title}</h3>"
            html += f'<img src="{item.image_url}" alt="{item.title}" width="250"><br><br>'

        html += "</body></html>"
        return html

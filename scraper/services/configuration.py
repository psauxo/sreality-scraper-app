from typing import Optional
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class ApiUrlConfigService:
    """
    Service for configuring Scrapy spiders with the appropriate start URL for API parsing.

    This service provides the functionality to retrieve the start URL for the API,
    which is used to fetch data from sreality.cz. The content from this site is loaded
    dynamically via JavaScript, hence the necessity to use the API endpoint for scraping.

    docs: https://docs.scrapy.org/en/latest/topics/dynamic-content.html#topics-dynamic-content-ref

    The class allows customization of the following query parameters:
    - per_page: Number of items to display per page.
    - page: The page number in the paginated result set.
    - category_main_cb: Main category code for filtering the results.
    - category_type_cb: Type category code for further filtering the results.
    """

    BASE_API_URL = "https://www.sreality.cz/api/cs/v2/estates"

    @staticmethod
    def get_start_url(custom_parameters: dict = None) -> str:
        """
        Construct the start URL for the API with customizable query parameters.

        :param custom_parameters: Dictionary of API parameters for custom requests.
        :return: Constructed API URL with the given parameters or a default set if none provided.
        """
        default_parameters = {"per_page": 60, "page": 1, "category_main_cb": 1, "category_type_cb": 1}

        # Update default parameters with any custom parameters provided
        if custom_parameters:
            default_parameters.update(custom_parameters)

        query_string = urlencode(default_parameters)
        return f"{ApiUrlConfigService.BASE_API_URL}?{query_string}"

    @staticmethod
    def build_next_page_url(url: str) -> Optional[str]:
        """
        Modifies the provided API URL to point to the next page in a paginated sequence.
        :param url: The current API URL.
        :return: The modified API URL pointing to the next page, or None if not applicable.
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        current_page = int(query_params.get("page", [1])[0])
        query_params["page"] = [str(current_page + 1)]

        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=new_query))

        return new_url

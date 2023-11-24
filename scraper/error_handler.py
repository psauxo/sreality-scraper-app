import logging
from scrapy.exceptions import IgnoreRequest, CloseSpider
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


logger = logging.getLogger(__name__)


class ScrapyErrorHandler:
    """
    Service to handle Scrapy related errors:
    - Request errors: ConnectionError, Timeout, TooManyRedirects
    - Parsing errors: errors that occur during parsing of the response
    - Other errors: unhandled exceptions

    Based on Scrapy's recommendations:
    https://docs.scrapy.org/en/latest/topics/request-response.html#error-handling
    """

    @staticmethod
    def handle_request_error(e: Exception, url: str):
        """
        Handle errors that occur during Scrapy requests.
        """
        if isinstance(e, ConnectionError):
            ScrapyErrorHandler._log_error(f"Connection failed for URL {url}.", e)
        elif isinstance(e, Timeout):
            ScrapyErrorHandler._log_error(f"Request to {url} timed out.", e)
        elif isinstance(e, TooManyRedirects):
            ScrapyErrorHandler._log_error(f"Too many redirects for URL {url}.", e)
        else:
            ScrapyErrorHandler._log_error("An unexpected error occurred during the request.", e)
            raise IgnoreRequest("Unhandled exception occurred.")

    @staticmethod
    def handle_parsing_error(e: Exception, url: str):
        """
        Handle errors that occur during parsing of the response.
        """
        ScrapyErrorHandler._log_error(f"Parsing error for URL {url}.", e)
        raise CloseSpider("Critical parsing error occurred.")

    @staticmethod
    def _log_error(message: str, exception: Exception):
        """
        Log the error message and exception.
        """
        logger.error(f"{message} Exception: {exception}")

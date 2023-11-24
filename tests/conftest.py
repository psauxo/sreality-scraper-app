import logging
import threading
from unittest.mock import Mock

import pytest
from psycopg2.errorcodes import DUPLICATE_DATABASE
import sqlalchemy
from sqlalchemy import text
from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy.orm.session import sessionmaker

from app.controller import Application
from database.config import db_config
from database.factory import get_session
from pytest_postgresql.janitor import DatabaseJanitor
from database import sql_schema
from http_server.config import ServerConfig
from http_server.handler import SimpleHTTPRequestHandler
from http_server.server import SimpleHTTPServer
from scraper.services.extractor import JsonDataExtractor
from scraper.services.parser import ApiResponseParser
from scraper.spiders.sreality_spider import SrealitySpider
from tests.utils import load_test_data, clear_test_data

logger = logging.getLogger(__name__)

SERVER_TESTING_IP = "127.0.0.1"
SERVER_TESTING_PORT = 8089
BASE_URL = f"http://{SERVER_TESTING_IP}:{SERVER_TESTING_PORT}"


@pytest.fixture(scope="session")
def database_url():
    """A new fresh DB is created prefixed with 'test_' prefix and dropped after the test session."""
    test_db_name = f"test_{db_config.dbname}"

    test_db_url = (
        f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{test_db_name}"
    )

    if database_exists(test_db_url):
        logger.warning("Test database already exists. Dropping it...")
        drop_database(test_db_url)

    logger.info(f"Creating a test database {test_db_name}...")
    janitor = DatabaseJanitor(
        user=db_config.user,
        host=db_config.host,
        port=db_config.port,
        password=db_config.password,
        dbname=test_db_name,
        version="14.0",
    )
    try:
        janitor.init()
    except Exception as e:
        if getattr(e, "pgcode", None) != DUPLICATE_DATABASE:
            raise e
        janitor.drop()
        janitor.init()
    finally:
        yield test_db_url
        janitor.drop()


@pytest.fixture(scope="session")
def db_session(initialized_application) -> sqlalchemy.orm.Session:
    """
    We need to reuse the same session for the whole testing session.
    :param initialized_application:
    :return:
    """
    with get_session(initialized_application.session_factory) as session:
        yield session


@pytest.fixture(scope="session")
def initialized_application(database_url) -> Application:
    """
    Initialize the application and apply database migrations for the testing session.

    :param database_url: The database URL for the test database.
    :return: An instance of the initialized Application.
    """
    print(f"Database URL: {database_url}")

    app = Application(database_url)
    is_initialized, message = app.setup()
    assert is_initialized, f"Setup should be successful. Message: {message}"

    with get_session(app.session_factory) as session:
        result = session.execute(text("SELECT to_regclass('public.flats')"))
        table_exists = result.fetchone()[0] is not None
        assert table_exists, "Table flats does not exist in the database."

    yield app


@pytest.fixture(scope="session")
def server_fixture():
    """
    Run the server in a separate thread for the testing session.
    """
    server_config = ServerConfig(host=SERVER_TESTING_IP, port=SERVER_TESTING_PORT)
    http_server = SimpleHTTPServer(server_config, SimpleHTTPRequestHandler, handle_signals=False)

    server_thread = threading.Thread(target=http_server.run, daemon=True)
    server_thread.start()

    yield http_server

    http_server.shutdown()
    server_thread.join()


@pytest.fixture(scope="function")
def test_data(initialized_application, db_session):
    """
    Load test data into the database before running tests:
        [{
            "id": "12345678-1234-5678-1234-567812345678",
            "title": "Prodej bytu 3+kk 73 m², Praha 6 - Bubeneč, 10900000 CZK",
            "image_url": "https://test-a.sdn.cz/d_18/c_img_QM_Kc/pF5BiVP.jpeg?fl=res,400,300,3|shr,,20|jpg,90",
        }]
    :param db_session:
    :param initialized_application:
    :return:
    """
    load_test_data(db_session)
    yield
    clear_test_data(db_session)


@pytest.fixture(scope="function")
def empty_database_state(db_session):
    """
    Ensure the database is in an empty state (specifically, the 'flats' table).
    :param db_session: The database session.
    :return: None
    """
    with db_session.begin():
        db_session.query(sql_schema.Flat).delete()
        db_session.commit()

    yield


@pytest.fixture
def mock_api_response_parser():
    mock_parser = Mock(spec=ApiResponseParser)
    return mock_parser


@pytest.fixture
def sreality_spider(mock_api_response_parser):
    mock_extractor = Mock(spec=JsonDataExtractor)
    mock_api_response_parser.json_data_extractor = mock_extractor
    spider = SrealitySpider(language="en")
    spider.page_parser = mock_api_response_parser
    return spider

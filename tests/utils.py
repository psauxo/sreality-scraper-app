import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from database.sql_schema import Flat

logger = logging.getLogger(__name__)


def load_test_data(session: Session) -> None:
    try:
        test_data = [
            {
                "id": "12345678-1234-5678-1234-567812345678",
                "title": "Prodej bytu 3+kk 73 m², Praha 6 - Bubeneč, 10900000 CZK",
                "image_url": "https://test-a.sdn.cz/d_18/c_img_QM_Kc/pF5BiVP.jpeg?fl=res,400,300,3|shr,,20|jpg,90",
            },
            {
                "id": "12345678-1234-5678-1234-567812345679",
                "title": "Prodej bytu 1+kk 30 m², Praha 6 - Bubeneč, 4990000 CZK",
                "image_url": "https://test-a.sdn.cz/d_18/c_img_gG_Q/6XJBiV.jpeg?fl=res,400,300,3|shr,,20|jpg,90",
            },
        ]

        for data in test_data:
            session.execute(Flat.__table__.insert().values(**data))
        session.commit()

    except Exception as e:
        logger.error("Failed to load test data: %s", e)
        session.rollback()
        raise e


def clear_test_data(session: Session):
    session.execute(Flat.__table__.delete())
    session.commit()


def parse_html_for_flats(html_content: str) -> List[Dict[str, Any]]:
    """
    Parses HTML content to extract flat details. Returns a list of dictionaries.
    :param html_content: HTML content as a string.
    :return: A list of dictionaries containing flat details.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    flats = []
    for h2_tag in soup.find_all("h3"):
        flat_info = {"title": h2_tag.get_text()}

        # Find the next <img> tag
        img_tag = h2_tag.find_next("img")
        if img_tag:
            flat_info["image_url"] = img_tag["src"]

        flats.append(flat_info)

    return flats

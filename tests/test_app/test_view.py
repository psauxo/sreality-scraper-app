import requests

from database.sql_schema import Flat
from tests.conftest import BASE_URL
from tests.utils import parse_html_for_flats


def test_no_items_to_display(server_fixture, empty_database_state):
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200
    assert "🕵️ No items to display." in response.text


def test_display_flats(server_fixture, test_data, db_session):
    with db_session.begin():
        flats = db_session.query(Flat).all()
        assert len(flats) > 0, "No flats found in the database."

        assert str(flats[0].id) == "12345678-1234-5678-1234-567812345678"

    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200
    flats = parse_html_for_flats(response.text)
    assert len(flats) == 2
    assert flats == [
        {
            "title": "🏠 Prodej bytu 3+kk 73 m², Praha 6 - Bubeneč, 10900000 CZK",
            "image_url": "https://test-a.sdn.cz/d_18/c_img_QM_Kc/pF5BiVP.jpeg?fl=res,400,300,3|shr,,20|jpg,90",
        },
        {
            "title": "🏠 Prodej bytu 1+kk 30 m², Praha 6 - Bubeneč, 4990000 CZK",
            "image_url": "https://test-a.sdn.cz/d_18/c_img_gG_Q/6XJBiV.jpeg?fl=res,400,300,3|shr,,20|jpg,90",
        },
    ]

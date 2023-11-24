import requests
from tests.conftest import BASE_URL


def test_404_not_found(server_fixture):
    response = requests.get(f"{BASE_URL}/nonexistentpath")
    assert response.status_code == 404
    assert "Not Found" in response.text


def test_200_ok(server_fixture):
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200

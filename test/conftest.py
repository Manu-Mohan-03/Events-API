import pytest
import requests


BASE_URL = "http://127.0.0.1:5001"

@pytest.fixture()
def auth_token():
    user_data = {
        "username": "John",
        "password": "init1234"
    }
    response = requests.post(
        url = f"{BASE_URL}/api/auth/login",
        json = user_data
    )

    return response.json().get("access_token")

@pytest.fixture()
def is_public():
    response = requests.get(
        f"{BASE_URL}/api/rsvps/event/5"
    )
    if response.status_code == 200:
        return response.json().get("event").get("is_public")
    return None

# is_public()

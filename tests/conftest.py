import os
import random
from http import HTTPStatus

import requests
import dotenv
import pytest


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url() -> str:
    return os.getenv("APP_URL")


@pytest.fixture
def users(app_url: str) -> dict:
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()

@pytest.fixture
def random_user_id(users: dict) -> int:
    return random.choice([user["id"] for user in users["items"]])
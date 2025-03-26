import os
from http import HTTPStatus

import requests
import dotenv
import pytest
import random

from faker import Faker

faker = Faker()
AUTOTEST_PREFIX = "autotest"


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url() -> str:
    return os.getenv("APP_URL")


@pytest.fixture(scope="session", autouse=True)
def generate_users(app_url: str) -> list[int]:
    """Генерация пользователей для сессии с тестами и удаление"""
    _clear_users_in_db(app_url)  # Очистка перед началом

    api_users = []
    for _ in range(12):
        response = requests.post(f"{app_url}/api/users/", json=generate_user_data())
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    _clear_users_in_db(app_url)

@pytest.fixture(scope="function")
def create_user(app_url: str ) -> dict:
    """Создание пользователя для теста"""

    response = requests.post(f"{app_url}/api/users/", json=generate_user_data())
    assert response.status_code == HTTPStatus.CREATED

    yield response.json()


@pytest.fixture
def users(app_url: str):
    """Получение пользователей"""
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]


def _clear_users_in_db(app_url: str) -> None:
    """Удаление всех сгенерированных пользователей из БД после прогона"""
    response = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": 100})
    users = response.json()["items"]

    generated_users = [user for user in users if AUTOTEST_PREFIX in user["email"]]

    for user in generated_users:
        requests.delete(f"{app_url}/api/users/{user['id']}")


def generate_user_data() -> dict[str, str]:
    """Генерация данных для тестового юзера"""
    user_data = {
        "email": faker.email(domain=f"{AUTOTEST_PREFIX}.com"),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "avatar": f"https://reqres.in/img/faces/{AUTOTEST_PREFIX}{random.randint(0, 5000)}-image.jpg"
    }
    return user_data
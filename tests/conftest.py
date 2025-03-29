import random
from http import HTTPStatus

import dotenv
import pytest
from faker import Faker

from clients.users_api import UsersApi

faker = Faker()
AUTOTEST_PREFIX = "autotest"


@pytest.fixture(scope='session', autouse=True)
def envs():
    dotenv.load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def users_api(env):
    yield UsersApi(env)


@pytest.fixture(scope="session", autouse=True)
def generate_users(users_api: UsersApi) -> list[int]:
    """Генерация пользователей для сессии с тестами и удаление"""
    _clear_users_in_db(users_api)  # Очистка перед началом

    api_users = []
    for _ in range(12):
        response = users_api.create_user(json=generate_user_data())
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    _clear_users_in_db(users_api)


@pytest.fixture(scope="function")
def create_user(users_api: UsersApi) -> dict:
    """Создание пользователя для теста"""

    response = users_api.create_user(json=generate_user_data())
    assert response.status_code == HTTPStatus.CREATED

    yield response.json()


@pytest.fixture
def users(users_api: UsersApi):
    """Получение пользователей"""
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]


def _clear_users_in_db(users_api: UsersApi) -> None:
    """Удаление всех сгенерированных пользователей из БД после прогона"""
    response = users_api.get_users(params={"page": 1, "size": 100})
    users = response.json()["items"]

    generated_users = [user for user in users if AUTOTEST_PREFIX in user["email"]]

    for user in generated_users:
        users_api.delete_user(user_id=user['id'])


def generate_user_data() -> dict[str, str]:
    """Генерация данных для тестового юзера"""
    user_data = {
        "email": faker.email(domain=f"{AUTOTEST_PREFIX}.com"),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "avatar": f"https://reqres.in/img/faces/{AUTOTEST_PREFIX}{random.randint(0, 5000)}-image.jpg"
    }
    return user_data

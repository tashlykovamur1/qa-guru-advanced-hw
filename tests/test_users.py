from http import HTTPStatus

import pytest

from app.models.User import User
from clients.users_api import UsersApi
from tests.conftest import AUTOTEST_PREFIX, generate_user_data


class TestUsers:

    def test_get_users(self, users_api: UsersApi):
        """Проверка получения юзеров"""
        response = users_api.get_users()
        assert response.status_code == HTTPStatus.OK

        for user in response.json()["items"]:
            User.model_validate(user)

    def test_users_no_duplicates(self, users: list[User]):
        """Проверка, что среди юзеров нет дублей"""
        users_ids = [user["id"] for user in users]
        assert len(users_ids) == len(set(users_ids))

    def test_get_user_by_id(self, users_api: UsersApi, generate_users: list[int]):
        """Проверка получения юзера с существующим user_id"""
        response = users_api.get_user(user_id=generate_users[0])
        assert response.status_code == HTTPStatus.OK

        user = response.json()
        User.model_validate(user)

    def test_get_user_by_unexisted_id(self, users_api: UsersApi, generate_users: list[int]):
        """Проверка получения юзера с несуществующим user_id"""
        unexisted_id = generate_users[-1] + 1
        response = users_api.get_user(user_id=unexisted_id)
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-1, 0, "asd", [3], None])
    def test_get_user_with_invalid_id(self, users_api: UsersApi, user_id):
        """Проверка получения юзера с невалидным user_id"""
        response = users_api.get_user(user_id)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_user(self, users_api: UsersApi):
        """Проверка создания юзера"""
        created_user_data = generate_user_data()
        response = users_api.create_user(json=created_user_data)
        assert response.status_code == HTTPStatus.CREATED

        user = response.json()
        User.model_validate(user)
        del user['id']
        assert created_user_data == user

    def test_delete_user(self, users_api: UsersApi, create_user: dict):
        """Проверка удаления юзера"""
        response = users_api.delete_user(user_id=create_user['id'])

        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"] == "User deleted"

    @pytest.mark.parametrize("user_data", [
        {
            "email": f"test-email@{AUTOTEST_PREFIX}.com",
        },
        {
            "first_name": "test name"
        },
        {
            "last_name": "last name"
        },
        {
            "avatar": "https://reqres.in/img/faces/unique-avatar-1.jpg"
        },
        {
            "email": f"autotestemail4@{AUTOTEST_PREFIX}.com",
            "first_name": "firstname1",
            "last_name": "lastname1",
            "avatar": "https://reqres.in/img/faces/unique-avatar-0.jpg"
        }
    ])
    def test_update_user(self, users_api: UsersApi, user_data: dict, create_user: dict):
        """Проверка обновления данных юзера"""

        response = users_api.update_user(user_id=create_user['id'], json=user_data)
        assert response.status_code == HTTPStatus.OK
        updated_user = response.json()
        User.model_validate(updated_user)

        assert create_user['id'] == updated_user['id']
        for key in user_data.keys():
            assert create_user[key] != updated_user[key]

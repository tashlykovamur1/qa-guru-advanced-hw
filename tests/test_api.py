from http import HTTPStatus
import pytest
import requests
from fastapi_pagination import Page

from models.User import User


class TestUsersApi:

    def test_get_users(self, app_url: str):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        Page[User].model_validate(response.json())

    def test_users_no_duplicates(self, users: dict):
        users_ids = [user["id"] for user in users["items"]]
        assert len(users_ids) == len(set(users_ids))


    def test_get_user_by_id(self, app_url: str, random_user_id: int):
        """Проверка получения юзера с существующим user_id"""
        response = requests.get(f"{app_url}/api/users/{random_user_id}")
        assert response.status_code == HTTPStatus.OK

        user = response.json()
        User.model_validate(user)

    def test_get_user_by_unexisted_id(self, app_url: str, users: dict):
        """Проверка получения юзера с несуществующим user_id"""
        unexisted_id = len(users["items"]) + 1
        response = requests.get(f"{app_url}/api/users/{unexisted_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND


    @pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
    def test_get_user_with_invalid_id(self, app_url: str, user_id):
        """Проверка получения юзера с невалидным user_id"""
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

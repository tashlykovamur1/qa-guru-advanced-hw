from http import HTTPStatus

import pytest
from fastapi_pagination import Page

from app.models.AppStatus import AppStatus
from app.models.User import User
from clients.users_api import UsersApi


@pytest.mark.smoke
class TestUsersSmoke:
    def test_smoke(self, users_api: UsersApi):
        response = users_api.get_app_status()
        assert response.status_code == HTTPStatus.OK

        result = response.json()
        AppStatus.model_validate(result)

        assert result["database"]

    def test_smoke_users(self, users_api: UsersApi):
        response = users_api.get_users()
        assert response.status_code == HTTPStatus.OK

        result = response.json()
        Page[User].model_validate(result)

        assert 'items' in result
        assert len(result['items']) > 0

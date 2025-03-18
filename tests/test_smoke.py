import pytest
import requests
from http import HTTPStatus

from fastapi_pagination import Page

from app.models.User import User
from app.models.AppStatus import AppStatus


@pytest.mark.smoke
class TestUsersSmoke:
    def test_smoke(self, app_url: str):
        response = requests.get(f"{app_url}/status/")
        assert response.status_code == HTTPStatus.OK

        result = response.json()
        AppStatus.model_validate(result)

        assert result["database"]

    def test_smoke_users(self, app_url: str):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK

        result = response.json()
        Page[User].model_validate(result)

        assert 'items' in result
        assert len(result['items']) > 0
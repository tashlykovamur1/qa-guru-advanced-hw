from http import HTTPStatus

import pytest
import requests
from fastapi_pagination import Page

from models.User import User


class TestUsersPagination:
    @pytest.mark.parametrize("page1, page2, size", [
        (1, 2, 5),
        (2, 3, 5),
        (1, 2, 10),
    ])
    def test_pagination_different_pages(self, app_url: str, page1, page2, size):
        """Проверка, что разные страницы возвращают разные данные"""

        page1_response = requests.get(f'{app_url}/api/users/', params={"page": page1, "size": size})
        assert page1_response.status_code == HTTPStatus.OK

        page2_response = requests.get(f"{app_url}/api/users/", params={"page": page2, "size": size})
        assert page2_response.status_code == HTTPStatus.OK

        page1_result = page1_response.json()
        page2_result = page2_response.json()

        for result in [page1_result, page2_result]:
            Page[User].model_validate(result)

        assert page1_result["items"] != page2_result["items"]

    @pytest.mark.parametrize("size", [
        4,
        1,
        12,
    ])
    def test_pagination_total_pages(self, app_url: str, size, users: dict):
        """Проверка, что общее количество страниц вычисляется правильно"""

        response = requests.get(f"{app_url}/api/users/", params={"size": size})
        assert response.status_code == HTTPStatus.OK

        result = response.json()
        Page[User].model_validate(result)

        actual_pages = result["pages"]
        expected_pages = (len(users["items"]) + size - 1) // size

        assert actual_pages == expected_pages, (
            f"Ожидалось {expected_pages} страниц, но получено {actual_pages} "
            f"для size={size} и total_items={len(users["items"])}"
        )

    def test_users_pagination_total(self, app_url: str, users: dict):
        """Проверка, что общее количество записей вычисляется правильно"""

        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        Page[User].model_validate(result)

        assert result["total"] == len(users["items"])
        assert result["page"] == 1
        assert result["pages"] == 1
        assert result["size"] == 50 # дефолтное значение, которое возвращает пагинация фаст апи
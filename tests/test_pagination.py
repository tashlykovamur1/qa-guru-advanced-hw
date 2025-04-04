from http import HTTPStatus

import pytest
from fastapi_pagination import Page

from app.models.User import User
from clients.users_api import UsersApi


@pytest.mark.pagination
class TestUsersPagination:
    @pytest.mark.parametrize("page1, page2, size", [
        (1, 2, 5),
        (2, 3, 5),
        (1, 2, 10),
    ])
    def test_pagination_different_pages(self, users_api: UsersApi, page1: int, page2: int, size: int):
        """Проверка, что разные страницы возвращают разные данные"""

        page1_response = users_api.get_users(params={"page": page1, "size": size})
        assert page1_response.status_code == HTTPStatus.OK

        page2_response = users_api.get_users(params={"page": page2, "size": size})
        assert page2_response.status_code == HTTPStatus.OK

        page1_result = page1_response.json()
        page2_result = page2_response.json()

        for result in [page1_result, page2_result]:
            Page[User].model_validate(result)

        assert page1_result["items"] != page2_result["items"]

        # Проверка, что элементы на страницах уникальны
        page1_ids = {user["id"] for user in page1_result["items"]}
        page2_ids = {user["id"] for user in page2_result["items"]}

        assert page1_ids.isdisjoint(page2_ids), (
            f"Элементы на странице {page1} и странице {page2} пересекаются: "
            f"{page1_ids.intersection(page2_ids)}"
        )

    @pytest.mark.parametrize("size", [
        4,
        1,
        12,
    ])
    def test_pagination_total_pages(self, users_api: UsersApi, size: int, users: dict):
        """Проверка, что общее количество страниц вычисляется правильно"""

        response = users_api.get_users(params={"size": size})
        assert response.status_code == HTTPStatus.OK

        result = response.json()
        Page[User].model_validate(result)

        actual_pages = result["pages"]
        expected_pages = (len(users) + size - 1) // size

        assert actual_pages == expected_pages, (
            f"Ожидалось {expected_pages} страниц, но получено {actual_pages} "
            f"для size={size} и total_items={len(users)}"
        )

    def test_get_users_data_wo_pagination(self, users_api: UsersApi, users: dict):
        """Проверка, что общее количество записей без пагинации вычисляется правильно"""

        response = users_api.get_users()
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        Page[User].model_validate(result)

        assert result["total"] == len(users)
        assert result["page"] == 1
        assert result["pages"] == 1
        assert result["size"] == 50  # дефолтное значение, которое возвращает пагинация фаст апи

    @pytest.mark.parametrize("page, size", [
        (1, 10),
        (5, 5),
        (3, 5),
        (1, 1)
    ])
    def test_pagination_with_diff_size_and_page(self, users_api: UsersApi, page: int, size: int, users: dict):
        response = users_api.get_users(params={"page": page, "size": size})
        assert response.status_code == HTTPStatus.OK

        result = response.json()
        Page[User].model_validate(result)

        assert result["total"] == len(users)
        assert result["page"] == page
        assert result["pages"] == (len(users) + size - 1) // size
        assert result["size"] == size

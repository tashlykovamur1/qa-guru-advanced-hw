from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException
from fastapi_pagination import add_pagination, Page

from app.database import users_db
from app.models.User import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users")
add_pagination(router)


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User | None:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users_db.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users() -> Iterable[User]:
    return users_db.get_users()

@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    try:
        UserCreate.model_validate(user.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(exc))

    return users_db.create_user(user)

@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    try:
        UserUpdate.model_validate(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return users_db.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int) -> dict[str, str]:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    users_db.delete_user(user_id)
    return {"message": "User deleted"}
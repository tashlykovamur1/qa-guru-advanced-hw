from fastapi import APIRouter
from http import HTTPStatus

from app.database import users_db
from app.models.AppStatus import AppStatus

router = APIRouter()

@router.get("", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users_db))
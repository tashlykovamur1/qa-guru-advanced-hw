from requests import Response

from clients.base.base_session import BaseSession
from config import Server


class UsersApi:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).app)

    def get_user(self, user_id: int) -> Response:
        return self.session.get(f'/api/users/{user_id}')

    def get_users(self, params: dict = None) -> Response:
        return self.session.get('/api/users/', params=params)

    def create_user(self, json: dict) -> Response:
        return self.session.post('/api/users/', json=json)

    def update_user(self, user_id: int, json: dict) -> Response:
        return self.session.patch(f'/api/users/{user_id}', json=json)

    def delete_user(self, user_id: int) -> Response:
        return self.session.delete(f'/api/users/{user_id}')

    def get_app_status(self) -> Response:
        return self.session.get('/status')

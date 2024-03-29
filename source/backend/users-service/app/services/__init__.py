from .auth import AuthenticationService
from .user import UserService


class Service:
    def __init__(self):
        self._user = UserService
        self._auth = AuthenticationService

    @property
    def user(self):
        return self._user

    @property
    def auth(self):
        return self._auth


service = Service()

__all__ = ["service"]

from abc import ABC, abstractmethod

from ..models import User, RefreshSession


class ISpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, user):
        raise NotImplementedError


class UserIDSpecification(ISpecification):
    def __init__(self, id) -> None:
        self._id = id

    def is_satisfied_by(self, user):
        return user.id == self._id


class UserEmailSpecification(ISpecification):
    def __init__(self, email) -> None:
        self._email = email

    def is_satisfied_by(self, user: User):
        return user.email == self._email


class RefreshTokenSpecification(ISpecification):
    def __init__(self, refresh_token) -> None:
        self._refresh_token = refresh_token

    def is_satisfied_by(self, refresh_session: RefreshSession):
        return refresh_session.refresh_token == self._refresh_token

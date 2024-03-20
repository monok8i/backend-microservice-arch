from abc import ABC, abstractmethod


class ISpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, user):
        raise NotImplementedError

    @abstractmethod
    def and_(self, other):
        pass

    @abstractmethod
    def or_(self, other):
        pass

    @abstractmethod
    def not_(self):
        pass


class UserIDSpecification(ISpecification):
    def __init__(self, id) -> None:
        self._id = id

    def is_satisfied_by(self, user):
        return user.id == self._id

    def and_(self, other):
        pass

    def or_(self, other):
        pass

    def not_(self):
        pass


class UserEmailSpecification(ISpecification):
    def __init__(self, email) -> None:
        self._email = email

    def is_satisfied_by(self, user):
        return user.email == self._email

    def and_(self, other):
        pass

    def or_(self, other):
        pass

    def not_(self):
        pass

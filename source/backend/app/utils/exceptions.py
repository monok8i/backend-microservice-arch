from typing import TypeVar, Optional

from fastapi import HTTPException, status

from ..utils.specification import ISpecification

SpecificationType = TypeVar("SpecificationType", bound=ISpecification)


class UserNotFoundException(HTTPException):
    def __init__(self, spec: Optional[SpecificationType] = None) -> None:
        self._spec = spec

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User found"
            if not self._spec
            else f"No User found with your specification {self._spec.__class__.__name__}",
        )


class UserAlreadyExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists in our system",
        )


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

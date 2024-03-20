from typing import Any

from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, spec: Any) -> None:
        self._spec = spec

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User found with your specification {self._spec.__class__.__name__}",
        )


class UserAlreadyExists(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists in our system",
        )

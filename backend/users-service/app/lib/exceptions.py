from typing import Any

from litestar.connection import Request
from litestar.middleware.exceptions.middleware import ExceptionResponseContent
from litestar.response import Response

from email_validator.exceptions_types import EmailNotValidError

from advanced_alchemy.exceptions import IntegrityError

from litestar.exceptions import (
    HTTPException,
    InternalServerException,
    NotFoundException,
    PermissionDeniedException,
)
from litestar.middleware.exceptions._debug_response import create_debug_response
from litestar.middleware.exceptions.middleware import create_exception_response
from litestar.repository.exceptions import ConflictError, NotFoundError, RepositoryError

from litestar import status_codes


class _HTTPConflictException(HTTPException):
    """Request conflict with the current state of the target resource."""

    status_code = status_codes.HTTP_409_CONFLICT


class ApplicationError(Exception):
    """Base exception type for the lib's custom exception types."""

    detail: str

    def __init__(self, *args: Any, detail: str = "") -> None:
        """Initialize ``AdvancedAlchemyException``.

        Args:
            *args: args are converted to :class:`str` before passing to :class:`Exception`
            detail: detail of the exception.
        """
        str_args = [str(arg) for arg in args if arg]
        if not detail:
            if str_args:
                detail, *str_args = str_args
            elif hasattr(self, "detail"):
                detail = self.detail
        self.detail = detail
        super().__init__(*str_args)

    def __repr__(self) -> str:
        if self.detail:
            return f"{self.__class__.__name__} - {self.detail}"
        return self.__class__.__name__

    def __str__(self) -> str:
        return " ".join((*self.args, self.detail)).strip()


def exception_to_http_response(
    request: Request[Any, Any, Any],
    exc: ApplicationError | RepositoryError,
) -> Response[ExceptionResponseContent]:
    """Transform repository exceptions to HTTP exceptions.

    Args:
        request: The request that experienced the exception.
        exc: Exception raised during handling of the request.

    Returns:
        Exception response appropriate to the type of original exception.
    """
    http_exc: type[HTTPException]
    if isinstance(exc, NotFoundError):
        http_exc = NotFoundException
    elif isinstance(exc, ConflictError | RepositoryError | IntegrityError):
        http_exc = _HTTPConflictException
    # elif isinstance(exc, AuthorizationError):
    #     http_exc = PermissionDeniedException
    else:
        http_exc = InternalServerException
    if request.app.debug and http_exc not in (
        PermissionDeniedException,
        NotFoundError,
        # AuthorizationError,
    ):
        return create_debug_response(request, exc)
    return create_exception_response(request, http_exc(detail=str(exc.__cause__)))


class IntegrityException(HTTPException):
    status_code = status_codes.HTTP_409_CONFLICT


class EmailValidationException(HTTPException, EmailNotValidError):
    status_code = status_codes.HTTP_400_BAD_REQUEST

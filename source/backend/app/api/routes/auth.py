from typing import Annotated  # noqa: I001

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import UnitOfWorkContext
from ... import schemas
from ...core.settings import config
from ...services import AuthenticationService
from ...utils.exceptions import InvalidTokenException

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def access_token(
    response: Response,
    uow: UnitOfWorkContext,
    *,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> schemas.Token:
    user = await AuthenticationService.authenticate_user(
        uow, email=credentials.username, password=credentials.password
    )

    token = await AuthenticationService.create_token(uow, user.id)

    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=config.Authentication().REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
        httponly=True,
    )

    return schemas.Token(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=config.Authentication().TOKEN_TYPE,
    )


@router.post("/refresh", response_model=schemas.Token)
async def refresh_access_token(
    request: Request,
    uow: UnitOfWorkContext,
) -> schemas.Token:
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise InvalidTokenException

    return await AuthenticationService.refresh_token(uow, refresh_token=refresh_token)


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    uow: UnitOfWorkContext,
) -> None:
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise InvalidTokenException

    response.delete_cookie("refresh_token", httponly=True)

    await AuthenticationService.logout(uow, refresh_token=refresh_token)

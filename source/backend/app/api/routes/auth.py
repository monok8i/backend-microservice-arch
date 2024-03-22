from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import UnitOfWorkContext
from ... import schemas
from ...core.settings import config
from ...services import AuthenticationService
from ...utils.exceptions import InvalidCredentialsException

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(
    response: Response,
    uow: UnitOfWorkContext,
    *,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> schemas.Token:
    user = await AuthenticationService.authenticate_user(
        uow, email=credentials.username, password=credentials.password
    )
    if not user:
        raise InvalidCredentialsException

    token = await AuthenticationService.create_token(uow, user.id)

    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=config.Authentication().ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=config.Authentication().REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
        httponly=True,
    )

    return schemas.Token(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=schemas.Token)
async def login(
    request: Request,
    response: Response,
    uow: UnitOfWorkContext,
) -> schemas.Token:
    refreshed_token = await AuthenticationService.refresh_token(
        uow, refresh_token=request.cookies.get("refresh_token")
    )

    response.set_cookie(
        "access_token",
        refreshed_token.access_token,
        max_age=config.Authentication().ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        refreshed_token.refresh_token,
        max_age=config.Authentication().REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
        httponly=True,
    )

    return refreshed_token


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    uow: UnitOfWorkContext,
) -> None:
    refresh_token = request.cookies.get("refresh_token")

    response.delete_cookie("access_token", httponly=True)
    response.delete_cookie("refresh_token", httponly=True)

    await AuthenticationService.logout(uow, refresh_token=refresh_token)

    return None

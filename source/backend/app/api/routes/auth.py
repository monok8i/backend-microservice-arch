from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import UnitOfWorkContext
from ... import schemas
from ...services import AuthenticationService

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(
    uow: UnitOfWorkContext,
    *,
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> schemas.Token:
    user = await AuthenticationService.authenticate_user(
        uow, email=auth_data.username, password=auth_data.password
    )

    return schemas.Token(
        access_token=AuthenticationService.encode_jwt_token(user.id),
        token_type="Bearer",
    )

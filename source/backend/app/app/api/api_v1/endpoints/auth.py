from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..deps import DatabaseSession
from ... import crud
from ...core import security
from ...schemas import Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
        db_session: DatabaseSession,
        *,
        auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await crud.user.authenticate(
        db_session, email=auth_data.username, password=auth_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user data (email or password)",
        )

    return Token(access_token=security.encode_jwt_token(user.id), token_type="Bearer")

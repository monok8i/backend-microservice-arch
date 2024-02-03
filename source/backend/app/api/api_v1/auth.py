from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ... import crud, schemas
from ...api import deps
from ...core import security

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(
    db_session: AsyncSession = Depends(deps.async_session),
    *,
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await crud.user.authenticate(
        db_session, email=auth_data.username, password=auth_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user data (email or password)",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive"
        )

    return schemas.Token(
        access_token=security.encode_jwt_token(user.user_id), token_type="Bearer"
    )


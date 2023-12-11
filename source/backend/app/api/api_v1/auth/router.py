from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from source.backend.app.core import security
from source.backend.app import crud, schemas
from source.backend.app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Token)
async def login(
    db_session: AsyncSession = Depends(deps.async_session),
    *,
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await crud.user.authenticate(db_session, email=auth_data.username, password=auth_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect user data (email or password)")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")

    return schemas.Token(
        access_token=security.encode_jwt_token(user.user_id),
        token_type='Bearer'
    )

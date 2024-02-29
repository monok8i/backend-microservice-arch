from typing import AsyncGenerator, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from ..core import security
from ..core.settings import settings
from ..infrastructure.postgres.setup import async_engine
from ..models import User
from ..schemas import TokenPayload


async def async_session() -> AsyncGenerator:
    session = async_sessionmaker(bind=async_engine(), expire_on_commit=False)
    async with session() as session:
        yield session


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/auth/login")


DbSession = Annotated[AsyncSession, Depends(async_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(db_session: DbSession, token: TokenDep) -> User:
    try:
        payload = security.decode_jwt_token(token=token)
        token = TokenPayload(**payload)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token"
        )
    user = await db_session.scalar(select(User).filter(User.user_id == token.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")
    return current_user


CurrentUser = Annotated[User, Depends(get_current_active_user)]

import jwt
from typing import AsyncGenerator, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from source.backend.app.core import settings, security
from source.backend.app.infrastructure.postgres.setup import async_engine
from source.backend.app.models import User
from source.backend.app.schemas import TokenPayload


async def async_session() -> AsyncGenerator:
    session = async_sessionmaker(bind=async_engine(), expire_on_commit=False)
    async with session() as session:
        yield session


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1}/login/"
)


DbSession = Annotated[AsyncSession, Depends(async_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(db_session: DbSession, token: TokenDep) -> User:
    try:
        payload = security.decode_jwt_token(token=token)
        token = TokenPayload(**payload)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token"
        )
    user = await db_session.scalar(select(User).filter(User.user_id == token.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")
    return current_user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


from typing import AsyncGenerator, Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .. import crud
from ..core import security
from ..core.settings import settings
from ..infrastructure.postgres.setup import async_engine
from ..models.users import User
from ..schemas.token import TokenPayload


# generator for async database session
async def async_session() -> AsyncGenerator:
    session = async_sessionmaker(bind=async_engine(), expire_on_commit=False)
    async with session() as session:
        yield session


# reusable URL for receiving auth token from user
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/auth/login")

# put async context in variable using Annotated special form
DatabaseSession = Annotated[AsyncSession, Depends(async_session)]

# put auth token in variable using Annotated special form
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(
    db_session: DatabaseSession, token: TokenDep
) -> Union[User, HTTPException]:
    """
    `get_current_user` function checks whether is authenticated user on his client
    :param db_session: Async database session
    :param token: Auth. token
    :return: ORM user object if he is authenticated, else raise exception
    """
    try:
        payload = security.decode_jwt_token(token=token)
        token = TokenPayload(**payload)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token"
        )
    user = await crud.user.get(db_session, obj_id=token.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")

    return user


# put result of function in variable using `Annotated` special form
CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_super_user(
    db_session: DatabaseSession, current_user: CurrentUser
) -> Union[User, HTTPException]:
    """
    `get_super_user` checks if the user has `super` privileges
    :param db_session: Async database session
    :param current_user: Current
    :return: result of `get_current_user` function
    """
    if current_user.is_superuser:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You aren't a SuperUser"
    )


# put result of function in variable using `Annotated` special form
CurrentSuperUser = Annotated[User, Depends(get_super_user)]

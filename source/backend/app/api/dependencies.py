from typing import Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status

from ..core.settings import config
from ..models import User
from ..schemas.token import TokenPayload
from ..services import UserService, AuthenticationService
from ..utils import UnitOfWork
from ..utils.exceptions import InvalidTokenException
from ..utils.security import OAuth2PasswordBearerWithCookie

# unit of work context
UnitOfWorkContext = Annotated[UnitOfWork, Depends(UnitOfWork)]

# reusable URL for receiving auth token from user
oauth2 = OAuth2PasswordBearerWithCookie(tokenUrl=f"{config.API_V1}/auth/login")

# put auth token in variable using Annotated special form
TokenDep = Annotated[str, Depends(oauth2)]


async def get_current_user(
    uow: UnitOfWorkContext, token: TokenDep
) -> Union[User, HTTPException]:
    """
    `get_current_user` function checks whether is authenticated user on his client

    :param uow: The dependency injection unit of work context
    :param token: Auth. token
    :return: ORM user object if he is authenticated, else raise exception
    """
    try:
        payload = AuthenticationService.decode_jwt_token(token=token)
        token = TokenPayload(**payload)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token"
        )
    user = await UserService.get_by_id(uow, user_id=token.sub)

    if not user:
        raise InvalidTokenException

    return user


# put result of function in variable using `Annotated` special form
CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_super_user(current_user: CurrentUser) -> Union[User, HTTPException]:
    """
    `get_super_user` checks if the user has `super` privileges
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

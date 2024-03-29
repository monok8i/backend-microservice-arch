from typing import Annotated, Union  # noqa: I001

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..core import settings as config
from ..database.uow import UnitOfWork
from ..models import User
from ..schemas.token import TokenPayload
from ..services import service
from ..utils.exceptions import InvalidTokenException

# unit of work context
UnitOfWorkContext = Annotated[UnitOfWork, Depends(UnitOfWork)]

# reusable URL for receiving auth token from user
oauth2 = OAuth2PasswordBearer(tokenUrl=f"{config.common.API_V1}/auth/login")

# put auth token in variable using Annotated special form
TokenDep = Annotated[str, Depends(oauth2)]


async def get_current_user(
        uow: UnitOfWorkContext, token: TokenDep
) -> Union[User, HTTPException]:
    try:
        payload = service.auth.decode_jwt_token(token=token)
        token = TokenPayload(**payload)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user = await service.user.get_by_id(uow, user_id=token.sub)

    if not user:
        raise InvalidTokenException

    return user


# put result of function in variable using `Annotated` special form
CurrentUser = Annotated[User, Depends(get_current_user)]

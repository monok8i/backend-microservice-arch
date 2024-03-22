from typing import Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(*, user_password: str, hashed_password: str) -> bool:
    """
    `verify_password` function checks whether the received cache is the specified term
    :param user_password: password original string
    :param hashed_password: hashed password
    :return: ``True`` if the hashed term is the specified user term, else ``None``
    """
    return hash_context.verify(user_password, hashed_password)


def generate_hashed_password(*, password: str) -> str:
    """
    `generate_hashed_password` function generates a hash based on the password string
    :param password: Password string which must be hashed
    :return: A hashed string
    """
    return hash_context.hash(password)


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param

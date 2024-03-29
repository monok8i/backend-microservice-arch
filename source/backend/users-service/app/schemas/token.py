from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Union[int, None] = None


class RefreshSessionCreate(BaseModel):
    refresh_token: str
    expires_in: int
    user_id: int


class RefreshSessionUpdate(BaseModel):
    refresh_token: str
    expires_in: int

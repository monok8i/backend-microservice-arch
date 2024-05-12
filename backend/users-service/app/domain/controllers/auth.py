from typing import Annotated
from litestar import post
from litestar.params import Parameter
from litestar.controller import Controller

from app.domain.schemas import Token
from app.lib.security.jwt import encode_jwt_token


class AuthController(Controller):
    #     dependencies = {"service": Provide(provide_auth_service)}
    #     signature_namespace = {"AuthService": AuthService}
    #     path = "/auth"
    #     return_dto = UserOutputDTO
    #     tags = ["users endpoints"]
    path = "/auth"

    @post("/token")
    async def jwt_token(
        self,
        user_id: Annotated[
            int,
            Parameter(
                title="User ID",
                description="Get user with specific identifier",
                required=True,
            ),
        ],
    ) -> Token:
        token = encode_jwt_token(subject=str(user_id))

        return Token(token=token, token_type="bearer")

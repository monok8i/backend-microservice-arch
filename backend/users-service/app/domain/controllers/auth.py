from typing import Annotated
from litestar import Response, post
from litestar.di import Provide
from litestar.params import Body
from litestar.controller import Controller
from litestar.enums import RequestEncodingType
from litestar.security.jwt import OAuth2Login

from app.domain.services import UserService
from app.domain.schemas import PydanticUserCredentials
from app.domain.dependencies import provide_users_service
from app.domain.guards import o2auth


class AuthController(Controller):
    dependencies = {"user_service": Provide(provide_users_service)}
    path = "/auth"
    tags = ["auth"]
    signature_namespace = {
        "UserService": UserService,
        "OAuth2Login": OAuth2Login,
        "RequestEncodingType": RequestEncodingType,
        "Body": Body,
    }

    @post("/login")
    async def jwt_token(
        self,
        user_service: UserService,
        data: Annotated[
            PydanticUserCredentials,
            Body(title="OAuth2 Login", media_type=RequestEncodingType.URL_ENCODED),
        ],
    ) -> Response[OAuth2Login]:
        user = await user_service.authenticate(data)

        return o2auth.login(str(user.id))

    @post("/logout")
    async def logout(self) -> dict:
        return {"ok": True}

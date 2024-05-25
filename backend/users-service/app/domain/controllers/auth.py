from typing import Annotated

from litestar import Request, Response, post
from litestar.exceptions import HTTPException
from litestar.di import Provide
from litestar.params import Body
from litestar.controller import Controller
from litestar.enums import RequestEncodingType
from litestar.security.jwt import OAuth2Login

from app.core import settings
from app.domain.services import RefreshTokenService, UserService
from app.domain.schemas import PydanticUserCredentials
from app.domain.dependencies import provide_users_service, provide_refresh_token_service
from app.domain.guards import o2auth
from app.lib.security.jwt import generate_refresh_token


class AuthController(Controller):
    dependencies = {
        "user_service": Provide(provide_users_service),
        "refresh_token_service": Provide(provide_refresh_token_service),
    }
    path = "/auth"
    tags = ["auth"]
    signature_namespace = {
        "UserService": UserService,
        "OAuth2Login": OAuth2Login,
        "RequestEncodingType": RequestEncodingType,
        "Body": Body,
    }

    @post("/login/access-token")
    async def jwt_token(
        self,
        user_service: UserService,
        refresh_token_service: RefreshTokenService,
        data: Annotated[
            PydanticUserCredentials,
            Body(title="OAuth2 Login", media_type=RequestEncodingType.URL_ENCODED),
        ],
    ) -> Response:
        # create user
        user = await user_service.authenticate(data)
        # create refresh_token in db and return it in cookie
        response = o2auth.login(str(user.id))

        refresh_token = generate_refresh_token()

        if not user.refresh_token:
            refresh_token = await refresh_token_service.create(user.id)

        response.set_cookie(
            "refresh_token",
            value=refresh_token,
            max_age=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
            httponly=True,
        )

        return response

    @post("/logout/access-token")
    async def logout(
        self, request: Request, refresh_token_service: RefreshTokenService
    ) -> Response:
        request.headers.pop("Authorization", None)
        refresh_token = request.cookies.pop("refresh_token", None)

        response = Response(content={"Logout": "Ok"}, status_code=200)

        response.delete_cookie("refresh_token")
        _ = await refresh_token_service.delete(refresh_token)

        return response

    @post("/refresh/access-token")
    async def refresh_tken(
        self,
        request: Request,
        refresh_token_service: RefreshTokenService,
    ) -> dict:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                detail="Couldn't find refresh_token in cookies", status_code=404
            )

        access_token_header = request.headers.get("Authorization")
        if not access_token_header:
            raise HTTPException(
                detail="Authorization header with expired access token must be in request"
            )

        new_access_token = await refresh_token_service.refresh_access_token(
            refresh_token, access_token_header
        )

        return Response(
            headers={"Authotization": f"Bearer {new_access_token}"}, status_code=200
        )

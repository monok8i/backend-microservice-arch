from typing import Annotated

from litestar import Request, Response, post
from litestar.controller import Controller
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.security.jwt import OAuth2Login

from app.core import settings
from app.database.models import User
from app.domain.dependencies import provide_refresh_token_service, provide_users_service
from app.domain.guards import o2auth
from app.domain.schemas import (
    PydanticUserCreate,
    PydanticUserCredentials,
    UserOutputDTO,
)
from app.domain.services import RefreshTokenService, UserService
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

    @post("/register", return_dto=UserOutputDTO)
    async def register_user(
        self,
        request: Request,
        user_service: UserService,
        data: Annotated[
            PydanticUserCreate,
            Body(title="Register", description="Register a new user"),
        ],
    ) -> User:
        user = await user_service.create(data=data)
        request.app.emit(
            "user_created",
            email=user.email,
            emails_broker=request.app.dependencies.get("emails_broker"),
        )

        return user

    @post("/login")
    async def login_user(
        self,
        user_service: UserService,
        refresh_token_service: RefreshTokenService,
        data: Annotated[
            PydanticUserCredentials,
            Body(title="OAuth2 Login", media_type=RequestEncodingType.URL_ENCODED),
        ],
    ) -> Response:
        user = await user_service.authenticate(data)
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

    @post("/logout")
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
                detail="Authorization header with expired access token must be in request"  # noqa: E501
            )

        new_access_token = await refresh_token_service.refresh_access_token(
            refresh_token, access_token_header
        )

        return Response(
            headers={"Authotization": f"Bearer {new_access_token}"}, status_code=200
        )

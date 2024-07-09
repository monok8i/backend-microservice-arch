from litestar.types import ControllerRouterHandler

from app.domain.controllers import AuthController, UserController

route_handlers: list[ControllerRouterHandler] = [UserController, AuthController]

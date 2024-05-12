from app.domain.controllers import UserController, AuthController

from litestar.types import ControllerRouterHandler

route_handlers: list[ControllerRouterHandler] = [UserController, AuthController]

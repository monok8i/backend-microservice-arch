from app.domain.controllers import UserController

from litestar.types import ControllerRouterHandler

route_handlers: list[ControllerRouterHandler] = [UserController]

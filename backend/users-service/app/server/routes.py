from app.domain.users.controllers import UserController

from litestar.types import ControllerRouterHandler

route_handlers: list[ControllerRouterHandler] = [UserController]

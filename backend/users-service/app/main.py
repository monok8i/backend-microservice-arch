from litestar import Litestar
from litestar.middleware import DefineMiddleware

from app.lib.security.jwt import JWTAuthenticationMiddleware
from app.core.config import cache_config
from app.server.plugins import sqlalchemy_plugin, structlog_plugin
from app.server.routes import route_handlers

def create_app() -> Litestar:
    auth_middleware = DefineMiddleware(JWTAuthenticationMiddleware, exclude=["/api/schema", "/api/auth/"])

    return Litestar(
        path="/api",
        response_cache_config=cache_config,
        route_handlers=route_handlers,
        plugins=[sqlalchemy_plugin, structlog_plugin],
        middleware=[auth_middleware],
    )


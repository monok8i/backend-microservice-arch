from litestar import Litestar

from app.domain.guards import o2auth
from app.core.config import cache_config
from app.server.plugins import sqlalchemy_plugin, structlog_plugin
from app.server.routes import route_handlers

def create_app() -> Litestar:

    return Litestar(
        path="/api",
        response_cache_config=cache_config,
        route_handlers=route_handlers,
        plugins=[sqlalchemy_plugin, structlog_plugin],
        on_app_init=[o2auth.on_app_init],
        middleware=[o2auth.middleware],
    )


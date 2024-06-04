from litestar import Litestar

from app.lib.dependencies import create_collection_dependencies
from app.domain.guards import o2auth
from app.domain import listeners
from app.core.config import cache_config
from app.server import events
from app.server.plugins import sqlalchemy_init_plugin, structlog_plugin, rabbitmq_plugin
from app.server.routes import route_handlers


def create_app() -> Litestar:
    dependencies = create_collection_dependencies()

    return Litestar(
        path="/api",
        dependencies=dependencies,
        response_cache_config=cache_config,
        route_handlers=route_handlers,
        plugins=[sqlalchemy_init_plugin, structlog_plugin, rabbitmq_plugin],
        on_app_init=[o2auth.on_app_init],
        middleware=[o2auth.middleware],
        listeners=[listeners.user_created],
        lifespan=[events.lifespan]
    )

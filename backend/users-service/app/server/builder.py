from litestar import Litestar

from app.lib.dependencies import create_collection_dependencies
from app.domain.guards import o2auth
from app.domain import listeners

from app.core.config import cache_config

from . import events
from .plugins import sqlalchemy_init_plugin, rabbitmq_plugin, structlog_plugin
from .routes import route_handlers


def configure_app() -> Litestar:
    dependencies = create_collection_dependencies()

    return Litestar(
        path="/api",
        dependencies=dependencies,
        response_cache_config=cache_config,
        route_handlers=route_handlers,
        plugins=[sqlalchemy_init_plugin, rabbitmq_plugin, structlog_plugin],
        on_app_init=[o2auth.on_app_init],
        middleware=[o2auth.middleware],
        listeners=[listeners.user_created],
        lifespan=[events.lifespan],
    )

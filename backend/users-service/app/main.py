from litestar import Litestar

from app.lib.plugins import sqlalchemy_plugin, structlog_plugin
from app.lib.dependencies import provide_dependencies
from app.server.routes import route_handlers


dependencies = provide_dependencies()

app = Litestar(
    route_handlers=route_handlers,
    dependencies=dependencies,
    plugins=[sqlalchemy_plugin, structlog_plugin],
)

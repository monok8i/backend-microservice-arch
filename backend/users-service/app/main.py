from litestar import Litestar

from app.server.plugins import sqlalchemy_plugin, structlog_plugin
from app.server.routes import route_handlers

app = Litestar(
    path="/api",
    route_handlers=route_handlers,
    plugins=[sqlalchemy_plugin, structlog_plugin],
)

from litestar import Litestar

from app.server.builder import configure_app


def create_app() -> Litestar:
    return configure_app()

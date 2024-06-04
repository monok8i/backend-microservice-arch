from typing import Any, AsyncGenerator  # , Callable
from dataclasses import dataclass
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.config.app import AppConfig
from litestar.plugins import InitPluginProtocol

from pika import ConnectionParameters, PlainCredentials, BlockingConnection


@dataclass(kw_only=True, frozen=True)
class RabbitMQConfig:
    host: str = "localhost"
    port: int = 5672
    vhost: str = "/"
    credentials: dict[str, str] = None
    connection: type[BlockingConnection] = None

    dependency_key: str = "rmq_session"

    def create_connection(
        self,
        # on_open_callback: Callable[[], Any] = None,
        # on_open_error_callback: Callable[[], Any] = None,
        # on_close_callback: Callable[[], Any] = None,
    ) -> BlockingConnection:
        if not self.connection:
            if not self.credentials:
                return BlockingConnection(
                    parameters=ConnectionParameters(
                        host=self.host,
                        port=self.port,
                        virtual_host=self.vhost,
                    ),
                    # on_open_callback=on_open_callback,
                    # on_open_error_callback=on_open_error_callback,
                    # on_close_callback=on_close_callback,
                )
            return BlockingConnection(
                parameters=ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.vhost,
                    credentials=PlainCredentials(
                        username=self.credentials.get("username"),
                        password=self.credentials.get("password"),
                    ),
                ),
                # on_open_callback=on_open_callback,
                # on_open_error_callback=on_open_error_callback,
                # on_close_callback=on_close_callback,
            )

        return self.connection

    @asynccontextmanager
    async def lifespan(self, app: Litestar) -> AsyncGenerator[None, None]:
        try:
            app.state.update(self.create_state_keys())
            yield
        except Exception as e:
            raise (e)
        finally:
            del app.state[self.dependency_key]

    def create_state_keys(self) -> dict[str, Any]:
        return {self.dependency_key: self.create_connection}


class RabbitMQPlugin(InitPluginProtocol):
    def __init__(self, config: RabbitMQConfig) -> None:
        self._config = config

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        # app_config.lifespan.append(self._config.lifespan)
        app_config.state.update(self._config.create_state_keys())
        return app_config


print(type(RabbitMQConfig().create_connection))

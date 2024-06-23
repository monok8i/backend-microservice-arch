from dataclasses import dataclass
from typing import Any

from litestar.config.app import AppConfig
from litestar.plugins import InitPluginProtocol

from aio_pika.abc import AbstractConnection
from aio_pika.connection import connect


@dataclass(kw_only=True, frozen=True)
class RabbitMQConfig:
    host: str = "localhost"
    port: int = 5672
    vhost: str = "/"
    credentials: dict[str, str] = None
    connection: type[AbstractConnection] = None

    dependency_key: str = "rmq_session"

    async def create_connection(
        self,
    ) -> AbstractConnection:
        if not self.connection:
            return await connect(
                host=self.host,
                port=self.port,
                login=self.credentials.get("username"),
                password=self.credentials.get("password"),
                virtualhost=self.vhost,
            )

        return self.connection

    def create_state_keys(self) -> dict[str, Any]:
        return {self.dependency_key: self.create_connection}

class RabbitMQPlugin(InitPluginProtocol):
    def __init__(self, config: RabbitMQConfig) -> None:
        self._config = config

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.dependencies.update(self._config.create_state_keys())
        return app_config

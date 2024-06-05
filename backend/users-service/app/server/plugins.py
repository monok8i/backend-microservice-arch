from litestar.plugins.sqlalchemy import SQLAlchemyInitPlugin
from litestar.plugins.structlog import StructlogPlugin

from app.core.config import alchemy_config, log_config, rabbitmq_config
from app.lib.broker.rmq_plugin import RabbitMQPlugin

sqlalchemy_init_plugin = SQLAlchemyInitPlugin(config=alchemy_config)
structlog_plugin = StructlogPlugin(config=log_config)
rabbitmq_plugin = RabbitMQPlugin(config=rabbitmq_config)

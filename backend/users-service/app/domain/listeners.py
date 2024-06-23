import logging

from litestar.events import listener

from app.utils.message_brokers import RabbitMQPublisher
from .dependencies import provide_message_broker

from aio_pika import Connection

logger = logging.getLogger(__name__)


@listener("user_created")
async def user_created(email: str, broker_connection: Connection) -> bool:
    try:
        broker: RabbitMQPublisher = await anext(provide_message_broker(broker_connection))

        async with broker as rmq:
            message = await rmq.publish_message(body=email)
            print(message)

        logger.info("Email successfully sended to broker")

    except Exception as e:
        logger.error(str(e))


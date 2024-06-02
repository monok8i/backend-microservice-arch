import logging

# from litestar import Request
from litestar.events import listener
from litestar.datastructures import State

from .dependencies import provide_message_broker

logger = logging.getLogger(__name__)


@listener("user_created")
async def user_created(email: str, state: State) -> bool:
    try:
        connection = state.rmq_session()
        broker = await anext(provide_message_broker(connection))

        with broker as rmq:
            rmq.send_message(email)

        logger.info("Email successfully sended to broker")

    except Exception as e:
        logger.error(str(e))


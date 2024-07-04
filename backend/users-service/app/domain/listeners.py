import logging

from litestar.events import listener

from app.utils.message_brokers.brokers import EmailsMessageBroker

logger = logging.getLogger(__name__)


@listener("user_created")
async def user_created(email: str, emails_broker: EmailsMessageBroker) -> bool:
    try:
        message = await emails_broker.publish(queue="emails", body=email)

        logger.info(message)
        logger.info("Email successfully sended to broker")

    except Exception as e:
        logger.error(str(e))

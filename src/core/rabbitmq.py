import json
from dataclasses import dataclass

import aio_pika
import structlog

from src.core import app_settings
from src.domain.value_objects import TaskPriority

logger = structlog.get_logger(__name__)


@dataclass(slots=True, eq=False)
class RabbitMQBase:
    queue_name = app_settings.RABBITMQ_QUEUE
    connection: aio_pika.abc.AbstractConnection | None = None
    channel: aio_pika.abc.AbstractChannel | None = None
    queue: aio_pika.abc.AbstractQueue | None = None

    async def startup(self):
        self.connection = await aio_pika.connect_robust(app_settings.RABBITMQ_URL)
        logger.info("RabbitMQ connection established successfully")

        self.channel = await self.connection.channel()
        logger.info(f"RabbitMQ channel {self.channel} established successfully")

        self.queue = await self._declare_queue()
        logger.info(f"RabbitMQ queue ({self.queue_name}) declared successfully")

    async def _declare_queue(self) -> aio_pika.abc.AbstractQueue:
        return await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={"x-max-priority": 10},
        )

    async def close(self):
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed successfully")


@dataclass(slots=True, eq=False)
class RabbitMQConsumer(RabbitMQBase):
    async def start_consuming(self, handler):
        await self.queue.consume(handler)
        logger.info("Worker started. Waiting for messages...")


@dataclass(slots=True, eq=False)
class RabbitMQProducer(RabbitMQBase):
    async def send_message(self, message: dict, priority: TaskPriority):
        msg = aio_pika.Message(
            body=json.dumps(message).encode(),
            priority=PRIORITY_MAP[priority],
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        logger.info(f"Sending message: {message}")

        await self.channel.default_exchange.publish(
            msg,
            routing_key=self.queue_name,
        )


PRIORITY_MAP = {
    TaskPriority.LOW: 1,
    TaskPriority.MEDIUM: 5,
    TaskPriority.HIGH: 9,
}

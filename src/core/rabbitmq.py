import json

import aio_pika

from src.core import app_settings
from src.models import TaskPriority

PRIORITY_MAP = {
    TaskPriority.LOW:    1,
    TaskPriority.MEDIUM: 5,
    TaskPriority.HIGH:   9,
}


class RabbitMQBase:
    queue_name = app_settings.RABBITMQ_QUEUE

    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue = None

    async def startup(self):
        self.connection = await aio_pika.connect_robust(app_settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()
        self.queue = await self._declare_queue()

    async def _declare_queue(self) -> aio_pika.Queue:
        return await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={"x-max-priority": 10},
        )

    async def close(self):
        if self.connection:
            await self.connection.close()


class RabbitMQProducer(RabbitMQBase):
    async def send_message(self, message: dict, priority: TaskPriority):
        msg = aio_pika.Message(
            body=json.dumps(message).encode(),
            priority=PRIORITY_MAP[priority],
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self.channel.default_exchange.publish(
            msg,
            routing_key=self.queue_name,
        )


class RabbitMQConsumer(RabbitMQBase):
    async def start_consuming(self, handler):
        await self.queue.consume(handler)

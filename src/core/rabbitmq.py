import json

import aio_pika

from src.core import app_settings
from src.models import TaskPriority

PRIORITY_MAP = {
    TaskPriority.LOW:    1,
    TaskPriority.MEDIUM: 5,
    TaskPriority.HIGH:   9,
}


class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = app_settings.RABBITMQ_QUEUE

    async def startup(self):
        self.connection = await aio_pika.connect_robust(app_settings.RABBITMQ_URL)
        self.channel = await self.connection.channel(publisher_confirms=True)
        await  self._setup_queue()

    async def _setup_queue(self):
        await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={"x-max-priority": 10}
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def send_message(self, message: dict, priority: TaskPriority):
        if not self.channel:
            raise RuntimeError("RabbitMQ not initialized")

        msg = aio_pika.Message(
            body=json.dumps(message).encode(),
            priority=PRIORITY_MAP[priority],
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await self.channel.default_exchange.publish(msg, routing_key=self.queue_name)


rabbitmq_client = RabbitMQClient()

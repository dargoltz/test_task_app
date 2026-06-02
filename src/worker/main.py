import asyncio
import json
import uuid

import aio_pika

from src.core import RabbitMQConsumer
from src.worker.logger import logger
from src.worker.task_processing import process_task


async def handler(message: aio_pika.IncomingMessage):
    async with message.process():
        msg = json.loads(message.body.decode())

        logger.info(f"Received message: {msg}")
        task_id = uuid.UUID(msg["task_id"])

        await process_task(task_id)


async def run_worker():
    rabbitmq_consumer = RabbitMQConsumer()
    await rabbitmq_consumer.startup()

    logger.info("Worker started")

    task = asyncio.create_task(
        rabbitmq_consumer.start_consuming(handler)
    )

    try:
        await task
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        logger.info("Worker stopping...")
        task.cancel()
        raise


if __name__ == "__main__":
    asyncio.run(run_worker())

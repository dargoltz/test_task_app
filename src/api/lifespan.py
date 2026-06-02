from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.core.rabbitmq import RabbitMQProducer


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq_producer = RabbitMQProducer()
    await rabbitmq_producer.startup()
    app.state.rabbitmq_producer = rabbitmq_producer
    yield
    await rabbitmq_producer.close()

from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.core.rabbitmq import RabbitMQProducer


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq = RabbitMQProducer()
    await rabbitmq.startup()
    app.state.rabbitmq = rabbitmq
    yield
    await rabbitmq.close()

from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.core.rabbitmq import rabbitmq_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_client.startup()
    yield
    await rabbitmq_client.close()

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import RabbitMQProducer
from src.persistence.db import get_db_session
from src.persistence.repositories import TaskRepository
from src.service import TaskService


async def get_db():
    async with get_db_session() as session:
        yield session


async def get_task_repository(
    session: AsyncSession = Depends(get_db),
) -> TaskRepository:
    return TaskRepository(session=session)


async def get_rabbitmq(request: Request):
    return request.app.state.rabbitmq


async def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
    rabbitmq: RabbitMQProducer = Depends(get_rabbitmq),
):
    return TaskService(repository=repository, rabbitmq=rabbitmq)

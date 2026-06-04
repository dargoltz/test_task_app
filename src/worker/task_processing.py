import asyncio
import random
import uuid

import structlog

from src.domain.exceptions import EntityNotFoundError, TaskExecutionError
from src.domain.models import Task
from src.persistence.db import get_db_session
from src.persistence.repositories import TaskRepository
from src.service import TaskStatusManager

logger = structlog.get_logger()


async def process_task(task_id: uuid.UUID):
    async with get_db_session() as session:
        repository = TaskRepository(session)

        try:
            task = await repository.get_by_id(task_id, for_update=True)
            logger.info(f"Task {task_id} found. Starting processing...")

            TaskStatusManager.start(task=task)
            await repository.update_status(task)

            result = await execute_task(task)

            TaskStatusManager.complete(task=task, result=result)
            await repository.update_status(task)

            logger.info(f"Task {task_id} completed successfully")

        except EntityNotFoundError:
            logger.error(f"Task {task_id} not found")
            return

        except (TaskExecutionError, ValueError) as e:
            logger.error(e)
            TaskStatusManager.fail(task=task, error=str(e))

            await repository.update_status(task)

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            TaskStatusManager.fail(task=task, error=str(e))

            await repository.update_status(task)


async def execute_task(task: Task) -> str:
    """
    Выполняет задачу за ~5 сек, возвращает лог об успешном выполнении задачи
    Падает в 10% случаев

    Args:
        task: задача
    """
    await asyncio.sleep(5)

    if random.randint(1, 10) > 9:
        raise TaskExecutionError(task.id)

    return f"Task {task.id} executed successfully"

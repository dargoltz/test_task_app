import asyncio
import datetime
import random
import uuid

from sqlalchemy import select

from src.core import get_db_session, TaskExecutionError
from src.models import TaskStatus, TaskORM
from src.worker.logger import logger


async def process_task(task_id: uuid.UUID):
    async with get_db_session() as session:
        task = (
            await session.execute(
                select(TaskORM)
                .where(TaskORM.id == task_id)
                .where(TaskORM.status == TaskStatus.PENDING)
                .with_for_update(skip_locked=True)
            )
        ).scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found")
            return

        task.started_at = datetime.datetime.now(datetime.timezone.utc)
        task.status = TaskStatus.IN_PROGRESS
        await session.flush()

        try:
            task.result = await execute_task(task.id)
            task.status = TaskStatus.COMPLETED

            logger.info(task.result)
        except TaskExecutionError as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED

            logger.info(task.error)
        except Exception as e:
            task.error = f"Unexpected error: {e}"
            task.status = TaskStatus.FAILED

            logger.info(task.error)

        task.finished_at = datetime.datetime.now(datetime.timezone.utc)
        await session.commit()


async def execute_task(task_id: uuid.UUID) -> str:
    """
    Выполняет задачу за ~5 сек, возвращает лог об успешном выполнении задачи
    Падает в 10% случаев

    Args:
        task_id: id задачи
    """
    await asyncio.sleep(5)

    if random.randint(1, 10) > 9:
        raise TaskExecutionError(task_id)

    return f"Task {task_id} executed successfully"

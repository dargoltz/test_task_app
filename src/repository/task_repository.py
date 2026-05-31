import uuid
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TaskORM, TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskORM) -> TaskORM:
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_list(self, page: int, limit: int) -> list[TaskORM]:
        offset = (page - 1) * limit

        result = await self.session.execute(
            select(TaskORM)
            .offset(offset)
            .limit(limit)
            .order_by(TaskORM.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_total(self) -> int:
        result = await self.session.execute(
            select(func.count(TaskORM.id))
        )
        return result.scalar_one()

    async def get_by_id(self, task_id: uuid.UUID) -> TaskORM | None:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.id == task_id)
        )
        return result.scalar_one_or_none()

    async def update_status_by_id(
        self,
        task_id: uuid.UUID,
        status: TaskStatus,
    ) -> None:
        await self.session.execute(
            update(TaskORM)
            .where(TaskORM.id == task_id)
            .values(status=status)
        )
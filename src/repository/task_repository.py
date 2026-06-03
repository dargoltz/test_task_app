import uuid
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import EntityNotFoundError
from src.dto import TaskFilterParameters
from src.models import TaskORM, TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskORM) -> TaskORM:
        self.session.add(task)
        await self.session.flush()
        return task

    @staticmethod
    def update_stmt_by_filter_params(stmt, filter_params: TaskFilterParameters):
        if filter_params.status:
            stmt = stmt.where(TaskORM.status == filter_params.status)

        if filter_params.priority:
            stmt = stmt.where(TaskORM.priority == filter_params.priority)

        return stmt

    async def get_list(self, filter_params: TaskFilterParameters) -> list[TaskORM]:
        stmt = (
            select(TaskORM)
            .offset(filter_params.offset)
            .limit(filter_params.limit)
            .order_by(TaskORM.created_at.desc())
        )

        filtered_stmt = self.update_stmt_by_filter_params(stmt, filter_params)

        result = await self.session.execute(filtered_stmt)
        return list(result.scalars().all())

    async def get_total(self, filter_params: TaskFilterParameters) -> int:
        stmt = (
            select(func.count(TaskORM.id))
        )

        filtered_stmt = self.update_stmt_by_filter_params(stmt, filter_params)

        result = await self.session.execute(filtered_stmt)
        return result.scalar_one()

    async def get_by_id(self, task_id: uuid.UUID) -> TaskORM:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.id == task_id)
        )

        found = result.scalar_one_or_none()

        if not found:
            raise EntityNotFoundError(TaskORM, task_id)

        return found

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

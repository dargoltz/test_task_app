import uuid
from dataclasses import dataclass

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.exceptions import EntityNotFoundError
from src.domain.models import Task
from src.domain.value_objects import TaskPriority, TaskStatus
from src.dto import Page, PageParameters, TaskFilterParameters
from src.persistence.orm_models import TaskORM


@dataclass(frozen=True, slots=True, eq=False)
class TaskRepository:
    session: AsyncSession

    @staticmethod
    def _domain_to_orm(domain: Task) -> TaskORM:
        return TaskORM(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            priority=domain.priority.value,
            status=domain.status.value,
            created_at=domain.created_at,
            started_at=domain.started_at,
            finished_at=domain.finished_at,
            result=domain.result,
            error=domain.error,
        )

    @staticmethod
    def _orm_to_domain(orm: TaskORM) -> Task:
        return Task(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            priority=TaskPriority(orm.priority),
            status=TaskStatus(orm.status),
            created_at=orm.created_at,
            started_at=orm.started_at,
            finished_at=orm.finished_at,
            result=orm.result,
            error=orm.error,
        )

    @staticmethod
    def _apply_filters(stmt, filter_params: TaskFilterParameters):
        if filter_params.status:
            stmt = stmt.where(TaskORM.status == filter_params.status.value)

        if filter_params.priority:
            stmt = stmt.where(TaskORM.priority == filter_params.priority.value)

        return stmt

    async def create(self, task: Task) -> Task:
        orm_obj = self._domain_to_orm(task)

        self.session.add(orm_obj)
        await self.session.commit()
        await self.session.refresh(orm_obj)

        return self._orm_to_domain(orm_obj)

    async def get_by_id(
        self, task_id: uuid.UUID, *, for_update: bool = False
    ) -> Task | None:
        stmt = select(TaskORM).where(TaskORM.id == task_id)

        if for_update:
            stmt = stmt.with_for_update()

        result = await self.session.execute(stmt)
        orm_obj = result.scalar_one_or_none()

        if not orm_obj:
            raise EntityNotFoundError(TaskORM, task_id)

        return self._orm_to_domain(orm_obj)

    async def _get_total(self, filter_params: TaskFilterParameters) -> int:
        stmt = select(func.count()).select_from(TaskORM)
        stmt = self._apply_filters(stmt, filter_params)

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_list(
        self,
        page_params: PageParameters,
        filter_params: TaskFilterParameters,
    ) -> Page[Task]:
        stmt = select(TaskORM)

        stmt = self._apply_filters(stmt, filter_params)

        stmt = (
            stmt.limit(page_params.limit)
            .offset(page_params.offset)
            .order_by(TaskORM.created_at)
        )

        result = await self.session.execute(stmt)
        orm_tasks = result.scalars().all()

        total = await self._get_total(filter_params)

        return Page(
            items=[self._orm_to_domain(t) for t in orm_tasks],
            total=total,
        )

    async def update_status(self, task: Task) -> None:
        stmt = (
            update(TaskORM)
            .where(TaskORM.id == task.id)
            .values(
                status=task.status.value,
                started_at=task.started_at,
                finished_at=task.finished_at,
                result=task.result,
                error=task.error,
            )
        )

        await self.session.execute(stmt)
        await self.session.commit()

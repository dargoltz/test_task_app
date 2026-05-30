import uuid

from src.core.db import DBSession
from src.models import TaskORM, TaskStatus


class TaskRepository:
    def __init__(self, session: DBSession):
        self.session = session

    async def create(self, task: TaskORM) -> TaskORM:
        pass

    async def get_list(self, page: int, limit: int) -> list[TaskORM]:
        pass

    async def get_total(self) -> int:
        pass

    async def get_by_id(self, task_id: uuid.UUID) -> TaskORM:
        pass

    async def update_status_by_id(self, task_id: uuid.UUID, status: TaskStatus):
        pass

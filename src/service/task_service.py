import uuid

from src.dto import TaskResponse, TaskRequest, PaginatedResponse
from src.models import TaskStatus
from src.repository.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task: TaskRequest) -> TaskResponse:
        task_orm = ...

        created = await self.repository.create(task_orm)

        task_response = ...

        return task_response

    async def get_task_list(self, page: int, limit: int) -> PaginatedResponse[TaskResponse]:
        task_list = await self.repository.get_list(page, limit)
        task_total = await self.repository.get_total()

        task_responses = ...

        return PaginatedResponse(
            page=page,
            limit=limit,
            items=task_responses,
            total=task_total
        )

    async def get_task(self, task_id: uuid.UUID) -> TaskResponse:
        task = await self.repository.get_by_id(task_id)

        task_response = ...

        return task_response

    async def get_task_status(self, task_id: uuid.UUID) -> TaskStatus:
        task = await self.repository.get_by_id(task_id)

        return task.status

    async def cancel_task(self, task_id: uuid.UUID) -> None:
        await self.repository.update_status_by_id(task_id, TaskStatus.CANCELLED)

        # todo cancel task execution if running

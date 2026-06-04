import datetime
import uuid
from dataclasses import dataclass

import structlog

from src.core import RabbitMQProducer
from src.domain.models import Task
from src.domain.value_objects import TaskStatus
from src.dto import PageParameters, TaskFilterParameters
from src.persistence.repositories import TaskRepository
from src.schemas.request import TaskRequest, TaskFilterQueryParameters, PaginationQueryParameters
from src.schemas.response import TaskResponse, PageResponse
from src.service.task_status_manager import TaskStatusManager

logger = structlog.get_logger()

@dataclass(frozen=True, slots=True, eq=False)
class TaskService:
    repository: TaskRepository
    rabbitmq: RabbitMQProducer

    @staticmethod
    def _domain_to_schema(domain: Task) -> TaskResponse:
        return TaskResponse.model_validate(domain)

    async def create_task(self, task: TaskRequest) -> TaskResponse:
        domain_task = Task(
            name=task.name,
            description=task.description,
            priority=task.priority,
            status=TaskStatus.NEW,
            created_at=datetime.datetime.now(),
        )

        created = await self.repository.create(domain_task)

        return self._domain_to_schema(created)

    async def run_task(self, task_id: uuid.UUID) -> None:
        logger.info(f"Running task {task_id}")

        task = await self.repository.get_by_id(task_id)

        TaskStatusManager.set_pending(task)
        await self.repository.update_status(task)

        await self._send_task_to_queue(task)

    async def _send_task_to_queue(self, task: Task) -> None:
        msg = {"task_id": str(task.id)}
        await self.rabbitmq.send_message(msg, task.priority)

    async def get_task(self, task_id: uuid.UUID) -> TaskResponse:
        task = await self.repository.get_by_id(task_id)

        return self._domain_to_schema(task)

    async def get_task_status(self, task_id: uuid.UUID) -> str:
        task = await self.repository.get_by_id(task_id)

        return task.status.value

    async def get_tasks(
        self,
        page_params: PaginationQueryParameters,
        filter_params: TaskFilterQueryParameters
    ) -> PageResponse[TaskResponse]:
        tasks_page = await self.repository.get_list(
            PageParameters(
                page=page_params.page,
                limit=page_params.limit,
            ),
            TaskFilterParameters(
                status=filter_params.status,
                priority=filter_params.priority,
            )
        )

        return PageResponse(
            page=page_params.page,
            limit=page_params.limit,
            items=[self._domain_to_schema(t) for t in tasks_page.items],
            total=tasks_page.total,
        )

    async def cancel_task(self, task_id: uuid.UUID) -> None:
        """
        Отменяет задачу до начала ее выполнения.

        В остальных случаях отмена не происходит по одной из двух причин:

        - задача уже завершена (выполнена, отменена)
        - задача уже запущена (в процессе выполнения)

        Args:
            task_id: id задачи
        """
        logger.info(f"Cancelling task {task_id}")

        task = await self.repository.get_by_id(task_id)

        TaskStatusManager.cancel(task)
        await self.repository.update_status(task)

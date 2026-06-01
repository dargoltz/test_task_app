import json
import uuid

from src.core import DBSession, TaskExecutionError, TaskCancelError, rabbitmq_client
from src.dto import TaskResponse, TaskRequest, PaginatedResponse
from src.models import TaskStatus, TaskORM
from src.repository import TaskRepository


class TaskService:
    def __init__(self, session: DBSession):
        self.session = session
        self.repository = TaskRepository(session)

    @staticmethod
    def _orm_to_response(task: TaskORM | None) -> TaskResponse:
        return TaskResponse.model_validate(task)

    async def create_task(self, task: TaskRequest) -> TaskResponse:
        """
        Создает и запускает задачу. Возвращает инфо о созданной задаче

        Args:
            task: тело запроса
        """
        task_orm = TaskORM(
            name=task.name,
            description=task.description,
            priority=task.priority,
            status=TaskStatus.NEW
        )
        created = await self.repository.create(task_orm)
        await self.session.commit()

        await self._send_task_to_queue(created)

        return self._orm_to_response(created)

    async def get_task_list(self, page: int, limit: int) -> PaginatedResponse[TaskResponse]:
        """
        Возвращает пагинированный список задач

        Args:
            page: номер страницы
            limit: количество задач на странице
        """
        task_list = await self.repository.get_list(page, limit)
        task_total = await self.repository.get_total()

        task_responses = [self._orm_to_response(task) for task in task_list]

        return PaginatedResponse(
            page=page,
            limit=limit,
            items=task_responses,
            total=task_total
        )

    async def get_task(self, task_id: uuid.UUID) -> TaskResponse:
        task = await self.repository.get_by_id(task_id)

        return self._orm_to_response(task)

    async def get_task_status(self, task_id: uuid.UUID) -> TaskStatus:
        task = await self.repository.get_by_id(task_id)

        return task.status

    async def cancel_task(self, task_id: uuid.UUID) -> None:
        """
        Отменяет задачу до начала ее выполнения.

        В остальных случаях отмена не происходит по двум причинам:

        - задача уже завершена (выполнена, отменена)
        - задача уже запущена (в процессе выполнения)

        Args:
            task_id: id задачи
        """
        found = await self.repository.get_by_id(task_id)

        if found.status in (TaskStatus.NEW, TaskStatus.PENDING):
            await self.repository.update_status_by_id(task_id, TaskStatus.CANCELLED)
        else:
            raise TaskCancelError(found.id, found.status)

        await self.session.commit()

    async def _send_task_to_queue(self, task: TaskORM):
        try:
            await rabbitmq_client.send_message({"task_id": str(task.id)}, task.priority)

            await self.repository.update_status_by_id(task.id, TaskStatus.PENDING)
        except Exception as exc:
            await self.repository.update_status_by_id(task.id, TaskStatus.FAILED)

            raise TaskExecutionError(task.id) from exc
        finally:
            await self.session.commit()

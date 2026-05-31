import uuid

from src.core import DBSession, EntityNotFoundError
from src.dto import TaskResponse, TaskRequest, PaginatedResponse
from src.models import TaskStatus, TaskORM
from src.repository.task_repository import TaskRepository


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

        # todo run task

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

        if not task:
            raise EntityNotFoundError(TaskORM, task_id)

        return self._orm_to_response(task)

    async def get_task_status(self, task_id: uuid.UUID) -> TaskStatus:
        task = await self.repository.get_by_id(task_id)

        if not task:
            raise EntityNotFoundError(TaskORM, task_id)

        return task.status

    async def cancel_task(self, task_id: uuid.UUID) -> None:
        """
        Отменяет задачу и останавливает ее выполнение (если запущена)

        Args:
            task_id: id задачи
        """
        updated_id = await self.repository.update_status_by_id(task_id, TaskStatus.CANCELLED)

        if not updated_id:
            raise EntityNotFoundError(TaskORM, task_id)

        # todo cancel task execution if running

        await self.session.commit()

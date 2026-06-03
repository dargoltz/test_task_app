from src.domain.value_objects import TaskStatus, TaskPriority
from src.schemas.request.pagination import PaginationParameters


class TaskFilterParameters(PaginationParameters):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

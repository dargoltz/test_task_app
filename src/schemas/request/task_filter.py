from pydantic import BaseModel

from src.domain.value_objects import TaskPriority, TaskStatus


class TaskFilterQueryParameters(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

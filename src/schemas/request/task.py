from pydantic import BaseModel, Field

from src.domain.value_objects import TaskPriority


class TaskRequest(BaseModel):
    name: str = Field(title="Имя", min_length=5)
    description: str = Field(title="Описание", min_length=5)
    priority: TaskPriority = Field(title="Приоритет")

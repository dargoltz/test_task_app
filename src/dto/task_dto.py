import datetime
import uuid

from pydantic import BaseModel, Field, ConfigDict

from src.models import TaskPriority, TaskStatus


class TaskRequest(BaseModel):
    name: str = Field(title="Имя", min_length=5)
    description: str = Field(title="Описание", min_length=5)
    priority: TaskPriority = Field(title="Приоритет")


class TaskResponse(BaseModel):
    id: uuid.UUID
    name: str = Field(title="Имя")
    description: str = Field(title="Описание")
    priority: TaskPriority = Field(title="Приоритет")
    status: TaskStatus = Field(title="Статус")
    created_at: datetime.datetime = Field(title="Создана")
    started_at: datetime.datetime | None = Field(title="Начата")
    finished_at: datetime.datetime | None = Field(title="Завершена")
    result: str | None = Field(title="Результат выполнения")
    error: str | None = Field(title="Ошибка выполнения")

    model_config = ConfigDict(from_attributes=True)

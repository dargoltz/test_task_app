from datetime import datetime
import uuid

from pydantic import BaseModel, Field, ConfigDict

from src.domain.value_objects import TaskPriority, TaskStatus


class TaskResponse(BaseModel):
    id: uuid.UUID
    name: str = Field(title="Имя")
    description: str = Field(title="Описание")
    priority: TaskPriority = Field(title="Приоритет")
    status: TaskStatus = Field(title="Статус")
    created_at: datetime = Field(title="Создана")
    started_at: datetime | None = Field(title="Начата")
    finished_at: datetime | None = Field(title="Завершена")
    result: str | None = Field(title="Результат выполнения")
    error: str | None = Field(title="Ошибка выполнения")

    model_config = ConfigDict(from_attributes=True)

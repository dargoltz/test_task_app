from pydantic import BaseModel, Field, computed_field

from src.models import TaskPriority, TaskStatus


class PaginationParameters(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=100, ge=1)

    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class TaskFilterParameters(PaginationParameters):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

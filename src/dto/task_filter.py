from dataclasses import dataclass

from src.domain.value_objects import TaskStatus, TaskPriority


@dataclass(frozen=True, slots=True)
class TaskFilterParameters:
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

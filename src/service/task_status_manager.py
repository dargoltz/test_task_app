from datetime import datetime

from src.domain.exceptions import TaskStatusError
from src.domain.models import Task
from src.domain.value_objects import TaskStatus


class TaskStatusManager:
    def __new__(cls):
        raise TypeError("TaskStatusManager cannot be instantiated")

    @staticmethod
    def set_pending(task: Task) -> None:
        if task.status not in (TaskStatus.NEW, TaskStatus.FAILED):
            raise TaskStatusError(f"Can't set task {task.id} as pending: must be NEW or FAILED")

        task.status = TaskStatus.PENDING

    @staticmethod
    def start(task: Task) -> None:
        if task.status != TaskStatus.PENDING:
            raise TaskStatusError(f"Can't start {task.id}: must be PENDING")

        task.started_at = datetime.now()
        task.status = TaskStatus.IN_PROGRESS

    @staticmethod
    def complete(task: Task, result: str) -> None:
        if task.status != TaskStatus.IN_PROGRESS:
            raise TaskStatusError(f"Can't complete {task.id}: must be IN_PROGRESS")

        task.result = result
        task.finished_at = datetime.now()
        task.status = TaskStatus.COMPLETED

    @staticmethod
    def fail(task: Task, error: str) -> None:
        task.error = error
        task.finished_at = datetime.now()
        task.status = TaskStatus.FAILED

    @staticmethod
    def cancel(task: Task) -> None:
        if task.status not in (TaskStatus.NEW, TaskStatus.PENDING):
            raise TaskStatusError(f"Can't cancel {task.id}: must be NEW or PENDING")

        task.status = TaskStatus.CANCELLED

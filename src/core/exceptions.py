import uuid

from src.models import TaskStatus


class EntityNotFoundError(Exception):
    def __init__(self, entity: type, entity_id: uuid.UUID):
        super().__init__(f"{entity.__name__} {entity_id} not found")


class TaskExecutionError(Exception):
    def __init__(self, task_id: uuid.UUID):
        super().__init__(f"Task {task_id} execution failed")


class TaskCancelError(Exception):
    def __init__(self, task_id: uuid.UUID, status: TaskStatus):
        super().__init__(f"Can't cancel task {task_id}: task status is {status.value}")

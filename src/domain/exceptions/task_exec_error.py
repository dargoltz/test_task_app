import uuid


class TaskExecutionError(Exception):
    def __init__(self, task_id: uuid.UUID):
        super().__init__(f"Task {task_id} execution failed")


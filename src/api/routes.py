import uuid

from fastapi import APIRouter

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/")
async def create_task():
    pass


@task_router.get("/")  # todo add pagination
async def get_tasks():
    pass


@task_router.get("/{task_id:uuid}")
async def get_task_by_id(task_id: uuid.UUID):
    pass


@task_router.get("/{task_id:uuid}/status")
async def get_task_status_by_id(task_id: uuid.UUID):
    pass


@task_router.delete("/{task_id:uuid}")
async def delete_task_by_id(task_id: uuid.UUID):
    pass

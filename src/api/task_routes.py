import uuid

from fastapi import APIRouter, status, Depends, Query

from src.dto import TaskRequest, PaginatedResponse, TaskResponse, TaskFilterParameters
from src.models import TaskStatus
from src.service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskRequest,
    service: TaskService = Depends(TaskService),
):
    return await service.create_task(request)


@task_router.get("/", response_model=PaginatedResponse[TaskResponse])
async def get_tasks(
    filter_params: TaskFilterParameters = Depends(),
    service: TaskService = Depends(TaskService),
):
    return await service.get_task_list(filter_params)


@task_router.get("/{task_id:uuid}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: uuid.UUID,
    service: TaskService = Depends(TaskService),
):
    return await service.get_task(task_id)


@task_router.get("/{task_id:uuid}/status", response_model=TaskStatus)
async def get_task_status_by_id(
    task_id: uuid.UUID,
    service: TaskService = Depends(TaskService),
):
    return await service.get_task_status(task_id)


@task_router.delete("/{task_id:uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_task_by_id(
    task_id: uuid.UUID,
    service: TaskService = Depends(TaskService),
):
    return await service.cancel_task(task_id)

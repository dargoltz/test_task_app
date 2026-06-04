import uuid

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.dependencies import get_task_service
from src.schemas.request import (
    PaginationQueryParameters,
    TaskFilterQueryParameters,
    TaskRequest,
)
from src.schemas.response import PageResponse, TaskResponse
from src.service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskRequest,
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(request)


@task_router.get("/", response_model=PageResponse[TaskResponse])
async def get_tasks(
    page_params: PaginationQueryParameters = Depends(),
    filter_params: TaskFilterQueryParameters = Depends(),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_tasks(page_params, filter_params)


@task_router.get("/{task_id:uuid}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: uuid.UUID,
    service: TaskService = Depends(get_task_service),
):
    return await service.get_task(task_id)


@task_router.get("/{task_id:uuid}/status")
async def get_task_status_by_id(
    task_id: uuid.UUID,
    service: TaskService = Depends(get_task_service),
):
    task_status = await service.get_task_status(task_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": task_status})


@task_router.delete("/{task_id:uuid}")
async def cancel_task_by_id(
    task_id: uuid.UUID,
    service: TaskService = Depends(get_task_service),
):
    await service.cancel_task(task_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": f"Task {task_id} cancelled"}
    )

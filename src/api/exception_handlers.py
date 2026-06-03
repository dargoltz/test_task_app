from fastapi import status, Request
from fastapi.responses import JSONResponse

from src.core import TaskExecutionError, EntityNotFoundError, TaskCancelError


async def not_found_handler(
    request: Request,
    exc: EntityNotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


async def cancel_error_handler(
    request: Request,
    exc: TaskCancelError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


async def task_execution_error_handler(
    request: Request,
    exc: TaskExecutionError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

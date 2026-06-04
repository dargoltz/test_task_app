from fastapi import status, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import EntityNotFoundError, TaskStatusError


async def not_found_handler(
    request: Request,
    exc: EntityNotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

async def task_status_error_handler(
    request: Request,
    exc: TaskStatusError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )
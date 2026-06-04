import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import EntityNotFoundError, TaskStatusError

logger = structlog.get_logger()


async def not_found_handler(
    request: Request,
    exc: EntityNotFoundError,
):
    logger.info(exc)

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


async def task_status_error_handler(
    request: Request,
    exc: TaskStatusError,
):
    logger.info(exc)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )

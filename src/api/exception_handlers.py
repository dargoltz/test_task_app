from fastapi import status, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import EntityNotFoundError


async def not_found_handler(
    request: Request,
    exc: EntityNotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

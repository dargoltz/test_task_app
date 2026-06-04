from fastapi import APIRouter, FastAPI

from src.api.exception_handlers import not_found_handler, task_status_error_handler
from src.api.lifespan import lifespan
from src.api.task_routes import task_router
from src.domain.exceptions import EntityNotFoundError, TaskStatusError

app = FastAPI(lifespan=lifespan)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(task_router)

app.include_router(api_v1_router)

app.add_exception_handler(EntityNotFoundError, not_found_handler)
app.add_exception_handler(TaskStatusError, task_status_error_handler)

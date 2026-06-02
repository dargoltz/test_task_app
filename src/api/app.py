from fastapi import FastAPI, APIRouter

from src.api.exception_handlers import not_found_handler, cancel_error_handler, task_execution_error_handler
from src.api.task_routes import task_router
from src.core import EntityNotFoundError, TaskCancelError, TaskExecutionError
from src.api.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(task_router)

app.include_router(api_v1_router)

app.add_exception_handler(EntityNotFoundError, not_found_handler)
app.add_exception_handler(TaskCancelError, cancel_error_handler)
app.add_exception_handler(TaskExecutionError, task_execution_error_handler)

from fastapi import FastAPI, APIRouter

from src.api.routes import task_router

app = FastAPI()

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(task_router)

app.include_router(api_v1_router)

from fastapi import APIRouter
from app.api.endpoints import weather, tasks, results

api_router = APIRouter()

# Include individual route files
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(results.router, prefix="/results", tags=["Results"])

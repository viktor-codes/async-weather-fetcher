from fastapi import APIRouter, HTTPException
import json
import redis
from app.core.config import settings
from app.schemas.weather import TaskStatusResponse

# Initialize Redis client
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

router = APIRouter()


@router.get("/{task_id}", response_model=TaskStatusResponse, tags=["Tasks"])
async def get_task_status(task_id: str):
    """
    Fetches the status of a Celery task using Redis.
    """
    task_data = redis_client.get(task_id)

    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    parsed_data = json.loads(task_data)
    parsed_data["task_id"] = task_id  # Ensure task_id is included in response

    return parsed_data

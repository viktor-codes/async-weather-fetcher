from fastapi import APIRouter, HTTPException
import json
from app.schemas.weather import TaskStatusResponse
from app.utils.redis_client import redis_client

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

from fastapi import APIRouter, HTTPException
from app.schemas.weather import WeatherRequest
from app.services.weather_service import process_weather_data
from app.utils.logger import logger
import uuid

router = APIRouter()


@router.post("/", response_model=dict, tags=["Weather"])
async def request_weather_data(payload: WeatherRequest):
    """
    Accepts a list of cities, assigns a unique task ID,
    and triggers an asynchronous task for weather processing.
    """
    task_id = str(uuid.uuid4())  # Generate unique task ID
    try:
        process_weather_data.delay(payload.cities, task_id)
        return {"task_id": task_id, "status": "running"}
    except Exception as e:
        logger.error(f"Failed to start weather task: {e}")
        raise HTTPException(
            status_code=500,
            detail="Could not start weather data processing."
        )

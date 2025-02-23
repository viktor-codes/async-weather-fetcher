from pydantic import BaseModel, Field
from typing import List, Optional


# Request Model
class WeatherRequest(BaseModel):
    cities: List[str] = Field(..., min_items=1, max_items=50)


# Response Model
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str


# Task Status Model
class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    results: Optional[dict] = None


class WeatherData(BaseModel):
    city: str = Field(
        ..., min_length=1, max_length=100, pattern=r"^[a-zA-Z\s-]+$"
    )
    temperature: float = Field(
        ..., ge=-50, le=50, description="Temperature in Celsius (-50 to 50)"
    )
    description: str = Field(..., min_length=2, max_length=100)

from fastapi import APIRouter, HTTPException
import os
import json

router = APIRouter()

WEATHER_DATA_DIR = "weather_data"


@router.get("/{region}", response_model=dict, tags=["Results"])
async def get_results_by_region(region: str):
    """
    Fetches stored weather data for a specific region.
    """
    region_dir = os.path.join(WEATHER_DATA_DIR, region)

    if not os.path.exists(region_dir):
        raise HTTPException(status_code=404, detail="Region not found")

    results = {}

    for filename in os.listdir(region_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(region_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                task_id = filename.replace("task_", "").replace(".json", "")
                results[task_id] = json.load(file)

    return {"region": region, "tasks": results}

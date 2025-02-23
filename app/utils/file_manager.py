import os
import json
from app.utils.logger import logger

WEATHER_DATA_DIR = "weather_data"


def save_results_to_files(task_id, results):
    """
    Saves the processed weather data into region-based JSON files.
    """
    try:
        if not os.path.exists(WEATHER_DATA_DIR):
            logger.info(f"Creating directory: {WEATHER_DATA_DIR}")
            os.makedirs(WEATHER_DATA_DIR, exist_ok=True)

        for region, cities_data in results.items():
            region_dir = os.path.join(WEATHER_DATA_DIR, region)

            if not os.path.exists(region_dir):
                logger.info(f"Creating directory: {region_dir}")
                os.makedirs(region_dir, exist_ok=True)

            file_path = os.path.join(region_dir, f"task_{task_id}.json")

            # Exclude 'country' field before saving
            sanitized_data = [
                {k: v for k, v in city_data.items() if k != "country"}
                for city_data in cities_data
            ]

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(sanitized_data, file, indent=4, ensure_ascii=False)

        logger.info(f"Weather data saved successfully for task {task_id}")

    except Exception as e:
        logger.error(f"Failed to save weather data: {str(e)}")

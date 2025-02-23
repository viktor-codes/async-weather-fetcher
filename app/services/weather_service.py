import json
import httpx
from app.utils.logger import logger
from app.core.celery_app import celery
from app.utils.redis_client import log_api_failure
from app.services.city_normalizer import normalize_city
from app.utils.file_manager import save_results_to_files
from app.utils.redis_client import redis_client
from app.core.config import settings
from app.utils.region_mapping import get_region_for_country
from app.utils.retry import retry
from app.services.weather_providers import (
    WeatherAPIProvider,
    WeatherBitProvider
)

# Provider mapping
PROVIDER_CLASSES = {
    "weatherapi": WeatherAPIProvider,
    "weatherbit": WeatherBitProvider,
}


def get_provider(provider_name: str):
    """
    Returns an instance of the requested weather provider.
    Falls back to default if an invalid provider is given.
    """
    if provider_name not in PROVIDER_CLASSES:
        logger.warning(
            f"Unsupported provider: {provider_name}, falling back to default."
        )
        provider_name = settings.DEFAULT_WEATHER_PROVIDER

    provider_cls = PROVIDER_CLASSES[provider_name]
    return provider_cls(
        settings.WEATHER_PROVIDERS[provider_name]["url"],
        settings.WEATHER_PROVIDERS[provider_name]["key"],
    )


def get_weather_data(city: str, provider_name: str = None):
    """
    Fetches weather data using the specified provider.
    Falls back to another provider if the first fails.
    If both providers fail, returns None.
    """
    providers = ["weatherapi", "weatherbit"]
    provider_name = provider_name or settings.DEFAULT_WEATHER_PROVIDER

    for provider in providers:
        try:
            selected_provider = get_provider(provider)
            logger.info(
                f"Fetching weather data for {city} using {provider}..."
            )
            data = selected_provider.fetch_weather(city)
            if data:
                return data
        except httpx.HTTPStatusError as e:
            logger.error(
                f"{provider} API request failed: "
                f"{e.response.status_code} {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"Connection error with {provider}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error with {provider}: {str(e)}")
            log_api_failure(city, provider, str(e))

    logger.warning(
        f"Both providers failed. Weather data unavailable for {city}."
    )
    return None


@celery.task(bind=True)
@retry(
    max_retries=3,
    initial_delay=2,
    backoff_factor=2,
    exceptions=(httpx.RequestError,)
)
def process_weather_data(self, cities, task_id):
    """
    Celery background task to fetch and validate weather data for cities.
    If all providers fail, the task will not save incomplete data.
    """
    logger.info(f"Starting weather data processing for Task ID: {task_id}")

    # Normalize city names
    normalized_cities = [normalize_city(city) for city in cities]
    results = {}
    valid_data_found = False

    for city in normalized_cities:
        weather_data = get_weather_data(city)

        if not weather_data:
            logger.warning(f"Skipping {city} due to missing weather data.")
            continue

        # Ensure 'country' key exists
        country = weather_data.get("country")
        if not country:
            logger.warning(f"Skipping {city} due to missing 'country' field.")
            continue

        # Get region mapping
        region = get_region_for_country(country)
        if region not in results:
            results[region] = []
        results[region].append(weather_data)
        valid_data_found = True

    if valid_data_found:
        save_results_to_files(task_id, results)
        redis_client.set(
            task_id, json.dumps({"status": "completed", "results": results})
        )
        logger.info(
            f"Task ID {task_id} processing completed and stored in Redis."
        )
    else:
        logger.warning(
            f"No valid weather data found for Task ID: "
            f"{task_id}. Task will be marked as failed."
        )
        redis_client.set(
            task_id, json.dumps({"status": "failed", "results": {}})
        )

        # Raise an exception to mark the task as failed
        raise Exception(f"Task {task_id} failed: No valid weather data found.")

from app.utils.logger import logger
import redis
import json
import time
from app.core.config import settings

# Shared Redis client for the whole stack (API and Celery).
# decode_responses=True so Redis returns str and json.loads works without extra decoding.
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)

try:
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except redis.ConnectionError as e:
    # Do not close redis_client at import time; surface errors at call sites
    # where they can be handled with proper context.
    logger.warning(f"Redis ping failed (will fail on use): {str(e)}")


def log_api_failure(city, provider, error_message):
    """Logs API failure details in Redis"""
    failure_entry = {
        "timestamp": int(time.time()),  # Unix timestamp
        "city": city,
        "provider": provider,
        "error": error_message,
    }

    try:
        redis_client.rpush("weather_api_failures", json.dumps(failure_entry))
        logger.info(
            f"Logged API failure for {city} ({provider}): {error_message}"
        )
    except redis.ConnectionError as e:
        logger.warning(f"Failed to log API failure to Redis: {str(e)}")

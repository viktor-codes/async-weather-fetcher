from app.utils.logger import logger
import redis
import json
import time

try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {str(e)}")
    redis_client = None


def log_api_failure(city, provider, error_message):
    """Logs API failure details in Redis"""
    if not redis_client:
        logger.warning("Redis is not available. Skipping API failure logging.")
        return

    failure_entry = {
        "timestamp": int(time.time()),  # Unix timestamp
        "city": city,
        "provider": provider,
        "error": error_message,
    }

    redis_client.rpush("weather_api_failures", json.dumps(failure_entry))
    logger.info(f"Logged API failure for {city} ({provider}): {error_message}")

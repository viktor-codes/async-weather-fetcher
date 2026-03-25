from app.utils.logger import logger
import redis
import json
import time
from app.core.config import settings

# Общий Redis-клиент для всей системы (и для API, и для Celery).
# Важно: decode_responses=True, чтобы Redis возвращал строки и json.loads работал без дополнительных преобразований.
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
    # Не выключаем redis_client на этапе импорта:
    # пусть ошибка проявится в точках использования, где её можно обработать контекстно.
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

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application configuration settings.
    Loads environment variables with default fallback values.
    """

    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL", "redis://localhost:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )

    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    # Weather API Keys (Ensure these are set in your .env file)
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")
    WEATHERBIT_API_KEY: str = os.getenv("WEATHERBIT_API_KEY")

    # Supported Weather Providers
    WEATHER_PROVIDERS = {
        "weatherapi": {
            "url": "https://api.weatherapi.com/v1/current.json",
            "key": WEATHER_API_KEY,
        },
        "weatherbit": {
            "url": "https://api.weatherbit.io/v2.0/current",
            "key": WEATHERBIT_API_KEY,
        },
    }

    # Default Weather Provider
    DEFAULT_WEATHER_PROVIDER: str = os.getenv(
        "DEFAULT_WEATHER_PROVIDER", "weatherbit"
    )


# Initialize settings
settings = Settings()

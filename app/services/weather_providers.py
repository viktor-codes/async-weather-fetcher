import httpx
from app.utils.logger import logger
from app.utils.redis_client import log_api_failure


class WeatherProvider:
    """Base class for weather providers."""

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def fetch_weather(self, city):
        """Must be implemented by subclasses."""
        raise NotImplementedError(
            "Subclasses must implement fetch_weather method."
        )

    def _make_request(self, params):
        """Handles the HTTP request and error logging synchronously."""
        try:
            response = httpx.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            error_message = str(e)
            logger.error(
                f"Failed to fetch weather data from "
                f"{self.api_url}: {error_message}"
            )

            # Log the failure in Redis
            log_api_failure(
                params.get("q") or params.get("city"),
                self.api_url, error_message
            )

            return None


class WeatherAPIProvider(WeatherProvider):
    """WeatherAPI provider implementation."""

    def fetch_weather(self, city):
        params = {"q": city, "key": self.api_key}
        data = self._make_request(params)
        if data:
            return {
                "city": data["location"]["name"],
                "temperature": data["current"]["temp_c"],
                "description": data["current"]["condition"]["text"],
                "country": data["location"]["country"],
            }
        return None


class WeatherBitProvider(WeatherProvider):
    """WeatherBit provider implementation."""

    def fetch_weather(self, city):
        params = {"city": city, "key": self.api_key}
        data = self._make_request(params)
        if data and "data" in data and data["data"]:
            return {
                "city": data["data"][0]["city_name"],
                "temperature": data["data"][0]["temp"],
                "description": data["data"][0]["weather"]["description"],
                "country": data["data"][0]["country_code"],
            }
        return None

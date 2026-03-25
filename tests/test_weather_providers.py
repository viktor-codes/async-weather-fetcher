from app.services.weather_providers import WeatherAPIProvider, WeatherBitProvider


class MockResponse:
    def __init__(self, payload: dict, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code
        self.text = str(payload)

    def raise_for_status(self) -> None:
        # In these tests the HTTP response is always successful, so always pass.
        return None

    def json(self) -> dict:
        return self._payload


def test_weatherapi_provider_maps_fields(mocker):
    payload = {
        "location": {"name": "Kyiv", "country": "Ukraine"},
        "current": {"temp_c": -2.0, "condition": {"text": "snow"}},
    }
    mock_get = mocker.patch(
        "app.services.weather_providers.httpx.get",
        return_value=MockResponse(payload),
    )

    provider = WeatherAPIProvider(
        api_url="https://api.weatherapi.com/v1/current.json",
        api_key="test_key",
    )

    result = provider.fetch_weather("Kyiv")

    assert result == {
        "city": "Kyiv",
        "temperature": -2.0,
        "description": "snow",
        "country": "Ukraine",
    }

    assert mock_get.call_args.kwargs["params"]["q"] == "Kyiv"
    assert mock_get.call_args.kwargs["params"]["key"] == "test_key"


def test_weatherbit_provider_maps_fields(mocker):
    payload = {
        "data": [
            {
                "city_name": "London",
                "temp": 10,
                "weather": {"description": "rain"},
                "country_code": "GB",
            }
        ]
    }
    mock_get = mocker.patch(
        "app.services.weather_providers.httpx.get",
        return_value=MockResponse(payload),
    )

    provider = WeatherBitProvider(
        api_url="https://api.weatherbit.io/v2.0/current",
        api_key="test_key",
    )

    result = provider.fetch_weather("London")

    assert result == {
        "city": "London",
        "temperature": 10,
        "description": "rain",
        "country": "GB",
    }

    assert mock_get.call_args.kwargs["params"]["city"] == "London"
    assert mock_get.call_args.kwargs["params"]["key"] == "test_key"


from fastapi.testclient import TestClient

from app.main import app
from app.services.weather_service import process_weather_data


class FakeRedis:
    def __init__(self):
        self._store: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self._store[key] = value

    def get(self, key: str):
        return self._store.get(key)


def sanitize_results_for_test(task_id: str, results_by_region: dict) -> dict:
    # Мы хотим тестировать контракт API, поэтому без записи на диск.
    sanitized = {}
    for region, cities_data in results_by_region.items():
        sanitized[region] = [
            {k: v for k, v in city_data.items() if k != "country"}
            for city_data in cities_data
        ]
    return sanitized


def test_post_weather_then_get_task_status_completed(mocker):
    fake_redis = FakeRedis()

    mocker.patch("app.services.weather_service.redis_client", fake_redis)
    mocker.patch("app.api.endpoints.tasks.redis_client", fake_redis)
    mocker.patch(
        "app.services.weather_service.save_results_to_files",
        sanitize_results_for_test,
    )

    mocker.patch(
        "app.services.weather_service.get_weather_data",
        return_value={
            "city": "Kyiv",
            "temperature": -2.0,
            "description": "snow",
            "country": "Ukraine",
        },
    )

    def fake_delay(cities, task_id):
        # В процессе теста выполняем "таск" синхронно.
        return process_weather_data.run(cities, task_id)

    mocker.patch(
        "app.api.endpoints.weather.process_weather_data.delay",
        new=fake_delay,
    )

    client = TestClient(app)

    post_resp = client.post("/weather/", json={"cities": ["Kyiv"]})
    assert post_resp.status_code == 200
    payload = post_resp.json()

    task_id = payload["task_id"]
    assert payload["status"] == "running"

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 200
    task_status = get_resp.json()

    assert task_status["task_id"] == task_id
    assert task_status["status"] == "completed"
    assert "Europe" in task_status["results"]
    assert task_status["results"]["Europe"][0]["city"] == "Kyiv"
    assert "country" not in task_status["results"]["Europe"][0]


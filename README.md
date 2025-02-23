# Asynchronous Weather Data Processing System

This project is a FastAPI-based asynchronous weather data processing system using Celery, Redis, and external APIs. It processes weather data for user-specified cities, normalizes city names, handles API failures, and stores results regionally.

## Features

- Accepts a list of cities via an HTTP POST request
- Fetches weather data asynchronously using Celery workers
- Retries on API failures and uses multiple providers (weatherapi, weatherbit)
- Supports city names in multiple languages with typo correction
- Organized data storage by geographic region (weather_data/<region>/task_<task_id>.json)
- Task tracking with Redis (GET /tasks/{task_id})
- Robust error handling and logging for reliability
- Easily configurable with environment variables (.env support)

## Getting Started

### Prerequisites
Ensure you have the following installed:

- Python 3.8+
- Redis (for task tracking)
- Docker (optional, for running Redis)
- pip, virtualenv

### Clone the Repository
```sh
git clone https://github.com/viktor-codes/async-weather-fetcher.git
cd async-weather-fetcher
```

### Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```
### Obtain API Keys
To fetch weather data, you need to obtain API keys from the following providers:

1. **WeatherAPI**
   - Register at [https://www.weatherapi.com/](https://www.weatherapi.com/)
   - Sign up and navigate to the API section
   - Generate a free API key and copy it

2. **Weatherbit**
   - Register at [https://www.weatherbit.io/](https://www.weatherbit.io/)
   - Create an account and go to the API section
   - Obtain an API key for free-tier access

Once you have the keys, add them to the `.env` file as shown below.

### Set Up Environment Variables
Create a `.env` file and configure your API keys and Redis settings:
```ini
# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Weather API Keys
WEATHER_API_KEY=your_weatherapi_key
WEATHERBIT_API_KEY=your_weatherbit_key

# Default Weather Provider
DEFAULT_WEATHER_PROVIDER=weatherbit
```

## Running the Application

### Start Redis
If Redis is not running, start it using Docker:
```sh
docker run -d -p 6379:6379 redis
```
Or, if installed locally:
```sh
redis-server
```

### Start Celery Workers
```sh
celery -A app.core.celery_app worker --loglevel=info
```

### Start the FastAPI Server
```sh
uvicorn app.main:app --reload
```
The API will now be available at `http://127.0.0.1:8000`.

## API Usage

### Submit a Weather Data Processing Request
#### `POST /weather`
Request:
```json
{
  "cities": ["New York", "Киев", "Londn"]
}
```
Response:
```json
{
  "task_id": "a1b2c3d4",
  "status": "running"
}
```

### Check Task Status
#### `GET /tasks/{task_id}`
Response:
```json
{
  "status": "completed",
  "results": {
    "Europe": [
      { "city": "Kyiv", "temperature": -2.0, "description": "snow" },
      { "city": "London", "temperature": 10.0, "description": "rain" }
    ],
    "America": [
      { "city": "New York", "temperature": 15.0, "description": "clear sky" }
    ]
  }
}
```

### Fetch Processed Weather Data by Region
#### `GET /results/{region}`
Example:
```sh
GET /results/Europe
```
Response:
```json
[
  { "city": "Kyiv", "temperature": -2.0, "description": "snow" },
  { "city": "London", "temperature": 10.0, "description": "rain" }
]
```

## Project Structure
```
async-weather-fetcher/
│── app/
│   ├── api/              # FastAPI endpoints
│   ├── core/             # Config & Celery setup
│   ├── services/         # Weather processing logic
│   ├── utils/            # Utility functions (logging, file handling)
│   ├── schemas/          # Data validation (Pydantic)
│   ├── main.py           # Entry point for FastAPI
│── weather_data/         # Stores processed weather data
│── .env                  # Environment variables (ignored in .gitignore)
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```
from fastapi import FastAPI
from app.api.routers import api_router

app = FastAPI(
    title="Weather Service API",
    description="An asynchronous weather data processing API using Celery",
    version="1.0.0",
)

# Include API routers
app.include_router(api_router)


# Root endpoint to check service health
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}

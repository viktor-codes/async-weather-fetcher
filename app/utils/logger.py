import logging
import os
import colorlog

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

log_format = "%(log_color)s%(asctime)s - " \
             "%(name)s - %(levelname)s - " \
             "%(message)s"

date_format = "%Y-%m-%d %H:%M:%S"

colorlog.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.FileHandler(LOG_FILE),
        colorlog.StreamHandler(),
    ],
)

logger = logging.getLogger("WeatherApp")

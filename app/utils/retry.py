import time
import functools
from app.utils.logger import logger


def retry(
        max_retries=3,
        initial_delay=1,
        backoff_factor=2,
        exceptions=(Exception,)
):
    """
    A retry decorator to handle transient failures.

    Parameters:
    - max_retries: Number of times to retry the function before failing.
    - initial_delay: Time (in seconds) to wait before the first retry.
    - backoff_factor: Multiplier for exponential backoff
    (e.g., 2 means 1s → 2s → 4s).
    - exceptions: A tuple of exception types to catch and retry.

    Usage:
    ```
    @retry(max_retries=3, initial_delay=2, backoff_factor=2)
    def unstable_function():
        ...
    ```
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed: {e}"
                    )
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= backoff_factor  # Exponential backoff
                    else:
                        logger.error(
                            f"Function {func.__name__} failed "
                            f"after {max_retries} attempts."
                        )
                        raise

        return wrapper

    return decorator

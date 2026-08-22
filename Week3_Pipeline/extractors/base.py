"""
extractors/base.py

Shared retry/error-handling logic used by every source extractor.
Each source module (world_bank.py, who.py) calls fetch_with_retry()
instead of requests.get() directly, so pagination/retry behavior is
written once and reused everywhere — this is the "reusable" part of
today's task.
"""

import time
import logging
import requests

logger = logging.getLogger(__name__)


def fetch_with_retry(url, params=None, max_retries=3, backoff_seconds=2):
    """
    Calls requests.get() with automatic retries.

    Why this exists: a single failed request (timeout, 500 error,
    flaky connection) shouldn't crash the whole pipeline. This retries
    up to `max_retries` times with a short pause between attempts,
    and only gives up (raising the error) after all retries fail.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()  # raises on 4xx/5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"Attempt {attempt}/{max_retries} failed for {url}: {e}"
            )
            if attempt == max_retries:
                logger.error(f"Giving up on {url} after {max_retries} attempts")
                raise
            time.sleep(backoff_seconds * attempt)  # wait longer each retry
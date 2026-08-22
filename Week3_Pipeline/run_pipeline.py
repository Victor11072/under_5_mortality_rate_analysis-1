"""
run_pipeline.py

THE single entrypoint for the whole pipeline: extract -> transform ->
load, for every indicator in config.py, across both sources. This is
the answer to Day 1's question 1: one command, no manual rework.

Run with:  python run_pipeline.py
"""

import logging
import os
from datetime import datetime

from extractors.world_bank import fetch_world_bank
from extractors.who import fetch_who
from transform.clean import transform
from validate.checks import validate, ValidationError
from load.db import load_rows
import config

# ---- Logging setup ----
# Writes to BOTH a file (for unattended runs -- this is what makes
# failures traceable when nobody's watching) and the console (for
# when you're running it manually and want to see progress live).
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/pipeline_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(),  # also prints to terminal
    ],
)
logger = logging.getLogger(__name__)


def run():
    logger.info("=" * 60)
    logger.info("Pipeline run started")

    total_loaded = 0
    failures = 0

    for indicator_code, source in config.INDICATORS:
        try:
            logger.info(f"Processing {indicator_code} from {source}...")

            if source == "world_bank":
                raw_rows = fetch_world_bank(
                    indicator_code,
                    countries=config.COUNTRIES_WORLD_BANK,
                    start_year=config.START_YEAR,
                    end_year=config.END_YEAR,
                )
            elif source == "who":
                raw_rows = fetch_who(indicator_code, countries=config.COUNTRIES_WHO)
            else:
                logger.error(f"Unknown source '{source}' for {indicator_code}, skipping")
                failures += 1
                continue

            clean_rows = transform(raw_rows)

            try:
                validated_rows = validate(clean_rows)
            except ValidationError as e:
                # A validation failure means this indicator's data
                # looked wrong enough to refuse -- log it clearly and
                # skip loading, but don't crash the whole pipeline
                # over one bad indicator.
                logger.error(f"Validation failed for {indicator_code}: {e}")
                failures += 1
                continue

            loaded_count = load_rows(validated_rows, source=source)
            total_loaded += loaded_count

            logger.info(f"{indicator_code}: {loaded_count} rows loaded successfully")

        except Exception as e:
            # One indicator failing shouldn't kill the whole pipeline --
            # log it and move on to the next one. This is the
            # "traceable failures" part of today's task.
            logger.error(f"FAILED processing {indicator_code} from {source}: {e}")
            failures += 1

    logger.info(
        f"Pipeline run complete: {total_loaded} rows loaded, {failures} failures"
    )
    logger.info("=" * 60)

    return total_loaded, failures


if __name__ == "__main__":
    run()
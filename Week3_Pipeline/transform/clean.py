"""
transform/clean.py

Turns raw rows from extractors/world_bank.py or extractors/who.py
(already in the standard shape: country_code, indicator_code, year,
value) into clean, load-ready rows.

Takes a list of dicts in, returns a list of dicts out — no pandas
DataFrame required, though the same logic works fine on a DataFrame
too if you prefer that for larger datasets.
"""

import logging

logger = logging.getLogger(__name__)

# A small known-good list for this project's 3-country test subset.
# In a full pipeline this would be a longer reference list (or its
# own database table) covering every real country you track — the
# point is filtering OUT non-country aggregates like "Arab World"
# or "Sub-Saharan Africa" that some APIs mix into country data.
VALID_COUNTRY_CODES = {"NGA", "KEN", "GHA"}


def standardize_types(rows):
    """
    Fixes cross-source inconsistencies discovered in Day 2's real
    output: World Bank returns year as a string ('2022'), WHO returns
    it as an int (2011). Every row leaving this function has the same
    types no matter which source it came from.
    """
    cleaned = []
    for row in rows:
        try:
            row["year"] = int(row["year"])
            if row["value"] is not None:
                row["value"] = float(row["value"])
            cleaned.append(row)
        except (ValueError, TypeError) as e:
            logger.warning(f"Skipping row with unconvertible types: {row} ({e})")
    return cleaned


def filter_valid_countries(rows):
    """
    Drops rows whose country_code isn't in our known-good list —
    catches region aggregates and unrecognized codes before they
    reach storage.
    """
    kept, dropped = [], 0
    for row in rows:
        if row.get("country_code") in VALID_COUNTRY_CODES:
            kept.append(row)
        else:
            dropped += 1
    if dropped:
        logger.info(f"Filtered out {dropped} rows with non-standard country codes")
    return kept


def drop_missing_values(rows):
    """
    Drops rows where value is None or missing — an API returning
    'no data' for a country/year shouldn't silently become 0.
    """
    kept, dropped = [], 0
    for row in rows:
        if row.get("value") is not None:
            kept.append(row)
        else:
            dropped += 1
    if dropped:
        logger.info(f"Dropped {dropped} rows with missing values")
    return kept


def deduplicate(rows):
    """
    Removes exact duplicate (country_code, indicator_code, year)
    combinations, keeping the first occurrence. This mirrors the
    composite primary key on indicator_values — a duplicate here
    would otherwise fail (or silently overwrite) at load time.
    """
    seen = set()
    deduped = []
    duplicates = 0
    for row in rows:
        key = (row["country_code"], row["indicator_code"], row["year"])
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        deduped.append(row)
    if duplicates:
        logger.info(f"Removed {duplicates} duplicate rows")
    return deduped


def transform(rows):
    """
    Runs the full transform pipeline in order. This is the one
    function extract's output gets handed to — everything above is
    an internal step, this is the public interface.
    """
    rows = standardize_types(rows)
    rows = filter_valid_countries(rows)
    rows = drop_missing_values(rows)
    rows = deduplicate(rows)
    logger.info(f"Transform complete: {len(rows)} clean rows")
    return rows


if __name__ == "__main__":
    # Manual test with deliberately messy fake data: mixed year types,
    # a missing value, a non-standard country code, and a duplicate —
    # exactly the four problems this file exists to fix.
    logging.basicConfig(level=logging.INFO)

    messy_rows = [
        {"country_code": "NGA", "indicator_code": "X", "year": "2022", "value": 54.7},
        {"country_code": "KEN", "indicator_code": "X", "year": 2021, "value": 61.4},
        {"country_code": "ARB", "indicator_code": "X", "year": 2022, "value": 70.0},  # region aggregate
        {"country_code": "GHA", "indicator_code": "X", "year": 2022, "value": None},  # missing
        {"country_code": "NGA", "indicator_code": "X", "year": "2022", "value": 54.7},  # duplicate
    ]

    result = transform(messy_rows)
    print(f"\nInput: {len(messy_rows)} rows -> Output: {len(result)} clean rows")
    for r in result:
        print(r)
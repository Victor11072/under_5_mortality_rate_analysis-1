"""
extractors/world_bank.py

Fetches indicator data from the World Bank API, handling pagination
automatically. Output columns are renamed to the pipeline's standard
shape so transform.py never has to know this data came from World Bank.
"""

import logging
from extractors.base import fetch_with_retry

logger = logging.getLogger(__name__)

BASE_URL = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"

# World Bank's raw field names -> our standard column names.
# transform.py only ever sees the right-hand side.
COLUMN_MAP = {
    "countryiso3code": "country_code",
    "date": "year",
    "value": "value",
}


def fetch_world_bank(indicator_code, countries="all", start_year=2015, end_year=2023):
    """
    Fetches one indicator for the given countries/year range.

    countries: "all", or semicolon-joined ISO3 codes e.g. "NGA;KEN;GHA"
               (World Bank's API syntax, not ours — this is the one
               place that quirk needs to be known)

    Returns a list of dicts already renamed to standard column names:
        [{"country_code": "NGA", "year": "2022", "value": 54.7, "indicator_code": "..."}, ...]
    """
    url = BASE_URL.format(countries=countries, indicator=indicator_code)
    all_rows = []
    page = 1

    while True:
        params = {
            "date": f"{start_year}:{end_year}",
            "format": "json",
            "per_page": 1000,
            "page": page,
        }
        data = fetch_with_retry(url, params=params)

        # World Bank always returns [metadata, records] — metadata tells
        # us how many total pages exist, records is the actual data.
        if not data or len(data) < 2 or data[1] is None:
            logger.warning(f"No data returned for {indicator_code} on page {page}")
            break

        metadata, records = data[0], data[1]

        for record in records:
            row = {COLUMN_MAP[k]: record[k] for k in COLUMN_MAP if k in record}
            row["indicator_code"] = indicator_code
            all_rows.append(row)

        total_pages = metadata.get("pages", 1)
        logger.info(f"{indicator_code}: fetched page {page}/{total_pages}")

        if page >= total_pages:
            break
        page += 1

    return all_rows


if __name__ == "__main__":
    # Quick manual test on a small subset — 3 countries, one indicator.
    # This is today's "test on a subset of countries" requirement.
    logging.basicConfig(level=logging.INFO)
    rows = fetch_world_bank(
        indicator_code="SP.DYN.LE00.IN",  # life expectancy at birth
        countries="NGA;KEN;GHA",
        start_year=2020,
        end_year=2022,
    )
    print(f"Fetched {len(rows)} rows")
    for r in rows[:5]:
        print(r)
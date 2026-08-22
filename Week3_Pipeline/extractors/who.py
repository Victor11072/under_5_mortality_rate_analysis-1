"""
extractors/who.py

Fetches indicator data from the WHO Global Health Observatory (GHO)
OData API. WHO paginates differently from World Bank — instead of a
page number you request, each response includes a full URL
("@odata.nextLink") pointing to the next page. You follow that link
until it stops appearing.

Output columns are renamed to the same standard shape as world_bank.py,
so transform.py treats both sources identically.
"""

import logging
from extractors.base import fetch_with_retry

logger = logging.getLogger(__name__)

BASE_URL = "https://ghoapi.azureedge.net/api/{indicator}"

# WHO's raw field names -> our standard column names.
COLUMN_MAP = {
    "SpatialDim": "country_code",
    "TimeDim": "year",
    "NumericValue": "value",
}


def fetch_who(indicator_code, countries=None):
    """
    Fetches one WHO indicator, optionally filtered to specific
    countries (list of ISO3 codes, e.g. ["NGA", "KEN", "GHA"]).

    Returns a list of dicts in the same standard shape as
    fetch_world_bank(): country_code, year, value, indicator_code.
    """
    url = BASE_URL.format(indicator=indicator_code)
    params = {}
    if countries:
        # WHO's OData filter syntax — another source-specific quirk
        # that stays contained in this file.
        country_filter = " or ".join(f"SpatialDim eq '{c}'" for c in countries)
        params["$filter"] = country_filter

    all_rows = []
    next_url = url

    while next_url:
        data = fetch_with_retry(next_url, params=params if next_url == url else None)

        records = data.get("value", [])
        for record in records:
            row = {COLUMN_MAP[k]: record[k] for k in COLUMN_MAP if k in record}
            row["indicator_code"] = indicator_code
            all_rows.append(row)

        next_url = data.get("@odata.nextLink")  # None once there's no more data
        if next_url:
            logger.info(f"{indicator_code}: following next page")

    return all_rows


if __name__ == "__main__":
    # Quick manual test on a small subset of countries.
    logging.basicConfig(level=logging.INFO)
    rows = fetch_who(
        indicator_code="WHOSIS_000001",  # life expectancy at birth
        countries=["NGA", "KEN", "GHA"],
    )
    print(f"Fetched {len(rows)} rows")
    for r in rows[:5]:
        print(r)
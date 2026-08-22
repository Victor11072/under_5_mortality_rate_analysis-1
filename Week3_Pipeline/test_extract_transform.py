"""
test_extract_transform.py

Chains Tuesday's real extractor into Wednesday's transform function,
so you can see extract -> transform working together on real API
data, not just isolated test rows. This is a temporary test script —
run_pipeline.py (later this week) will be the real entrypoint.
"""

import logging
from extractors.world_bank import fetch_world_bank
from transform.clean import transform

logging.basicConfig(level=logging.INFO)

# Fetch real data from the World Bank API (same call as Tuesday)
raw_rows = fetch_world_bank(
    indicator_code="SP.DYN.LE00.IN",
    countries="NGA;KEN;GHA",
    start_year=2018,
    end_year=2022,
)
print(f"\nExtract stage: {len(raw_rows)} raw rows fetched")

# Immediately hand that real data to transform
clean_rows = transform(raw_rows)
print(f"\nTransform stage: {len(clean_rows)} clean rows remain")
for r in clean_rows[:5]:
    print(r)
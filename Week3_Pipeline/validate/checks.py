"""
validate/checks.py

Batch-level sanity checks that run on a full set of transformed rows,
answering "does this result look right overall?" -- different from
transform.py's row-by-row cleanup. Raises ValidationError if something
looks wrong enough that loading it would be a mistake.
"""

import logging

logger = logging.getLogger(__name__)

# Believable range for life expectancy at birth, in years. Values
# outside this almost certainly indicate bad data (a unit mismatch,
# a percentage instead of a year count, an API glitch) rather than
# a real value -- this is the "out-of-range" check from Day 1's
# original research questions.
VALID_VALUE_RANGE = (20.0, 100.0)

EXPECTED_COUNTRIES = {"NGA", "KEN", "GHA"}


class ValidationError(Exception):
    """Raised when a batch of rows fails a validation check."""
    pass


def check_not_empty(rows):
    if not rows:
        raise ValidationError("Validation failed: 0 rows to load -- refusing to proceed.")


def check_missing_countries(rows):
    """
    Confirms every expected country actually appears in this batch.
    This is the 'missing countries' check from Day 1's research
    questions -- catches a source silently returning incomplete data.
    """
    present = {row["country_code"] for row in rows}
    missing = EXPECTED_COUNTRIES - present
    if missing:
        logger.warning(f"Expected countries missing from this batch: {missing}")
        # A warning, not a hard failure -- a single indicator genuinely
        # not having data for one country is plausible and shouldn't
        # block loading the countries that DID come back.


def check_value_ranges(rows):
    """
    Flags (and drops) any value outside a believable range. This is
    the 'out-of-range values' check from Day 1's research questions.
    """
    low, high = VALID_VALUE_RANGE
    valid_rows = []
    flagged = 0
    for row in rows:
        value = row.get("value")
        if value is not None and (value < low or value > high):
            logger.warning(
                f"Out-of-range value flagged and dropped: {row} "
                f"(expected {low}-{high})"
            )
            flagged += 1
            continue
        valid_rows.append(row)
    if flagged:
        logger.info(f"Flagged {flagged} out-of-range values")
    return valid_rows


def check_required_fields(rows):
    """
    Asserts every row has all four required fields non-null. This is
    a safety net -- transform.py should already guarantee this, but
    validation re-checks it independently rather than trusting a
    previous step blindly.
    """
    required = ("country_code", "indicator_code", "year", "value")
    for row in rows:
        for field in required:
            if row.get(field) is None:
                raise ValidationError(
                    f"Validation failed: row missing required field '{field}': {row}"
                )


def validate(rows):
    """
    Runs all validation checks in order. Returns the (possibly
    smaller, after range-flagging) list of rows that are safe to load.
    Raises ValidationError if the batch fails a hard check.
    """
    check_not_empty(rows)
    rows = check_value_ranges(rows)
    check_required_fields(rows)
    check_missing_countries(rows)
    logger.info(f"Validation passed: {len(rows)} rows cleared for loading")
    return rows


if __name__ == "__main__":
    # Manual test with deliberately bad data: one out-of-range value,
    # one row missing a required field, and a country genuinely absent.
    logging.basicConfig(level=logging.INFO)

    test_rows = [
        {"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": 54.7},
        {"country_code": "KEN", "indicator_code": "X", "year": 2022, "value": 999.0},  # out of range
        {"country_code": "GHA", "indicator_code": "X", "year": 2022, "value": None},   # missing field
    ]

    print("Test 1: batch with an out-of-range value and a missing field")
    try:
        result = validate(test_rows)
        print(f"Unexpectedly passed with {len(result)} rows")
    except ValidationError as e:
        print(f"Correctly caught: {e}")

    print("\nTest 2: empty batch")
    try:
        validate([])
    except ValidationError as e:
        print(f"Correctly caught: {e}")

    print("\nTest 3: valid batch (should pass)")
    good_rows = [
        {"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": 54.7},
        {"country_code": "KEN", "indicator_code": "X", "year": 2022, "value": 61.4},
        {"country_code": "GHA", "indicator_code": "X", "year": 2022, "value": 64.1},
    ]
    result = validate(good_rows)
    print(f"PASS: {len(result)} rows cleared correctly")
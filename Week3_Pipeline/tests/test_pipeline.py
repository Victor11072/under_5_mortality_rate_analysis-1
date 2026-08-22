"""
tests/test_pipeline.py

Automated tests for transform.clean and validate.checks -- run with:
    python -m unittest tests.test_pipeline

These replace manually running a script and reading printed output:
every check below runs automatically and reports PASS/FAIL on its own.
"""

import unittest
from transform.clean import transform
from validate.checks import validate, ValidationError


class TestTransform(unittest.TestCase):

    def test_standardizes_year_type(self):
        """World Bank's string year and WHO's int year both become int."""
        rows = [
            {"country_code": "NGA", "indicator_code": "X", "year": "2022", "value": 50.0},
            {"country_code": "KEN", "indicator_code": "X", "year": 2021, "value": 60.0},
        ]
        result = transform(rows)
        self.assertTrue(all(isinstance(r["year"], int) for r in result))

    def test_drops_missing_values(self):
        rows = [
            {"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": 50.0},
            {"country_code": "KEN", "indicator_code": "X", "year": 2022, "value": None},
        ]
        result = transform(rows)
        self.assertEqual(len(result), 1)

    def test_removes_duplicates(self):
        row = {"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": 50.0}
        result = transform([row, dict(row)])  # exact duplicate
        self.assertEqual(len(result), 1)

    def test_filters_invalid_country_codes(self):
        rows = [
            {"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": 50.0},
            {"country_code": "ARB", "indicator_code": "X", "year": 2022, "value": 70.0},  # region aggregate
        ]
        result = transform(rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["country_code"], "NGA")


class TestValidate(unittest.TestCase):

    def test_rejects_empty_batch(self):
        with self.assertRaises(ValidationError):
            validate([])

    def test_rejects_missing_required_field(self):
        rows = [{"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": None}]
        with self.assertRaises(ValidationError):
            validate(rows)

    def test_flags_out_of_range_value(self):
        rows = [
            {"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": 55.0},
            {"country_code": "KEN", "indicator_code": "X", "year": 2022, "value": 999.0},
        ]
        result = validate(rows)
        # the out-of-range row should be dropped, not crash the batch
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["country_code"], "NGA")

    def test_accepts_clean_batch(self):
        rows = [
            {"country_code": "NGA", "indicator_code": "X", "year": 2022, "value": 54.7},
            {"country_code": "KEN", "indicator_code": "X", "year": 2022, "value": 61.4},
            {"country_code": "GHA", "indicator_code": "X", "year": 2022, "value": 64.1},
        ]
        result = validate(rows)
        self.assertEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()
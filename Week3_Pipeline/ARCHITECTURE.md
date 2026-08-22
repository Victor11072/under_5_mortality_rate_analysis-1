# Architecture — Day 1

## Flow
World Bank API ─┐
                 ├─> extract() ─> transform() ─> validate() ─> load()
WHO API ─────────┘                                                │
                                                                   v
                                                         Postgres (indicator_values)

## Why this shape
- **Two extractors, one output shape.** Each source (World Bank, WHO)
  has its own module that knows that API's pagination/field-naming
  quirks, but both must return the same standard shape: country_code,
  indicator_code, year, value. Transform/validate/load never know or
  care which source a row came from. Adding a third source later
  means writing one new extractor — nothing downstream changes.

- **ETL, not ELT.** Cleaning/standardizing happens in Python before
  the data reaches Postgres, because the raw API responses aren't in
  a queryable tabular shape yet (nested JSON, inconsistent country
  naming) — there's nothing meaningful to load first and transform
  later. ELT makes more sense when the destination is a warehouse
  built to transform at scale (e.g. Snowflake/BigQuery); this
  pipeline's destination is a small operational Postgres DB.

- **Composite primary key = idempotency.** (country_code,
  indicator_code, year) as the primary key on indicator_values means
  Thursday's `INSERT ... ON CONFLICT DO UPDATE` step can re-run the
  whole pipeline any number of times without creating duplicate rows.

## Not done yet (later days)
- Extract functions (Tue), transform functions (Wed)
- Idempotent load logic in Python (Thu)
- Scheduling + logging (Fri)
- Validation checks + tests (Sat)

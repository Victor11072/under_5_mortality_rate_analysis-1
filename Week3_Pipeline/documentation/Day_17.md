# Day 17/30 — Week 3: Turning Week 1-2 cleaning logic into reusable transform functions

Day 15 was architecture, Day 16 was extraction. Day 17 closed the loop
between them: turning the manual data-cleaning I did in Weeks 1-2 into
proper, reusable transform functions — and proving, for the first
time, that extract and transform actually work together as one
pipeline instead of two separate pieces.

## What I built

`transform/clean.py` — four small, composable functions, each doing
one job:

- **`standardize_types()`** — fixes a real inconsistency Day 2's
  output actually surfaced: World Bank returns `year` as a string
  (`'2022'`), WHO returns it as an integer (`2011`). Every row leaving
  this function now has the same types regardless of source.
- **`filter_valid_countries()`** — drops rows whose country code isn't
  a real country (APIs sometimes mix in region aggregates like "Arab
  World" alongside actual countries).
- **`drop_missing_values()`** — drops rows where `value` is `None`,
  rather than letting a missing data point silently become `0` and
  corrupt any analysis built on top of it.
- **`deduplicate()`** — removes duplicate
  `(country_code, indicator_code, year)` combinations, mirroring the
  composite primary key from Day 1's schema.

All four are chained together in one `transform()` function — extract
hands it raw rows, it hands back clean ones. Every drop gets logged
with a reason, so nothing disappears silently.

## Proving it actually works — twice

**First, on deliberately messy fake data** — 5 rows with every problem
these functions exist to catch (mixed year types, a missing value, a
bad country code, an exact duplicate):
```
Input: 5 rows -> Output: 2 clean rows
INFO: Filtered out 1 rows with non-standard country codes
INFO: Dropped 1 rows with missing values
INFO: Removed 1 duplicate rows
```

**Then, chained directly to Tuesday's real extractor** — this was the
actual milestone of the day. A small script called
`fetch_world_bank()` and piped its real output straight into
`transform()`:
```
Extract stage: 15 raw rows fetched
Transform stage: 15 clean rows remain
{'country_code': 'GHA', 'year': 2022, 'value': 65.246, 'indicator_code': 'SP.DYN.LE00.IN'}
...
```
All 15 real rows survived transform cleanly — no bad data in this
batch — and every `year` came out as a proper integer, string
inconsistency gone. This is the first time two separate pieces of the
pipeline actually ran as one.

## Why this matters more than it might look like

It's easy to think of "clean the data" as a single step you do once.
The actual lesson today was that it's four *separate, testable*
decisions — what counts as a valid country, what to do with missing
values, how to catch duplicates, how to reconcile type mismatches
between sources — and keeping them as small named functions instead of
one tangled block is what makes each one independently checkable.

## Next up

Thursday: the load step — writing clean rows into Postgres using
`INSERT ... ON CONFLICT DO UPDATE`, so re-running the pipeline never
creates duplicates. That's the piece that finally makes today's clean
rows actually persist somewhere instead of just printing to a
terminal.

#DataEngineering #Python #ETL #DataCleaning #PostgreSQL #30DaysOfDataChallenge
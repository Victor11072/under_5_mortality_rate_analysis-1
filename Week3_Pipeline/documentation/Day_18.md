# Day 18/30 — Week 3: Load & idempotency

Days 1-3 built architecture, extraction, and cleaning — but none of it
persisted anywhere. Every run started from zero. Day 18 closed that
gap: writing the load step that actually stores clean data in
Postgres, designed so running the pipeline any number of times never
creates duplicates.

## The concept: idempotency

Idempotent means running the same operation twice produces the same
result as running it once. This matters because a pipeline that's
meant to run daily (or on a schedule, which is Friday's task) will
inevitably be re-run on data it's already loaded — a naive `INSERT`
would either error out on the second run or silently duplicate every
row.

## What made it possible

Monday's schema decision is what made today's task tractable: the
composite primary key on `indicator_values` —
`(country_code, indicator_code, year)` — means Postgres itself
enforces uniqueness on that combination. That let today's load
function use:

```sql
INSERT INTO indicator_values (country_code, indicator_code, year, value, fetched_at)
VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
ON CONFLICT (country_code, indicator_code, year)
DO UPDATE SET value = EXCLUDED.value, fetched_at = CURRENT_TIMESTAMP;
```

Instead of erroring on a duplicate key, Postgres just refreshes that
row's value. Metadata tables (`countries`, `indicators`) use
`ON CONFLICT DO NOTHING` instead, since country/indicator names
essentially never change — there's nothing to refresh, just avoid a
duplicate insert.

## Proving it, not just claiming it

The test loaded the same 2 rows twice in a row and queried the actual
row count afterward:

```
First load:
Loaded 2 rows (inserted or updated).
Second load (same rows again):
Loaded 2 rows (inserted or updated).
Rows in DB for TEST.IND after loading twice: 2
PASS: idempotent -- loading the same data twice did not create duplicates.
```

Two loads, still 2 rows. That's the actual mechanism behind Day 1's
"single command, no manual rework" goal — the pipeline can be re-run
safely, without me manually checking for or deleting duplicates first.

## The bigger milestone

This is the day the pipeline stopped being separate pieces that each
print to a terminal and became something that actually stores data.
Four days in, three of the four core stages — extract, transform,
load — are each individually proven against real infrastructure, not
mocked or simulated.

## Next up

Friday: scheduling and logging, so the pipeline can run unattended —
and likely the day these three proven pieces finally get chained into
one real entrypoint script.

#DataEngineering #PostgreSQL #Idempotency #Python #ETL #30DaysOfDataChallenge
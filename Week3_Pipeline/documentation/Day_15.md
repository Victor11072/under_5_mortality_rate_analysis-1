# Day 15/30 — Week 3: Building an automated data pipeline (World Bank + WHO)

Weeks 1 and 2 of this challenge were analysis: cleaning under-5 mortality
data by hand, then building a regression model on what drives it. Week 3
is a shift — instead of analyzing data once, I'm building a pipeline that
can fetch, clean, and store *fresh* World Bank and WHO indicator data on
demand, with no manual rework each time.

Today was architecture and schema — the foundation the rest of the week
builds on.

## The three questions driving this week

1. Can the pipeline fetch, clean, and store fresh data with a single
   command, no manual rework?
2. How do I design it so a new data source can be added without
   rewriting everything?
3. What automatic checks catch bad data before it reaches storage
   (missing countries, out-of-range values)?

## What I decided

**ETL, not ELT.** Cleaning happens in Python before data reaches the
database — the raw API responses aren't in a usable shape yet (nested
JSON, inconsistent country naming), so there's nothing meaningful to
load first and transform later.

**One standard shape, many sources.** Every source — World Bank, WHO,
and later HDX — will have its own extractor that knows that API's
quirks (pagination, field names), but all of them output the same four
columns: `country_code, indicator_code, year, value`. Transform and
load never know or care which API a row came from. Adding a new source
later means writing one new extractor, not touching anything downstream.
This is my answer to question 2.

**A composite primary key does the heavy lifting for question 1.**
`indicator_values` is keyed on `(country_code, indicator_code, year)`
together, not a single ID column. That's what will let me use
`INSERT ... ON CONFLICT DO UPDATE` later this week — running the whole
pipeline twice won't create duplicates, it'll just refresh the values.
That's the actual mechanism behind "single command, no manual rework."

## PostgreSQL over SQLite

The original plan used SQLite for simplicity. I chose to switch to
PostgreSQL instead, since this challenge exists to build a job-ready
portfolio — Postgres is what real data engineering work actually looks
like, and SQLite would have been the easier but less honest choice.

That decision turned today into more than a schema-design exercise —
I had to actually get Postgres running on Windows, which meant:

- Installing WSL2 (hit a mid-download timeout, just needed a retry)
- Installing Docker Desktop on top of WSL2
- Writing a `docker-compose.yml` so Postgres spins up with one command
- Confirming the schema applied with `psql`'s `\dt`

None of that was in the original plan for today, and it took longer
than the schema itself. But it's also the more honest story: a
functioning `docker-compose.yml` that a recruiter or another developer
could clone and run themselves is a stronger portfolio signal than a
schema diagram alone.

## The schema

```sql
countries (country_code PK, country_name)
indicators (indicator_code PK, indicator_name, source, unit)
indicator_values (
    country_code, indicator_code, year,   -- composite PK
    value, fetched_at
)
```

Verified live and working:
```
 Schema |       Name       | Type  |  Owner
--------+------------------+-------+----------
 public | countries        | table | postgres
 public | indicator_values | table | postgres
 public | indicators       | table | postgres
```

## What I'm still working through

I'm two months into data engineering, coming from a data science
background — this week is genuinely stretching me. The part I still
want to understand more deeply before Tuesday: exactly how the
column-renaming will work when World Bank calls a field
`countryiso3code` and WHO calls the same concept `SpatialDim`. The plan
is a small mapping dictionary per source, applied right after extract,
so transform never has to know which API a row came from — but I want
to see it work in code before I fully trust it.

## Next up

Tuesday: writing the actual extract functions that call the World Bank
and WHO APIs and handle pagination/errors gracefully.

#DataEngineering #PostgreSQL #Docker #30DaysOfDataChallenge #Python #ETL
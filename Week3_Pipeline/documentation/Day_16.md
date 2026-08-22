# Day 16/30 — Week 3: Writing reusable extract functions

Day 15 was architecture: designing the schema and getting a real Postgres
database running via Docker. Day 17 moved into actually pulling data —
writing extract functions that call the World Bank and WHO APIs and
handle pagination and errors gracefully, instead of the manual
requests/JSON digging I did in Weeks 1-2.

## What I built

**Two source-specific extractors, one shared foundation.**

- `extractors/base.py` — a `fetch_with_retry()` function used by both
  sources. If a request fails (timeout, server error, flaky
  connection), it retries up to 3 times with a short pause between
  attempts before giving up. This is reusable error handling, written
  once instead of copy-pasted into every extractor.

- `extractors/world_bank.py` — fetches indicator data from the World
  Bank API, looping through pages using their `page`/`pages` metadata
  until every page is collected.

- `extractors/who.py` — fetches indicator data from WHO's Global
  Health Observatory API, which paginates completely differently: it
  gives back a `@odata.nextLink` URL in every response, and you keep
  following that link until it stops appearing.

Both extractors rename their source's raw field names into the same
four standard columns (`country_code, indicator_code, year, value`)
before returning — so the pagination logic is source-specific, but the
*output* is identical no matter which API it came from. That was the
Day 1 architecture decision actually holding up in real code.

## What surprised me

**Two APIs, two totally different pagination strategies**, and neither
extractor needs to know the other exists. World Bank counts numbered
pages; WHO follows a chain of links. Handling that difference inside
each source's own file — instead of one tangled function trying to
handle both — is what makes it possible to add a third source later
without touching either of these files.

**A small but real inconsistency showed up in the actual data**: World
Bank returns `year` as a string (`'2022'`), WHO returns it as an
integer (`2011`). Nothing broke because of it, but it's now the first
concrete thing Wednesday's transform step needs to fix — not a
hypothetical "you'll need to clean data" lesson, but a real
inconsistency sitting in front of me.

## Getting it running was its own lesson

Writing the code was the easier half of today. Actually running it
surfaced a string of small, real environment issues — each one a
legitimate thing to learn from:

- Google Colab can't reach my local Postgres database at all — cloud
  notebooks and local infrastructure don't mix, so I switched to
  running everything through VS Code's terminal on my own machine
- `pip` wasn't recognized until I used `python -m pip` instead
- Files initially landed in the wrong folder, breaking the import
  path (`extractors.base` only resolves correctly when the file
  structure actually matches the import statement)
- `ModuleNotFoundError` when running the script directly — fixed by
  running it as a module instead: `python -m extractors.world_bank`
  rather than `python extractors/world_bank.py`

None of these were code bugs — they were environment/tooling
mismatches, which is its own category of debugging I hadn't had to do
much of in data science work.

## Proof it works — real output, not sample data

```
python -m extractors.world_bank
Fetched 9 rows
{'country_code': 'GHA', 'year': '2022', 'value': 65.246, 'indicator_code': 'SP.DYN.LE00.IN'}
...

python -m extractors.who
Fetched 198 rows
{'country_code': 'GHA', 'year': 2011, 'value': 62.58287212, 'indicator_code': 'WHOSIS_000001'}
...
```

Both pulled live data — Ghana, Kenya, and Nigeria life expectancy —
directly from the real World Bank and WHO APIs, no manual downloading.

## Important note on scope

This data isn't stored anywhere yet — it prints to the terminal and
nothing keeps it. Extract is only step one of Extract → Transform →
Validate → Load. Storage comes Thursday, once the load step exists.

## Next up

Wednesday: transform functions — standardizing country codes, handling
missing values, deduplication, and fixing the year-type inconsistency
between sources.

#DataEngineering #Python #ETL #PostgreSQL #APIs #30DaysOfDataChallenge
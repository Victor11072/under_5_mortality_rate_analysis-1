# Day 19/30 — Week 3: Scheduling & logging — the pipeline finally runs itself

Days 15-18 built the pieces: architecture, extraction, transformation,
idempotent loading. Day 19 tied all of them into one real entrypoint —
`run_pipeline.py` — and made it run completely unattended, without me
typing a single command.

## What I built

**One script chaining everything.** `run_pipeline.py` loops through
every indicator in `config.py`, calls the right extractor
(World Bank or WHO), passes the result through `transform()`, then
`load_rows()` — all in one command. This is the direct answer to Day
1's question 1: can the pipeline fetch, clean, and store fresh data
with a single command, no manual rework? Now, genuinely, yes.

**File-based logging.** Every run writes to `logs/pipeline_YYYYMMDD.log`
with timestamps on every step, not just the terminal — so a run that
happens while I'm not watching (which is the whole point of
scheduling) leaves a traceable record of exactly what happened.

**Per-indicator failure isolation.** Each indicator is wrapped in its
own try/except — one API failing doesn't crash the whole run, it logs
the failure and the loop moves on to the next indicator.

**Windows Task Scheduler** as cron's equivalent (cron doesn't exist on
Windows) — pointed at a small `run_pipeline.bat` wrapper, scheduled to
run daily.

## Proof it actually failed and recovered — for real

The very first real run hit an actual timeout calling the World Bank
API:
```
WARNING | Attempt 1/3 failed for .../SP.DYN.LE00.IN: Read timed out.
INFO    | SP.DYN.LE00.IN: fetched page 1/1
```
`extractors/base.py`'s retry logic — written back on Day 2 — caught
it, waited, and succeeded on the second attempt automatically. I
didn't see it fail from the outside; the pipeline just kept going. The
final result: **93 rows loaded, 0 failures.**

## Proof Task Scheduler actually ran it unattended

Set up a daily trigger, then triggered it manually to confirm without
waiting a full day. The log file caught it precisely:
```
11:45:10 - manual run: 93 rows loaded, 0 failures
11:52:53 - Task Scheduler run: 93 rows loaded, 0 failures
```
Two runs, same clean result — no terminal open, no me watching, just
a scheduled task firing the `.bat` file and the whole pipeline
executing on its own.

## Seeing the actual data, finally

After four days of pieces working "in theory," I queried Postgres
directly and saw real World Bank and WHO life expectancy data sitting
together for Ghana, Kenya, and Nigeria — same table, same columns,
despite coming from two completely different APIs:
```
country_code | indicator_code | year | value
GHA          | WHOSIS_000001  | 2000 | 59.08...
GHA          | WHOSIS_000001  | 2001 | 59.15...
...
GHA          | SP.DYN.LE00.IN | 2015 | 63.175
```
This is Day 1's architecture decision, made real — two sources, one
shape, one table.

## A scope note worth being honest about

Data is currently restricted to 3 countries (Nigeria, Kenya, Ghana) —
a deliberate test subset carried since Day 2, not a limitation of the
pipeline itself. Widening it to more countries is straightforward
(one line in `config.py`), but I'm holding off until Saturday's
validation step exists, since transform's country-filtering logic
would need updating alongside it — better to expand scope and
validation together than separately.

## Next up

Saturday: data quality checks (flagging outliers, asserting no missing
critical fields), a couple of tests, and pushing the whole thing to
GitHub with a README.

#DataEngineering #Python #ETL #Automation #PostgreSQL #30DaysOfDataChallenge
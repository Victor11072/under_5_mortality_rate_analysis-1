# Week 3 — Automated Data Pipeline

Moving from one-off analysis (Weeks 1-2) into repeatable data
infrastructure: an automated ETL pipeline that fetches World Bank and
WHO indicator data, cleans and validates it, and loads it into
PostgreSQL — idempotently, on a schedule, with traceable logging.

**Full project, setup instructions, and daily build log:**
[`week3_pipeline/`](Week3_Pipeline/documentation)

## What it demonstrates

- API extraction with pagination handling and automatic retries
- Reusable transform functions (type standardization, deduplication,
  missing-value handling)
- Data quality validation (out-of-range flagging, required-field checks)
- Idempotent database loading (`INSERT ... ON CONFLICT DO UPDATE`)
- Unattended scheduling via Windows Task Scheduler, with file-based logging
- 8 automated unit tests

## Daily build log

## Daily build log

[Day 1](Week3_Pipeline/documentation/Day_15.md) — Architecture & schema
[Day 2](Week3_Pipeline/documentation/Day_16.md) — Extract functions
[Day 3](Week3_Pipeline/documentation/Day_17.md) — Transform functions
[Day 4](Week3_Pipeline/documentation/Day_18.md) — Load & idempotency
[Day 5](Week3_Pipeline/documentation/Day_19.md) — Scheduling & logging
[Day 6](Week3_Pipeline/documentation/Day_20.md) — Validation, tests & shipping
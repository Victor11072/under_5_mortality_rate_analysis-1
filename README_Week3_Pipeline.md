# Week 3 — Automated Data Pipeline

Moving from one-off analysis (Weeks 1-2) into repeatable data
infrastructure: an automated ETL pipeline that fetches World Bank and
WHO indicator data, cleans and validates it, and loads it into
PostgreSQL — idempotently, on a schedule, with traceable logging.

**Full project, setup instructions, and daily build log:**
[`week3_pipeline/`](week3_pipeline/README.md)

## What it demonstrates

- API extraction with pagination handling and automatic retries
- Reusable transform functions (type standardization, deduplication,
  missing-value handling)
- Data quality validation (out-of-range flagging, required-field checks)
- Idempotent database loading (`INSERT ... ON CONFLICT DO UPDATE`)
- Unattended scheduling via Windows Task Scheduler, with file-based logging
- 8 automated unit tests

## Daily build log

[Day 1](week3_pipeline/day1_writeup.md) — Architecture & schema
[Day 2](week3_pipeline/day2_writeup.md) — Extract functions
[Day 3](week3_pipeline/day3_writeup.md) — Transform functions
[Day 4](week3_pipeline/day4_writeup.md) — Load & idempotency
[Day 5](week3_pipeline/day5_writeup.md) — Scheduling & logging
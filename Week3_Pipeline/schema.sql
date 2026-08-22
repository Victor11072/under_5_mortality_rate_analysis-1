-- schema.sql
-- Postgres schema for the World Bank / WHO indicator pipeline.
-- Run once (or via db_init.py) to set up the database structure.
-- Composite primary key on indicator_values is what makes the
-- Thursday load step idempotent: ON CONFLICT (country_code,
-- indicator_code, year) DO UPDATE lets a re-run overwrite rather
-- than duplicate a row.

CREATE TABLE IF NOT EXISTS countries (
    country_code CHAR(3) PRIMARY KEY,      -- ISO3 code, e.g. 'NGA'
    country_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS indicators (
    indicator_code TEXT PRIMARY KEY,       -- e.g. 'SP.DYN.LE00.IN'
    indicator_name TEXT NOT NULL,
    source TEXT NOT NULL,                  -- 'world_bank' or 'who'
    unit TEXT
);

CREATE TABLE IF NOT EXISTS indicator_values (
    country_code   CHAR(3) NOT NULL REFERENCES countries(country_code),
    indicator_code TEXT    NOT NULL REFERENCES indicators(indicator_code),
    year           INTEGER NOT NULL,
    value          NUMERIC,
    fetched_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (country_code, indicator_code, year)
);

-- Helpful for validation-step lookups later (Saturday's task).
CREATE INDEX IF NOT EXISTS idx_indicator_values_year
    ON indicator_values(year);

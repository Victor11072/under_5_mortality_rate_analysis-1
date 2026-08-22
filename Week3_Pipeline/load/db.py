"""
load/db.py

Writes clean rows (from transform.clean.transform()) into Postgres.
Uses INSERT ... ON CONFLICT DO UPDATE so running the pipeline multiple
times never creates duplicates -- a re-run just refreshes existing
values. This is what "idempotent" means in practice.
"""

import os
import logging
import psycopg2
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()  # reads .env into environment variables


def get_connection():
    """
    Opens a connection to Postgres using credentials from .env.
    Centralized here so every load function shares one connection
    method -- if credentials ever change, this is the only place
    to update.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "wb_who_data"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def ensure_country(cur, country_code, country_name=None):
    """
    Inserts a country if it doesn't already exist. ON CONFLICT DO
    NOTHING here (not DO UPDATE) because country names essentially
    never change -- if the row exists, there's nothing to refresh.
    """
    cur.execute(
        """
        INSERT INTO countries (country_code, country_name)
        VALUES (%s, %s)
        ON CONFLICT (country_code) DO NOTHING
        """,
        (country_code, country_name or country_code),
    )


def ensure_indicator(cur, indicator_code, indicator_name=None, source=None, unit=None):
    """
    Same idea as ensure_country -- indicator metadata rarely changes,
    so DO NOTHING on conflict is correct here too.
    """
    cur.execute(
        """
        INSERT INTO indicators (indicator_code, indicator_name, source, unit)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (indicator_code) DO NOTHING
        """,
        (indicator_code, indicator_name or indicator_code, source or "unknown", unit),
    )


def load_rows(rows, source="unknown"):
    """
    The main entrypoint: takes clean rows from transform() and writes
    them to Postgres idempotently. Safe to call with the same rows
    multiple times -- values get refreshed, never duplicated.
    """
    if not rows:
        logger.info("No rows to load.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    try:
        for row in rows:
            ensure_country(cur, row["country_code"])
            ensure_indicator(cur, row["indicator_code"], source=source)

            # THE key line: ON CONFLICT DO UPDATE is what makes this
            # idempotent. Same (country_code, indicator_code, year)
            # -> value gets refreshed instead of erroring or duplicating.
            cur.execute(
                """
                INSERT INTO indicator_values
                    (country_code, indicator_code, year, value, fetched_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (country_code, indicator_code, year)
                DO UPDATE SET value = EXCLUDED.value,
                              fetched_at = CURRENT_TIMESTAMP
                """,
                (row["country_code"], row["indicator_code"], row["year"], row["value"]),
            )
            inserted += 1

        conn.commit()  # nothing is actually saved until this runs
        logger.info(f"Loaded {inserted} rows (inserted or updated).")
    except Exception as e:
        conn.rollback()  # undo everything from this run if any row failed
        logger.error(f"Load failed, rolled back: {e}")
        raise
    finally:
        cur.close()
        conn.close()

    return inserted


if __name__ == "__main__":
    # Manual idempotency test: load the same 2 rows TWICE and prove
    # the row count in the database doesn't double.
    logging.basicConfig(level=logging.INFO)

    test_rows = [
        {"country_code": "NGA", "indicator_code": "TEST.IND", "year": 2022, "value": 1.0},
        {"country_code": "KEN", "indicator_code": "TEST.IND", "year": 2022, "value": 2.0},
    ]

    print("First load:")
    load_rows(test_rows, source="test")

    print("\nSecond load (same rows again):")
    load_rows(test_rows, source="test")

    # Verify: query the count for these test rows -- should be 2, not 4
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM indicator_values WHERE indicator_code = 'TEST.IND'"
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    print(f"\nRows in DB for TEST.IND after loading twice: {count}")
    assert count == 2, "Idempotency broken -- duplicates were created!"
    print("PASS: idempotent -- loading the same data twice did not create duplicates.")
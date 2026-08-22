# Day 20/30 — Week 3 complete: validation, tests, and shipping to GitHub

Six days ago I started Week 3 admitting I was two months into data
engineering, coming from a data science background, and unsure if a
full ETL pipeline was realistic on that timeline. Today it's live on
GitHub — tested, validated, and running unattended.

## What I added today

**Validation** — a step between transform and load that asks a
different question than cleaning does: does this whole *batch* look
right? Concretely: are values inside a believable range (life
expectancy has to be 20-100, not 999), are required fields actually
present, is the batch non-empty. Out-of-range values get flagged and
dropped; a genuinely broken batch gets rejected before it ever reaches
Postgres.

**8 automated tests** — replacing "run a script and read the output"
with `python -m unittest tests.test_pipeline -v`, which checks every
rule the pipeline enforces (type standardization, missing-value
handling, deduplication, invalid-country filtering, empty-batch
rejection, out-of-range flagging) automatically, every time.

**Wiring validate() into the real pipeline** — the architecture from
Day 1 is now fully real: Extract → Transform → **Validate** → Load,
not just a diagram.

## A real failure caught the moment it mattered

While confirming the wired-in validation step, a run hit a genuine
infrastructure failure — Postgres wasn't reachable because Docker
wasn't running:
```
ERROR | FAILED processing SP.DYN.LE00.IN from world_bank: connection
to server at "localhost" ... Connection refused
```
No crash, no silent data loss — the log caught it precisely, both
indicators failed cleanly and separately, and the fix was as simple as
starting Docker. Re-running afterward: 93 rows, 0 failures. This is
the exact scenario all of this week's logging and error-handling work
was for.

## Shipped to GitHub

The pipeline now lives in my existing 30-day-challenge repo, alongside
Weeks 1-2, as its own self-contained folder — README, architecture
notes, and the full daily build log included. Getting there surfaced
a few real lessons of its own: a `.gitignore` file silently doing
nothing because it was missing its leading dot, `.env.example` vs.
the real `.env` (only the template belongs in a public repo), and
making sure a virtual environment never gets committed.

## What Week 3 actually proved

Looking back at Day 1's three research questions:

1. **Can it fetch, clean, and store data with one command, no manual
   rework?** Yes — `python run_pipeline.py` does the whole thing.
2. **Can a new source be added without rewriting everything?** Yes —
   each source is its own extractor outputting the same standard
   shape; adding a third source means writing one new file.
3. **What catches bad data before storage?** A real validation layer
   — range checks, required-field checks, empty-batch checks — not
   just hope.

Six days ago this felt like it might be too much for someone two
months into DE. It wasn't — it just required slowing down, asking
"why" before typing code, and treating every environment error (WSL,
Docker, import paths, PowerShell syntax) as a real lesson instead of
a distraction from the "real" work. Turns out that *was* the real
work.

#DataEngineering #Python #PostgreSQL #ETL #Docker #Testing #30DaysOfDataChallenge
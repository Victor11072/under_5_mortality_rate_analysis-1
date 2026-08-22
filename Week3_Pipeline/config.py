"""
config.py

Central place listing what the pipeline fetches. Changing what data
you pull means editing this file only -- run_pipeline.py itself never
needs to change.
"""

COUNTRIES_WORLD_BANK = "NGA;KEN;GHA"     # World Bank's semicolon syntax
COUNTRIES_WHO = ["NGA", "KEN", "GHA"]    # WHO's list syntax

START_YEAR = 2015
END_YEAR = 2023

# Each entry: (indicator_code, source)
INDICATORS = [
    ("SP.DYN.LE00.IN", "world_bank"),   # life expectancy at birth
    ("WHOSIS_000001", "who"),           # life expectancy at birth (WHO's version)
]
# Healthcare Data Breach Risk Analysis

Analysis of large healthcare data breaches reported to the U.S. HHS Office for Civil Rights, comparing healthcare providers and business associates, with a Massachusetts focus.

## Status
- [x] Data cleaning pipeline
- [ ] SQL analysis
- [ ] Statistics (median vs. mean)
- [ ] Dashboard
- [ ] Risk brief

## Data
Source: HHS OCR Breach Portal (breaches affecting 500+ people), downloaded 2026-11-23.
Raw files are in `data/raw`, cleaned data in `data/clean`.

## How to run
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python src/clean_data.py

## Cleaning
See `docs/cleaning_log.md` (what changed, with counts) and `docs/cleaning_decisions.md` (why).

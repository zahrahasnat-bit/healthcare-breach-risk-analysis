# Healthcare Data Breach Risk Analysis

Analysis of large healthcare data breaches reported to the U.S. HHS Office for Civil Rights (OCR), comparing healthcare providers and business associates, with a Massachusetts focus.

## Status
- [x] Data cleaning pipeline
- [x] SQL analysis
- [x] Statistics (median vs. mean)
- [x] Dashboard
- [x] Risk brief

## Data
Source: HHS OCR Breach Portal (breaches affecting 500+ people), downloaded 2026-11-23. Data runs through 2026-10-16.
Raw files are in `data/raw`, cleaned data in `data/clean`. After cleaning: 8,087 breaches.

## Key findings
- **Mean vs. median:** the typical (median) breach affects 4,036 people, but the mean is 137,328. A few mega-breaches (Change Healthcare, about 192.7 million) pull the mean up, so the median describes a typical incident better.
- **Business associates concentrate risk:** they are about 15% of breaches (1,244 of 8,087) but account for about 49% of all people affected (about 545 million). Their median is 5,890 vs. 3,915 for healthcare providers.
- **Hacking dominates:** hacking/IT incidents are 4,898 breaches (about 61%), have the highest median size (8,132), and account for about 1.01 billion people affected.
- **Massachusetts looks like the nation overall:** median 4,049 vs. 4,035 for the rest of the US, ranking 8th with 245 breaches. Providers are 167 of the 245 (68%), with a smaller median (2,739).
- **Typical breach size rose after 2018:** medians were about 2,000 to 2,700 through 2018 and 4,000 to 8,000 from 2019 on. This data cannot show why (more breaches, more reporting, or both).

## Limitations
- Only breaches affecting 500+ people are listed, so this describes large breaches only.
- 2009 and 2026 are partial years.
- HHS can amend records after posting, so this is a snapshot of the portal on the download date.
- `breach_type_primary` keeps only the first listed breach type.
- Small groups (for example, 18 Massachusetts health plan breaches) are too small for strong conclusions.

## How to run
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python src/clean_data.py
    python src/load_to_sqlite.py
    python src/run_queries.py
    python src/stats.py
    python src/histogram.py

## Project structure
- `src/clean_data.py`: cleans and combines the raw exports
- `src/load_to_sqlite.py`: loads the cleaned data into a SQLite database
- `sql/queries.sql` and `src/run_queries.py`: counts, totals, and rankings in SQL
- `src/stats.py`: median vs. mean by entity type, year, breach type, and state
- `src/histogram.py`: log-scale histogram of breach sizes (saved to `images/`)
- `docs/cleaning_log.md` (what changed) and `docs/cleaning_decisions.md` (why)

- `src/dashboard.py`: builds the interactive Plotly dashboard (`images/dashboard.html`, open in a browser)
- `docs/brief.md`: one-page risk brief

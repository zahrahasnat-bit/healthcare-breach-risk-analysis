# Cleaning Log

- Loaded data/raw/breach_under_investigation.csv: 692 rows. Renamed 2 broken placeholder headers to real names.
- Loaded data/raw/breach_archive.csv: 7401 rows. Renamed 2 broken placeholder headers to real names.
- Data downloaded from the HHS OCR breach portal on 2026-11-23. Combined both files: 8093 rows, 9 columns.
- Renamed columns to snake_case: ['name_of_covered_entity', 'state', 'covered_entity_type', 'individuals_affected', 'breach_submission_date', 'type_of_breach', 'location_of_breached_information', 'business_associate_present', 'web_description']
- Missing values before cleaning: {'state': 23, 'covered_entity_type': 5, 'individuals_affected': 1, 'type_of_breach': 1, 'web_description': 948}
- Stripped spaces and lowercased: ['name_of_covered_entity', 'covered_entity_type', 'type_of_breach', 'location_of_breached_information', 'business_associate_present']
- Stripped spaces and uppercased the state column (e.g., 'ma' -> 'MA').
- Converted individuals_affected to numbers (unreadable values became missing).
- Converted breach_submission_date to real dates (month/day/year) and added breach_year. Unreadable dates: 0.
- Removed 2 exact duplicate rows (kept first copy).
- Removed 4 more rows with the same name, date, and size (same breach listed twice).
- Added breach_type_primary = the first breach type listed, for simple grouping later.
- Missing values remaining (rows kept; filter per analysis later): {'state': 23, 'covered_entity_type': 5, 'individuals_affected': 1, 'type_of_breach': 1, 'web_description': 946, 'breach_type_primary': 1}
- Saved cleaned data: 8087 rows to data/clean/breaches_clean.csv.

# Cleaning Decisions: Why I Did It

## Data source
- HHS OCR Breach Portal ("HIPAA Cases Currently Under Investigation" and "Archive"), downloaded 2026-11-23.
- The portal lists only breaches affecting 500 or more people, so this analysis describes large breaches only.
- Not included: the separate "Part 2" breach list (a different set of rules).

## Choices and reasons
- **Fixed broken headers:** the export named two columns with technical placeholder text. I identified them by position and by checking their contents (entity names; yes/no values).
- **Lowercased and stripped labels:** otherwise "Business Associate" and "business associate " would be counted as different groups.
- **Removed duplicates:** the same breach counted twice would inflate counts and totals. I removed 2 exact duplicates and 4 rows that matched on name, date, and size.
- **Kept rows with missing values:** dropping them would undercount breaches. I filter only when a statistic needs the value (for example, median size, which is missing for 1 row).
- **Parsed dates and added breach_year:** to compare trends over time.
- **Added breach_type_primary:** many breaches list several types. I kept the first for simple grouping. Limitation: it ignores the others.

## Results of cleaning
- 8,093 rows combined, 8,087 after removing duplicates.
- Provider: 5,847 breaches. Business associate: 1,244. Health plan: 974. Clearing house: 17.
- Median individuals affected: 4,036. Mean: about 137,328. The mean is far higher because a few huge breaches pull it up.
- Massachusetts: 245 breaches.

## Known limitations
- 2009 and 2026 are partial years (data runs through 2026-10-16).
- HHS can amend records after posting, so this is a snapshot of the portal on the download date.
- Some breaches use placeholder sizes until the real number is known.
- A few very large breaches (for example, Change Healthcare, about 192.7 million) dominate totals and means. I report medians alongside means for this reason.

import re
import pandas as pd

RAW_FILES = [
    "data/raw/breach_under_investigation.csv",
    "data/raw/breach_archive.csv",
]
CLEAN_PATH = "data/clean/breaches_clean.csv"
LOG_PATH = "docs/cleaning_log.md"

# ---- Tiny logging helper: prints a message and remembers it for the log file ----
log_lines = []

def log(message):
    print(message)
    log_lines.append(f"- {message}")

# ---- 1. Load each file and fix the broken headers ----
# The portal export names two columns "javax.faces.component.UIPanel@<random>".
# In order, they are the entity name (first) and "Business Associate Present" (later).
REAL_NAMES = ["Name of Covered Entity", "Business Associate Present"]

def load_and_fix(path):
    d = pd.read_csv(path)
    fixed = []
    junk_count = 0
    for col in d.columns:
        if str(col).startswith("javax.faces"):
            fixed.append(REAL_NAMES[junk_count])
            junk_count += 1
        else:
            fixed.append(col)
    d.columns = fixed
    return d, junk_count

frames = []
for path in RAW_FILES:
    d, n_fixed = load_and_fix(path)
    log(f"Loaded {path}: {len(d)} rows. Renamed {n_fixed} broken placeholder headers to real names.")
    frames.append(d)

df = pd.concat(frames, ignore_index=True)
log(f"Data downloaded from the HHS OCR breach portal on 2026-11-23. Combined both files: {len(df)} rows, {df.shape[1]} columns.")

# ---- 2. Rename columns to lowercase_with_underscores ----
def to_snake(name):
    name = name.strip().lower()
    return re.sub(r"[^a-z0-9]+", "_", name).strip("_")

df.columns = [to_snake(c) for c in df.columns]
log(f"Renamed columns to snake_case: {df.columns.tolist()}")

# ---- 3. Report missing values BEFORE cleaning ----
missing = df.isna().sum()
missing = missing[missing > 0]
log(f"Missing values before cleaning: {missing.to_dict()}")

# ---- 4. Standardize text labels ----
text_cols = [
    "name_of_covered_entity",
    "covered_entity_type",
    "type_of_breach",
    "location_of_breached_information",
    "business_associate_present",
]
for col in text_cols:
    df[col] = df[col].astype("string").str.strip().str.lower()
log(f"Stripped spaces and lowercased: {text_cols}")

df["state"] = df["state"].astype("string").str.strip().str.upper()
log("Stripped spaces and uppercased the state column (e.g., 'ma' -> 'MA').")

# ---- 5. Fix the numeric column ----
df["individuals_affected"] = pd.to_numeric(df["individuals_affected"], errors="coerce")
log("Converted individuals_affected to numbers (unreadable values became missing).")

# ---- 6. Parse dates and extract the year ----
df["breach_submission_date"] = pd.to_datetime(
    df["breach_submission_date"], format="%m/%d/%Y", errors="coerce"
)
df["breach_year"] = df["breach_submission_date"].dt.year
bad_dates = int(df["breach_submission_date"].isna().sum())
log(f"Converted breach_submission_date to real dates (month/day/year) and added breach_year. Unreadable dates: {bad_dates}.")

# ---- 7. Remove duplicates (after cleaning labels, so near-matches are caught) ----
exact_dupes = int(df.duplicated().sum())
df = df.drop_duplicates()
log(f"Removed {exact_dupes} exact duplicate rows (kept first copy).")

key_cols = ["name_of_covered_entity", "breach_submission_date", "individuals_affected"]
key_dupes = int(df.duplicated(subset=key_cols).sum())
df = df.drop_duplicates(subset=key_cols)
log(f"Removed {key_dupes} more rows with the same name, date, and size (same breach listed twice).")

# ---- 8. Primary breach type (first one listed) ----
df["breach_type_primary"] = df["type_of_breach"].str.split(",").str[0].str.strip()
log("Added breach_type_primary = the first breach type listed, for simple grouping later.")

# ---- 9. Record remaining missing values (kept, not dropped) ----
still_missing = df.isna().sum()
still_missing = still_missing[still_missing > 0]
log(f"Missing values remaining (rows kept; filter per analysis later): {still_missing.to_dict()}")

# ---- 10. Save outputs ----
df.to_csv(CLEAN_PATH, index=False)
log(f"Saved cleaned data: {len(df)} rows to {CLEAN_PATH}.")

with open(LOG_PATH, "w") as f:
    f.write("# Cleaning Log\n\n")
    f.write("\n".join(log_lines))
    f.write("\n")
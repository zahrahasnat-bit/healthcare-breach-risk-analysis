import sqlite3
import pandas as pd

# Read the cleaned CSV; parse_dates turns the date column back into real dates
df = pd.read_csv("data/clean/breaches_clean.csv", parse_dates=["breach_submission_date"])

# SQLite has no date type, so store dates as plain text like 2026-10-16
df["breach_submission_date"] = df["breach_submission_date"].dt.strftime("%Y-%m-%d")

# We don't need the long description text for analysis, so drop it to keep the database small
df = df.drop(columns=["web_description"])

# Connect (this creates the file if it doesn't exist)
conn = sqlite3.connect("data/breaches.db")

# Copy the DataFrame into a table named "breaches", replacing it if it exists
df.to_sql("breaches", conn, if_exists="replace", index=False)

# Check it worked
count = conn.execute("SELECT COUNT(*) FROM breaches").fetchone()[0]
print("Rows in database table:", count)

conn.close()
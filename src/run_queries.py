import sqlite3
import pandas as pd

conn = sqlite3.connect("data/breaches.db")

# Read the .sql file and split it into separate queries at each semicolon
with open("sql/queries.sql") as f:
    queries = [q.strip() for q in f.read().split(";") if q.strip()]

pd.set_option("display.width", 200)

for q in queries:
    # The first line of each block is the "-- Q1: ..." comment; use it as a title
    title = q.splitlines()[0]
    print("=" * 70)
    print(title)
    print(pd.read_sql_query(q, conn).to_string(index=False))
    print()

conn.close()

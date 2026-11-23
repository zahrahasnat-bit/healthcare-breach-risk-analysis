import pandas as pd

# Load each file separately so we can compare them
df_open = pd.read_csv("data/raw/breach_under_investigation.csv")
df_arch = pd.read_csv("data/raw/breach_archive.csv")

for name, d in [("UNDER INVESTIGATION", df_open), ("ARCHIVE", df_arch)]:
    print("=" * 60)
    print(name)
    print("=" * 60)
    print("Shape (rows, columns):", d.shape)
    print("\nColumn names:")
    print(d.columns.tolist())
    print("\nFirst 3 rows:")
    print(d.head(3).to_string())
    print("\nInfo (types and non-null counts):")
    d.info()
    print("\nMissing values per column:")
    print(d.isna().sum())
    print()
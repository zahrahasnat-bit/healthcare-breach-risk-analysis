import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.float_format", "{:,.0f}".format)

df = pd.read_csv("data/clean/breaches_clean.csv")

# Only rows that have a size can be used for size statistics
sized = df.dropna(subset=["individuals_affected"])
print("Rows used for size statistics:", len(sized), "\n")

def summarize(data, by, label):
    """Count, median, mean, and mean/median ratio for each group."""
    out = data.groupby(by)["individuals_affected"].agg(
        breaches="count", median="median", mean="mean"
    )
    out["mean_to_median"] = (out["mean"] / out["median"]).round(1)
    print("=" * 70)
    print(label)
    print(out.sort_values("breaches", ascending=False).to_string())
    print()
    return out

# Overall
print("OVERALL: median =", f"{sized['individuals_affected'].median():,.0f}",
      "| mean =", f"{sized['individuals_affected'].mean():,.0f}", "\n")

summarize(sized, "covered_entity_type", "BY ENTITY TYPE")
summarize(sized, "breach_year", "BY YEAR")
summarize(sized, "breach_type_primary", "BY BREACH TYPE")

# Massachusetts vs. the rest of the country
sized = sized.copy()
sized["is_ma"] = sized["state"].eq("MA").map({True: "MA", False: "Rest of US"})
summarize(sized, "is_ma", "MASSACHUSETTS VS. REST OF US")

# MA broken down by entity type
ma = sized[sized["state"] == "MA"]
summarize(ma, "covered_entity_type", "MASSACHUSETTS BY ENTITY TYPE")
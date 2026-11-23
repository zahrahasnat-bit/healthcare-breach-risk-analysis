import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

df = pd.read_csv("data/clean/breaches_clean.csv")
sized = df.dropna(subset=["individuals_affected", "covered_entity_type"]).copy()

# Short, readable labels for the charts
sized["entity"] = sized["covered_entity_type"].str.title()

# ---- Chart 1: breaches and median size by entity type ----
by_entity = (
    sized.groupby("entity")["individuals_affected"]
    .agg(breaches="count", median="median")
    .reset_index()
    .sort_values("breaches", ascending=False)
)
fig1 = px.bar(
    by_entity, x="entity", y="breaches", text="breaches",
    hover_data={"median": ":,.0f"},
    title="Breaches by entity type (hover for median size)",
    labels={"entity": "Entity type", "breaches": "Number of breaches"},
)
fig1.update_traces(marker_color="#2b6cb0")

# ---- Chart 2: yearly trend, median size by entity type ----
# Leave out 2009 (partial) and 2026 (partial, through Oct 16)
trend = sized[sized["breach_year"].between(2010, 2025)]
trend = trend[trend["entity"].isin(["Healthcare Provider", "Business Associate"])]
by_year = (
    trend.groupby(["breach_year", "entity"])["individuals_affected"]
    .agg(breaches="count", median="median")
    .reset_index()
)
fig2 = px.line(
    by_year, x="breach_year", y="median", color="entity", markers=True,
    hover_data={"breaches": True},
    title="Median breach size by year: providers vs. business associates (2010-2025)",
    labels={"breach_year": "Year", "median": "Median individuals affected", "entity": ""},
)

# ---- Chart 3: Massachusetts vs. the rest of the US ----
sized["region"] = sized["state"].eq("MA").map({True: "Massachusetts", False: "Rest of US"})
core = sized[sized["entity"].isin(["Healthcare Provider", "Business Associate", "Health Plan"])]
region = (
    core.groupby(["region", "entity"])["individuals_affected"]
    .agg(breaches="count", median="median")
    .reset_index()
)
fig3 = px.bar(
    region, x="entity", y="median", color="region", barmode="group",
    text=region["median"].round(0).map("{:,.0f}".format),
    hover_data={"breaches": True},
    title="Median breach size: Massachusetts vs. rest of US",
    labels={"entity": "Entity type", "median": "Median individuals affected", "region": ""},
)

# ---- Write everything into one HTML page ----
html_parts = [
    "<html><head><meta charset='utf-8'><title>Healthcare Breach Dashboard</title></head>",
    "<body style='font-family:sans-serif;max-width:1000px;margin:auto;padding:20px'>",
    "<h1>Healthcare Data Breach Dashboard</h1>",
    "<p>Source: HHS OCR breach portal (500+ individuals), data through 2026-10-16. "
    "Medians are used because a few mega-breaches inflate averages.</p>",
]
for i, fig in enumerate([fig1, fig2, fig3]):
    html_parts.append(fig.to_html(full_html=False, include_plotlyjs="cdn" if i == 0 else False))
html_parts.append("</body></html>")

with open("images/dashboard.html", "w") as f:
    f.write("\n".join(html_parts))
print("Saved images/dashboard.html")
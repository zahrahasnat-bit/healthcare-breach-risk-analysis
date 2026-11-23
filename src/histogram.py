import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean/breaches_clean.csv").dropna(subset=["individuals_affected"])
sizes = df["individuals_affected"]

# Bins that are evenly spaced on a log scale, from 500 up to the max
bins = np.logspace(np.log10(sizes.min()), np.log10(sizes.max()), 40)

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(sizes, bins=bins, color="#2b6cb0", edgecolor="white")
ax.set_xscale("log")

# Mark the median and mean so the gap is visible
ax.axvline(sizes.median(), color="green", linestyle="--", label=f"Median: {sizes.median():,.0f}")
ax.axvline(sizes.mean(), color="red", linestyle="--", label=f"Mean: {sizes.mean():,.0f}")

ax.set_xlabel("Individuals affected (log scale)")
ax.set_ylabel("Number of breaches")
ax.set_title("Healthcare breach sizes (HHS OCR, 500+ individuals)")
ax.legend()

plt.tight_layout()
plt.savefig("images/breach_size_histogram.png", dpi=150)
print("Saved images/breach_size_histogram.png")
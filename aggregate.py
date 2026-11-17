"""
ISM2411 Lab 15 — Aggregate & Chart — Capstone Warm-up
Author: Layton Niemier

Run from the repo root:
    python aggregate.py

Reads data/clean_sales.csv (the cleaned file from Lab 14), prints the
summary numbers for each question, and saves four charts into charts/.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # save PNGs without needing a display window
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = Path("data/clean_sales.csv")
CHART_DIR = Path("charts")
CHART_DIR.mkdir(exist_ok=True)

# Colors used across every chart so they look like one set
BLUE = "#2a78d6"      # main highlight color
ORANGE = "#eb6834"    # second series (Q4 only)
GRAY = "#b9b8b3"      # de-emphasized bars
DARK_GRAY = "#52514e" # reference lines and notes

plt.rcParams.update({
    "figure.dpi": 120,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.titlesize": 13,
})


def dollars(x):
    """Format a number like $565,862 (or -$2,000 for negatives)."""
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


# ---------------------------------------------------------------------------
# Load the data
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df["order_date"] = pd.to_datetime(df["order_date"])  # parse dates before using .dt
print(f"Loaded {len(df):,} orders from {DATA_PATH}")
print(f"Date range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")
print(f"Total revenue: {dollars(df['revenue'].sum())}\n")


# ===========================================================================
# Q1: Revenue by region  (Exercise 1)
# Business question: Which region brings in the most revenue?
# ===========================================================================
region_rev = (
    df.groupby("region")["revenue"].sum()
    .reset_index()
    .sort_values("revenue", ascending=False)
)
print("Q1 — Revenue by region")
print(region_rev.to_string(index=False), "\n")

top_region = region_rev.iloc[0]
avg_region_rev = region_rev["revenue"].mean()

fig, ax = plt.subplots(figsize=(8, 5))
# Highlight the top region in blue; keep the rest gray so the answer pops
bar_colors = [BLUE if r == top_region["region"] else GRAY for r in region_rev["region"]]
bars = ax.bar(region_rev["region"], region_rev["revenue"], color=bar_colors, width=0.6)
ax.bar_label(bars, labels=[dollars(v) for v in region_rev["revenue"]], padding=3, fontsize=9)
ax.set_title(f"{top_region['region']} Region Leads 2025 Revenue")
ax.set_xlabel("Region")
ax.set_ylabel("Total Revenue (USD)")
ax.yaxis.set_major_formatter(lambda v, _: dollars(v))
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(CHART_DIR / "q1_revenue_by_region.png")
plt.close(fig)

q1_pct_above = (top_region["revenue"] / avg_region_rev - 1) * 100
q1_sentence = (
    f"The {top_region['region']} region was the top region with "
    f"{dollars(top_region['revenue'])} in revenue, {q1_pct_above:.0f}% above the "
    f"average region ({dollars(avg_region_rev)})."
)
print("Q1 finding:", q1_sentence, "\n")
# Q1 finding: The South region was the top region with $565,862 in revenue,
# 58% above the average region ($357,172).
# (Note: "Unknown" is the 108 orders Lab 14 couldn't match to a region.)

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


# ===========================================================================
# Q2: Monthly revenue trend  (Exercise 2)
# Business question: How does revenue change month to month, and when is the peak?
# ===========================================================================
df["month"] = df["order_date"].dt.month
monthly = df.groupby("month")["revenue"].sum().reset_index()
print("Q2 — Revenue by month")
print(monthly.to_string(index=False), "\n")

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
avg_month = monthly["revenue"].mean()
peak = monthly.loc[monthly["revenue"].idxmax()]
peak_name = month_names[int(peak["month"]) - 1]

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(monthly["month"], monthly["revenue"], marker="o", markersize=7,
        linewidth=2, color=BLUE, label="Monthly revenue")
ax.axhline(avg_month, color=DARK_GRAY, linestyle="--", linewidth=1,
           label=f"Monthly average ({dollars(avg_month)})")
ax.annotate(f"Peak: {peak_name}\n{dollars(peak['revenue'])}",
            xy=(peak["month"], peak["revenue"]),
            xytext=(peak["month"] - 2.6, peak["revenue"] - 8000),
            fontsize=9, arrowprops=dict(arrowstyle="->", color=DARK_GRAY))
ax.set_xticks(range(1, 13))           # all 12 months on the x-axis
ax.set_xticklabels(month_names)
ax.set_title("Revenue Climbs Into a December Peak")
ax.set_xlabel("Month (2025)")
ax.set_ylabel("Total Revenue (USD)")
ax.yaxis.set_major_formatter(lambda v, _: dollars(v))
ax.grid(axis="y", alpha=0.3)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(CHART_DIR / "q2_monthly_trend.png")
plt.close(fig)

q2_pct_above = (peak["revenue"] / avg_month - 1) * 100
q2_sentence = (
    f"{peak_name} was the peak month with {dollars(peak['revenue'])} in revenue, "
    f"{q2_pct_above:.1f}% above the monthly average of {dollars(avg_month)}."
)
print("Q2 finding:", q2_sentence, "\n")
# Q2 finding: Dec was the peak month with $197,308 in revenue, 32.6% above the
# monthly average of $148,822.


# ===========================================================================
# Q3: Order size distribution  (Exercise 3 — redone in Seaborn for Exercise 5)
# Business question: What does a typical order look like, and is the mean misleading?
# ===========================================================================
median_order = df["revenue"].median()
mean_order = df["revenue"].mean()
skewness = df["revenue"].skew()
print("Q3 — Order size")
print(f"Median order size: {dollars(median_order)}  (exact: {median_order:.2f})")
print(f"Mean order size:   {dollars(mean_order)}  (exact: {mean_order:.2f})")
print(f"Skewness: {skewness:.2f}\n")

# --- Original matplotlib version (replaced by Seaborn below for Exercise 5) ---
# fig, ax = plt.subplots(figsize=(9, 5))
# ax.hist(df["revenue"], bins=20, color=BLUE, edgecolor="white")
# ax.set_title("Most Orders Are Small; a Few Big Ones Pull the Mean Up")
# ax.set_xlabel("Order Revenue (USD)")
# ax.set_ylabel("Number of Orders")
# fig.savefig(CHART_DIR / "q3_order_distribution.png")

# --- Seaborn version (Exercise 5) ---
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(data=df, x="revenue", bins=20, color=BLUE, edgecolor="white", ax=ax)
ax.axvline(median_order, color=DARK_GRAY, linestyle="--", linewidth=1.5,
           label=f"Median {dollars(median_order)}")
ax.axvline(mean_order, color=ORANGE, linestyle="-", linewidth=1.5,
           label=f"Mean {dollars(mean_order)}")
ax.set_title("Most Orders Are Small; a Few Big Ones Pull the Mean Up")
ax.set_xlabel("Order Revenue (USD)")
ax.set_ylabel("Number of Orders")
ax.xaxis.set_major_formatter(lambda v, _: dollars(v))
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(CHART_DIR / "q3_order_distribution.png")
plt.close(fig)

# Exercise 5 — one difference I noticed:
# sns.histplot takes the DataFrame and the column name directly (data=df, x="revenue"),
# so I don't have to pull the column out myself, and it labels the x-axis with the
# column name automatically. The bars look the same, but Seaborn's default styling
# is a little cleaner, and switching to a KDE curve or splitting by a category
# (hue="region") is just one extra argument, which would take several lines in
# plain matplotlib. The amount of code for the basic chart was about the same.

q3_sentence = (
    f"The distribution is strongly right-skewed (skewness {skewness:.2f}): the median "
    f"order is {dollars(median_order)} but the mean is {dollars(mean_order)}, because a "
    f"small number of large orders pull the average up. An analyst describing a "
    f"'typical' order should use the median; the mean is still useful for totals and "
    f"forecasting revenue."
)
print("Q3 finding:", q3_sentence, "\n")
# Q3 finding: The distribution is strongly right-skewed (skewness 3.79): the median
# order is $141 but the mean is $382, because a small number of large orders pull
# the average up. An analyst describing a "typical" order should use the median;
# the mean is still useful for totals and forecasting revenue.
# (The few negative values are returns/refunds that Lab 14 kept in the data.)


# ===========================================================================
# Q4: Custom question  (Exercise 4)
# Business question: Which product categories "punch above their weight" —
# bringing in a bigger share of revenue than their share of orders?
# A manager would use this to decide which categories deserve more shelf space,
# marketing budget, or sales attention.
# ===========================================================================
cat = df.groupby("product_category").agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "count"),
)
cat["revenue_share"] = cat["revenue"] / cat["revenue"].sum() * 100
cat["order_share"] = cat["orders"] / cat["orders"].sum() * 100
cat = cat.sort_values("revenue_share")
print("Q4 — Share of revenue vs share of orders by category")
print(cat.round(1).to_string(), "\n")

# Chart choice: a grouped horizontal bar chart. Both measures are percentages on the
# same 0-100 scale, so they can share one axis and be compared side by side within
# each category. Horizontal bars leave room for long category names like
# "Office Supplies", and sorting by revenue share puts the biggest earners on top.
# A pie chart would make this comparison much harder to read.
fig, ax = plt.subplots(figsize=(9, 5.5))
y = range(len(cat))
h = 0.38
ax.barh([i + h / 2 for i in y], cat["revenue_share"], height=h, color=BLUE,
        label="Share of revenue")
ax.barh([i - h / 2 for i in y], cat["order_share"], height=h, color=ORANGE,
        label="Share of orders")
ax.set_yticks(list(y))
ax.set_yticklabels(cat.index)
for i, (rs, os_) in enumerate(zip(cat["revenue_share"], cat["order_share"])):
    ax.text(rs + 0.4, i + h / 2, f"{rs:.1f}%", va="center", fontsize=8)
    ax.text(os_ + 0.4, i - h / 2, f"{os_:.1f}%", va="center", fontsize=8, color=DARK_GRAY)
ax.set_title("Electronics & Furniture Earn Far More Than Their Order Count Suggests")
ax.set_xlabel("Percent of 2025 Total (%)")
ax.set_ylabel("Product Category")
ax.grid(axis="x", alpha=0.3)
ax.set_axisbelow(True)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig(CHART_DIR / "q4_custom.png")
plt.close(fig)

elec = cat.loc["Electronics"]
q4_sentence = (
    f"Electronics drove {dollars(elec['revenue'])} ({elec['revenue_share']:.1f}% of revenue) "
    f"from only {elec['order_share']:.1f}% of orders, while Paper and Office Supplies "
    f"together make up {cat.loc[['Paper', 'Office Supplies'], 'order_share'].sum():.1f}% "
    f"of orders but just {cat.loc[['Paper', 'Office Supplies'], 'revenue_share'].sum():.1f}% "
    f"of revenue."
)
print("Q4 finding:", q4_sentence, "\n")
# Q4 finding: Electronics drove $576,469 (32.3% of revenue) from only 12.3% of orders,
# while Paper and Office Supplies together make up 37.7% of orders but just 13.6%
# of revenue.

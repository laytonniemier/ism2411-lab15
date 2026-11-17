# ISM2411 Lab 15 — Aggregate & Chart — Capstone Warm-up

**Author:** Layton Niemier

Aggregates the cleaned 2025 sales data from Lab 14 (`data/clean_sales.csv`) and charts four business questions: revenue by region, the monthly revenue trend, order-size distribution, and which product categories earn more than their share of orders.

## How to run

```bash
pip install pandas matplotlib seaborn
python aggregate.py
```

The script prints the summary numbers and saves four charts to `charts/`:

| File | Question |
|---|---|
| `charts/q1_revenue_by_region.png` | Which region brings in the most revenue? |
| `charts/q2_monthly_trend.png` | How does revenue move month to month? |
| `charts/q3_order_distribution.png` | What does a typical order look like? (Seaborn) |
| `charts/q4_custom.png` | Which categories earn more than their share of orders? |

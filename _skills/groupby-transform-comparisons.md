---
name: groupby-transform-comparisons
title: Compare Each Row to Its Group with Transform
description: Attach group-level totals, averages, running balances, or ranks to every detail row using groupby().transform(), keeping full detail for review instead of collapsing to a summary.
category: summarization
tools: pandas
---

## When to use this skill

- You need each transaction compared against its own group: "what percent of this vendor's annual spend is this invoice?" or "what is the running balance for this member?"
- A regular `groupby().sum()` won't work because it collapses the detail — you need the group figure *next to* every row so a reviewer can scan line by line.
- You're replacing slow, fragile SUMIFS / cumulative SUMIFS formulas that break when rows are re-sorted.

The key distinction: `agg` gives you one row per group; `transform` gives you a value for **every original row**, aligned to the detail. Detail stays intact for tie-outs and workpapers.

## Inputs it expects

- A DataFrame at transaction/detail level — one row per payment, invoice, or journal line.
- A grouping column (`Vendor_ID`, `Member_ID`, `Account`, `Department`).
- A numeric amount column to aggregate.
- For running totals: a date or period column, and the data **sorted** by group then date before computing cumulative figures.

## Steps

1. Sort the DataFrame by group and date — cumulative sums follow row order, so this matters.
2. Use `transform('sum')` to put each group's total on every row of that group.
3. Use `transform('cumsum')` for a running balance within each group.
4. Derive comparison columns: percent of group total, difference from group average, rank within group.
5. Keep the detail rows — this enriched table *is* the deliverable, ready for filtering and reviewer sampling.

## Code

```python
import pandas as pd

# Detail-level payment data
df = pd.DataFrame({
    'Vendor_ID': ['V-1001', 'V-1001', 'V-1001', 'V-2002', 'V-2002', 'V-3003'],
    'Invoice_Date': ['2025-01-15', '2025-02-10', '2025-03-05',
                     '2025-01-20', '2025-02-25', '2025-01-30'],
    'Invoice_Amount': [12500.00, 8750.00, 15300.00, 42000.00, 38500.00, 9900.00],
})
df['Invoice_Date'] = pd.to_datetime(df['Invoice_Date'])

# Sort first — running totals follow row order
df = df.sort_values(['Vendor_ID', 'Invoice_Date']).reset_index(drop=True)

# Group total repeated on every detail row
df['Vendor_Total'] = df.groupby('Vendor_ID')['Invoice_Amount'].transform('sum')

# Running balance within each vendor
df['Running_Total'] = df.groupby('Vendor_ID')['Invoice_Amount'].transform('cumsum')

# Each invoice as a share of its vendor's total spend
df['Pct_of_Vendor_Total'] = (df['Invoice_Amount'] / df['Vendor_Total'] * 100).round(1)

# Variance from the vendor's average invoice
df['Vendor_Avg'] = df.groupby('Vendor_ID')['Invoice_Amount'].transform('mean')
df['Diff_vs_Avg'] = df['Invoice_Amount'] - df['Vendor_Avg']

# Rank invoices within each vendor (largest = 1)
df['Rank_in_Vendor'] = df.groupby('Vendor_ID')['Invoice_Amount'] \
                         .rank(method='dense', ascending=False).astype(int)

print(df)
```

## Validation (control totals)

- **Row count unchanged:** transform never adds or removes rows — `len(df)` must match the source detail exactly.
- **Grand total unchanged:** `df['Invoice_Amount'].sum()` is identical before and after — you only added columns.
- **Group totals tie to an independent aggregation:** `df.groupby('Vendor_ID')['Invoice_Amount'].sum()` must equal `df.groupby('Vendor_ID')['Vendor_Total'].first()` for every group.
- **Running total lands on the group total:** the last `Running_Total` row in each group must equal that group's `Vendor_Total`.
- **Percentages sum to 100:** `df.groupby('Vendor_ID')['Pct_of_Vendor_Total'].sum()` should be ~100 per group (allow small rounding drift).

## Exceptions to surface

- Rows where `Pct_of_Vendor_Total` is unusually high (e.g., one invoice is more than half the vendor's total) — concentration worth a look.
- Groups with only one row — group average and rank are trivially meaningless there; flag them rather than letting them blend in.
- Rows with a null or zero group total — a percent-of-total divides by zero and produces `inf`/`NaN`; the underlying amounts need review.
- Negative amounts (credits/reversals) mixed into a group — they distort running totals and percentages; confirm they belong in the same population.
- Rows whose `Diff_vs_Avg` exceeds a set threshold (e.g., 3x the group's typical invoice) — classic outlier candidates for the reviewer's sample.

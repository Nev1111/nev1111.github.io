---
name: fiscal-period-calculations
title: Fiscal Year and Quarter Calculations
description: Add fiscal year and fiscal quarter columns to dated transaction data for any non-calendar year-end (e.g., federal government October-September), so every later summary groups on the same fiscal periods.
category: summarization
tools: pandas
---

## When to use this skill

- Your organization's fiscal year does not match the calendar year — federal government (Oct 1 to Sep 30), many state and local governments (Jul 1 to Jun 30), UK/Japan (Apr 1 to Mar 31).
- You are about to summarize transactions "by quarter" or "by fiscal year" and the raw file only has a transaction date.
- You inherited a workbook full of nested IF formulas that translate months into fiscal quarters, and you want one calculation you can trust and reuse.

The core idea: compute `Fiscal_Year` and `Fiscal_Quarter` **once** as columns on the detail data. Every pivot, groupby, and report after that just uses those columns — no formula ever gets re-derived.

## Inputs it expects

- A DataFrame with one row per transaction (journal entries, payments, receipts, holdings).
- A date column (`Posting_Date` below) that pandas can parse — Excel dates, `YYYY-MM-DD` strings, etc.
- The month your fiscal year **ends** in (September for federal, June for many state/local governments). That's the only setting you need.
- An amount column if you plan to summarize (`Amount` below).

## Steps

1. Convert the date column with `pd.to_datetime` — do this first, and check for unparseable dates.
2. Pick the pandas frequency code for your year-end month: `Q-SEP` / `Y-SEP` for a September 30 year-end, `Q-JUN` / `Y-JUN` for June 30, `Q-MAR` / `Y-MAR` for March 31. (Older pandas versions spell the annual code `A-SEP`.)
3. Add `Fiscal_Year` and `Fiscal_Quarter` columns using that frequency. By convention the fiscal year is named for the year it ends in (October 2025 falls in FY2026 for a September year-end).
4. Spot-check the boundary months: the first month of the fiscal year should show Q1 of the *next* fiscal year label, and the last month should show Q4.
5. Group by the new columns for your summary.

## Code

```python
import pandas as pd

# Detail transactions with a posting date
df = pd.DataFrame({
    'Posting_Date': ['2025-10-15', '2026-01-20', '2026-04-10', '2026-07-05', '2026-09-30'],
    'Fund': ['General', 'General', 'Capital', 'General', 'Capital'],
    'Amount': [125000.00, 98000.00, 245000.00, 87500.00, 132000.00],
})

df['Posting_Date'] = pd.to_datetime(df['Posting_Date'])

# Federal fiscal year: October 1 - September 30 (year-end month = SEP)
# For a June 30 year-end use 'Q-JUN' / 'Y-JUN'; March 31 use 'Q-MAR' / 'Y-MAR'.
df['Fiscal_Year'] = df['Posting_Date'].dt.to_period('Y-SEP').dt.year
df['Fiscal_Quarter'] = pd.PeriodIndex(df['Posting_Date'], freq='Q-SEP').strftime('Q%q')

print(df)
# October 2025 -> FY2026 Q1; September 2026 -> FY2026 Q4

# Reuse the columns in any summary
quarterly_summary = (
    df.groupby(['Fiscal_Year', 'Fiscal_Quarter'])['Amount']
      .agg(Total='sum', Count='count', Average='mean')
)
print(quarterly_summary)
```

## Validation (control totals)

- **Row count unchanged:** adding the two columns must not add or drop rows — `len(df)` before equals `len(df)` after.
- **Grand total unchanged:** `df['Amount'].sum()` on the detail must equal `quarterly_summary['Total'].sum()` to the penny. Every row lands in exactly one fiscal quarter, so the summary must tie out.
- **No unassigned periods:** `df['Fiscal_Year'].isna().sum()` and `df['Fiscal_Quarter'].isna().sum()` should both be 0. A blank fiscal period means a date failed to parse.
- **Boundary check:** filter one transaction from the first month of the fiscal year (e.g., October for a September year-end) and confirm it shows Q1 of the correct fiscal year.

## Exceptions to surface

- Rows where `pd.to_datetime(..., errors='coerce')` produced `NaT` — the original date text was unparseable and a human must decide the real date.
- Transactions dated outside the expected fiscal range (e.g., a "FY2026" file containing dates from FY2024) — likely prior-period adjustments or data entry errors.
- Dates exactly on the fiscal year boundary (Sep 30 vs. Oct 1) when the source system's cutoff practices are unclear — confirm which fiscal year the accounting records assign them to.
- Any row where the fiscal year derived from the date disagrees with a fiscal-year field already present in the source file.

---
name: reshape-melt-pivot
title: Reshape Between Report Layouts and Analysis Layouts
description: Convert wide report-style data (one column per month/period) into tall analysis-ready rows with melt, and back into readable crosstabs with pivot_table, without losing or double-counting amounts.
category: summarization
tools: pandas
---

## When to use this skill

- The source file is a report layout: one row per account or member, with a column for each month (`Jan`, `Feb`, ... `Dec`) — and you need to filter by period, compute month-over-month change, or join to other monthly data.
- The opposite direction: you have tidy transaction rows (`Account`, `Month`, `Amount`) and the reviewer wants a crosstab with months across the top.
- You'd otherwise be copy-pasting columns into rows by hand in Excel.

Rule of thumb: **store and analyze in tall (long) format, present in wide format.** `melt()` goes wide-to-tall; `pivot_table()` goes tall-to-wide.

## Inputs it expects

- **For melt:** a wide DataFrame with identifier columns (`Account_ID`, `Account_Name`) plus one value column per period. Know which columns are identifiers and which are periods.
- **For pivot:** a tall DataFrame with an identifier column, a period column, and an amount column. Know whether (identifier, period) pairs can repeat — if they can, you must use `pivot_table` with an `aggfunc`, not plain `pivot`.

## Steps

1. List the identifier columns and the period columns explicitly — don't rely on "everything else."
2. **Wide to tall:** `melt()` with `id_vars` for identifiers, `var_name='Month'`, `value_name='Amount'`.
3. Fix month ordering — melted month names sort alphabetically (Apr, Aug, Dec...). Use an ordered `Categorical` or convert to real dates.
4. **Tall to wide:** `pivot_table()` with `aggfunc='sum'` and `fill_value=0`, plus `margins=True` if you want row/column totals for tie-out.
5. Run the control totals below before using the reshaped data.

## Code

```python
import pandas as pd

# Wide report layout: one column per month
gl_wide = pd.DataFrame({
    'Account_ID': ['4000', '5100', '5200'],
    'Account_Name': ['Contributions', 'Benefit_Payments', 'Admin_Expense'],
    'Jan': [520000.00, 310000.00, 45000.00],
    'Feb': [498000.00, 312500.00, 47200.00],
    'Mar': [545000.00, 315000.00, 44100.00],
})

month_cols = ['Jan', 'Feb', 'Mar']

# --- Wide -> Tall (melt) ---
gl_tall = gl_wide.melt(
    id_vars=['Account_ID', 'Account_Name'],
    value_vars=month_cols,
    var_name='Month',
    value_name='Amount',
)

# Months sort alphabetically unless you tell pandas the real order
gl_tall['Month'] = pd.Categorical(gl_tall['Month'], categories=month_cols, ordered=True)
gl_tall = gl_tall.sort_values(['Account_ID', 'Month']).reset_index(drop=True)

# Now analysis is easy: totals by month, month-over-month change, filtering
monthly_totals = gl_tall.groupby('Month', observed=True)['Amount'].sum()
print(monthly_totals)

# --- Tall -> Wide (pivot_table) ---
# Use pivot_table, not pivot: it tolerates duplicate (account, month) pairs
# by aggregating them instead of raising an error.
gl_crosstab = gl_tall.pivot_table(
    index=['Account_ID', 'Account_Name'],
    columns='Month',
    values='Amount',
    aggfunc='sum',
    fill_value=0,
    observed=True,
)
print(gl_crosstab)
```

## Validation (control totals)

- **Grand total is preserved both directions:** `gl_wide[month_cols].sum().sum()` must equal `gl_tall['Amount'].sum()` and must equal `gl_crosstab.to_numpy().sum()`. Reshaping moves numbers; it must never change them.
- **Row count arithmetic:** after melt, `len(gl_tall)` must equal `len(gl_wide) * len(month_cols)` exactly. More rows means duplicated identifiers; fewer means dropped periods.
- **Per-account totals tie:** row totals of the crosstab (`gl_crosstab.sum(axis=1)`) must match each account's melted total (`gl_tall.groupby('Account_ID', observed=True)['Amount'].sum()`).
- **Round-trip check:** pivoting the melted data back should reproduce the original wide figures cell for cell.

## Exceptions to surface

- Duplicate (identifier, period) pairs found before pivoting — `pivot_table` will silently sum them; a reviewer must confirm whether they are legitimate multiple postings or double-loaded data.
- Cells that were blank in the wide source — after melt these become `NaN` rows. Decide with the reviewer whether blank means zero or missing before filling with 0.
- Identifier rows in the wide file with no amounts in any period (all-zero or all-blank) — possibly closed accounts that shouldn't be in the population.
- (identifier, period) combinations that exist in one direction of the reshape but not the other — check the round-trip diff.
- Period column names that didn't match the expected list (a stray `Total` or `YTD` column melted in as if it were a month will double-count the grand total).

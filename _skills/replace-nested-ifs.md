---
name: replace-nested-ifs
title: Replace Nested IF Formulas with Classification Rules
description: Convert deep nested Excel IF formulas into readable Python classification logic — a dictionary lookup for simple mappings, np.select for multi-condition rules — with an "Unknown" bucket that ties out.
category: reconciliation
tools: pandas
---

## When to use this skill

- Your workbook has a formula like `=IF(A2=11,"Fund_A",IF(A2=12,"Fund_B",IF(A2=13,...` and nobody dares touch it.
- Adding one new fund or department code means editing the same fragile formula in a dozen workbooks — and Excel caps you at 64 nested IFs anyway.
- You need classification rules that combine conditions (account range AND fund code AND amount threshold), which nested IFs make unreadable.

Two clean replacements: a **dictionary lookup** when it's a straight code-to-name mapping (this is a VLOOKUP table living in code, or loaded from a small Excel file), and **np.select** when rules involve ranges and multiple conditions. Both send anything unrecognized to an explicit "Unknown" bucket instead of a silent blank.

## Inputs it expects

- **Data file**: transactions with the driver columns for classification (e.g., `Fund_Code`, `Account_num`, `Amount`).
- **The business rules**: the nested IF translated into plain English — get the person who owns the formula to confirm each branch, including what happens when nothing matches.
- Optionally, a **mapping file** (`fund_mappings.xlsx` with `Fund_Code`, `Fund_Name`) so non-programmers can maintain the code list without touching Python.

## Steps

1. Write out the nested IF branch by branch as a plain list of rules. This is the moment hidden gaps get found — do it with the formula's owner.
2. For simple code-to-name mappings: build a dictionary (or load it from Excel with `dict(zip(...))`) and apply it with `.map()`, defaulting misses to `'Unknown'`.
3. For multi-condition rules: express each rule as a boolean condition and use `np.select(conditions, choices, default='Unknown')`. Order matters — the first matching condition wins, just like nested IFs.
4. Record the input row count and total amount.
5. Classify, then count how many rows fell into each category, including `Unknown`.
6. Spot-check against the old spreadsheet: run both on the same data once and diff the category columns before retiring the formula.
7. Export the `Unknown` rows as the exception list.

## Code

```python
import pandas as pd
import numpy as np

df = pd.read_excel('gl_detail.xlsx')   # Account_num, Fund_Code, Amount
rows_in = len(df)
amount_in = df['Amount'].sum()

# --- Simple mapping: replaces =IF(A2=11,"Fund_A",IF(A2=12,... ---
# Maintainable in Excel: fund_mappings.xlsx with Fund_Code / Fund_Name columns
fund_map = pd.read_excel('fund_mappings.xlsx')
fund_dict = dict(zip(fund_map['Fund_Code'], fund_map['Fund_Name']))

df['Fund_Name'] = df['Fund_Code'].map(fund_dict).fillna('Unknown')

# --- Multi-condition rules: replaces the unreadable mega-IF ---
acct = df['Account_num'].astype(str).str[:4].astype(int)   # first 4 digits drive the rules

conditions = [
    (acct.between(1000, 1999)) & (df['Amount'] > 10_000),   # first match wins, like nested IFs
    (acct.between(1000, 1999)),
    (acct.between(2000, 2999)) & (df['Fund_Code'].isin([11, 12, 13])),
    (acct.between(2000, 2999)),
    (acct.between(3000, 3999)),
    (acct.between(4000, 4999)),
]
choices = [
    'Major Revenue',
    'Minor Revenue',
    'Operating Expense',
    'Capital Expense',
    'Asset',
    'Liability',
]
df['Category'] = np.select(conditions, choices, default='Unknown')

# Control totals and exceptions
summary = df.groupby('Category')['Amount'].agg(Rows='count', Total='sum')
print(summary)
print(f"\nRows in: {rows_in:,} | Rows classified: {summary['Rows'].sum():,}")
print(f"Amount in: {amount_in:,.2f} | Amount out: {summary['Total'].sum():,.2f}")

df[(df['Category'] == 'Unknown') | (df['Fund_Name'] == 'Unknown')] \
    .to_excel('EXCEPTIONS_unclassified.xlsx', index=False)
df.to_excel('gl_detail_classified.xlsx', index=False)
```

## Validation (control totals)

- **Rows in vs. rows out**: classification adds columns, never rows — `summary['Rows'].sum() == rows_in`, always.
- **Classified + Unknown = total**: every row lands in exactly one bucket. Report rows per category including the `Unknown` count; a sudden jump in `Unknown` means new codes appeared upstream.
- **Amount tie-out**: `summary['Total'].sum() == amount_in` to the penny — the category subtotals plus the `Unknown` bucket must rebuild the original grand total.
- **Parallel run**: for one period, compare Python categories to the legacy formula's output row by row (`df['Category'] != df['Excel_Category']`). Zero differences (or explained ones) before the formula is retired.

## Exceptions to surface

- Every row in `EXCEPTIONS_unclassified.xlsx` — codes or account ranges no rule covers. These are new funds/accounts needing a rule, or data-entry errors. Never let them ride as blanks.
- Rows where the parallel run disagrees with the old Excel formula — each difference is either a bug in the new rules or a bug that's been living in the spreadsheet for years. Both are worth knowing.
- Rows that matched an earlier condition when a later, more specific one also applied — if two rules overlap, confirm the ordering reflects the intended business priority.
- Fund codes present in `fund_mappings.xlsx` but never seen in the data (stale mappings), and any duplicate `Fund_Code` entries in the mapping file — the dictionary silently keeps the last one, so a reviewer should resolve duplicates in the source file.

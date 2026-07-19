---
name: safe-excel-sql-merges
title: Merge Excel Lists with SQL Extracts Without Losing Rows
description: Join a spreadsheet list against a database extract safely — parameterized queries, indicator and validate flags, and pre/post row counts so nothing drops silently.
category: reconciliation
tools: pandas
---

## When to use this skill

- You have a list in Excel (account numbers, vendor IDs, employee IDs) and need to enrich it with fields pulled from a SQL database.
- You've been burned by a VLOOKUP or merge that silently dropped rows, silently duplicated rows, or matched nothing because one side stored the key as text and the other as a number.
- Someone on the team is building SQL strings by pasting IDs into the query text. Stop them — that's an injection risk and a formatting time bomb.

The pattern: pull from the database with a *parameterized* query, then merge with `how='left'`, `indicator=True`, and `validate=` so every row is accounted for and any fan-out is caught immediately.

## Inputs it expects

- **Excel list**: one row per item you care about, with a clean key column (e.g., `account_id`).
- **Database connection**: pyodbc/SQLAlchemy connection string to the source system.
- **Expected relationship**: know before you merge whether the database should return one row per key (`one_to_one`) or many (`one_to_many`). This becomes the `validate=` argument.
- Keys on both sides in the **same dtype** — cast both to string (and strip whitespace/leading zeros consistently) before merging.

## Steps

1. Load the Excel list and record its row count. This is your control total — the output must have at least this many rows, and exactly this many if the relationship is one-to-one.
2. Build a parameterized `IN (...)` query with `?` placeholders — never f-string the values into the SQL text. For 1,000+ keys, query in batches.
3. Pull the extract and record its row count too.
4. Normalize the key columns on both sides (dtype, strip, case).
5. Merge with `how='left'` (keep every Excel row), `indicator=True` (label each row's match status), and `validate=` (blow up loudly if the shape isn't what you expected).
6. Tabulate `_merge`: matched + unmatched must equal the Excel total. Export the `left_only` rows as the exception list.

## Code

```python
import pandas as pd
import pyodbc

# 1. Load the Excel list — this row count is the control total
excel_df = pd.read_excel('accounts.xlsx')          # account_id, account_desc, gl_balance
rows_in = len(excel_df)
excel_df['account_id'] = excel_df['account_id'].astype(str).str.strip()
account_list = excel_df['account_id'].unique().tolist()

# 2. Parameterized query — placeholders, never string-pasted values
conn = pyodbc.connect('Driver={SQL Server};Server=MyServer;Database=MyDB;Trusted_Connection=yes;')

def query_in_batches(conn, values, batch_size=1000):
    """IN-list queries in safe batches (SQL Server caps parameters)."""
    frames = []
    for i in range(0, len(values), batch_size):
        batch = values[i:i + batch_size]
        placeholders = ','.join(['?'] * len(batch))
        sql = f"""
            SELECT Account_ID AS account_id, Account_Name, Current_Balance
            FROM Accounts
            WHERE Account_ID IN ({placeholders})
        """
        frames.append(pd.read_sql_query(sql, conn, params=batch))
    return pd.concat(frames, ignore_index=True)

db_df = query_in_batches(conn, account_list)
db_df['account_id'] = db_df['account_id'].astype(str).str.strip()
print(f"Excel rows: {rows_in:,}  |  DB rows returned: {len(db_df):,}")

# 3. Safe merge: keep every Excel row, label match status, enforce shape
merged = pd.merge(
    excel_df,
    db_df,
    on='account_id',
    how='left',
    indicator=True,
    validate='one_to_one'   # use 'one_to_many' only if fan-out is genuinely expected
)

# 4. Account for every row
counts = merged['_merge'].value_counts()
matched = counts.get('both', 0)
unmatched = counts.get('left_only', 0)
print(f"Matched: {matched:,}  |  Unmatched: {unmatched:,}  |  Total: {len(merged):,}")

assert matched + unmatched == rows_in, "Rows gained or lost in merge — investigate before using output!"

merged[merged['_merge'] == 'left_only'].drop(columns='_merge') \
    .to_excel('EXCEPTIONS_not_in_database.xlsx', index=False)
merged.drop(columns='_merge').to_excel('accounts_with_data.xlsx', index=False)
```

## Validation (control totals)

- **Rows in vs. rows out**: with `how='left'` and `validate='one_to_one'`, `len(merged)` must equal `rows_in` exactly. If you allowed `one_to_many`, rows out will exceed rows in — reconcile the difference to the expected fan-out, don't shrug at it.
- **Matched + unmatched = total**: `counts['both'] + counts['left_only'] == rows_in`. Put all three numbers in the workpaper.
- **Amount tie-out**: `excel_df['gl_balance'].sum()` must equal `merged['gl_balance'].sum()` — a left merge never changes left-side totals; if it did, rows duplicated.
- **validate= as tripwire**: if `pd.merge` raises `MergeError`, the database has duplicate keys. That's a finding, not a nuisance — do not "fix" it by dropping duplicates without understanding why they exist.

## Exceptions to surface

- Every row in `EXCEPTIONS_not_in_database.xlsx` (`_merge == 'left_only'`): accounts on the Excel list the database doesn't know about — typos, closed accounts, wrong system, or something worse.
- Duplicate keys in the database extract (caught by `validate=` or `db_df['account_id'].duplicated()`): a reviewer must decide which record is authoritative.
- Keys that only matched after normalization (dtype/whitespace/leading-zero fixes): note them so the source-system formatting issue gets fixed upstream.
- DB rows returned that exceed the distinct keys requested — a sign the key isn't unique in the source table.

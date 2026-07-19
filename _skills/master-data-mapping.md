---
name: master-data-mapping
title: Apply Master Classifications from a Mapping Table
description: Classify transactions (accounts, departments, report lines) from a single master mapping table, with duplicate/inconsistency checks and an unmatched-exception list.
category: reconciliation
tools: pandas
---

## When to use this skill

- You need to tag a trial balance or transaction file with categories — expense type, department, financial-statement line — from a lookup table.
- The same account keeps getting classified three different ways across months, and year-over-year analysis has stopped making sense.
- The current "process" is a VLOOKUP against whichever `Classification_FINAL_FINAL.xlsx` happens to be newest on the shared drive.

The fix: one master mapping file, validated before use (no duplicate keys, no conflicting categories), merged with `indicator=True` so every unmapped account lands on an exception list instead of silently becoming blank.

## Inputs it expects

- **Transaction file**: e.g., a trial balance with `Account_num`, `Account_desc`, `Amount`.
- **Master mapping table**: one Excel sheet, one row per account, with `Account_num`, `Category`, `Subcategory`, `Report_Line`, and a `Year_created` (or effective-date) column for the audit trail.
- Keys in the **same format** on both sides — account numbers as strings, consistently padded, no stray spaces.
- An agreed rule for conflicts: usually "most recent classification wins."

## Steps

1. Load the mapping library and check it for trouble *before* using it: accounts appearing more than once, and accounts whose category differs between rows.
2. Export any inconsistencies for team review — those are governance findings, not code problems.
3. Deduplicate to one row per account (keep the most recent by `Year_created`).
4. Record the transaction row count and total amount — your control totals.
5. Left-merge transactions against the clean library with `indicator=True` and `validate='many_to_one'`.
6. Split matched vs. unmatched. Summarize unmatched accounts by transaction count and total dollars (biggest dollars first) and export for classification.
7. Tie out totals, then publish the classified file.

## Code

```python
import pandas as pd

# 1. Load transactions and the master mapping library
txns = pd.read_excel('trial_balance_december.xlsx')          # Account_num, Account_desc, Amount
library = pd.read_excel('Master_Classifications.xlsx',
                        sheet_name='Mappings', keep_default_na=False)

for df in (txns, library):
    df['Account_num'] = df['Account_num'].astype(str).str.strip()

rows_in = len(txns)
amount_in = txns['Amount'].sum()

# 2. Validate the library: same account, different categories?
cat_counts = library.groupby('Account_num')['Category'].nunique()
inconsistent = cat_counts[cat_counts > 1]
if len(inconsistent) > 0:
    library[library['Account_num'].isin(inconsistent.index)] \
        .sort_values(['Account_num', 'Year_created']) \
        .to_excel('REVIEW_inconsistent_classifications.xlsx', index=False)
    print(f"WARNING: {len(inconsistent)} accounts have conflicting classifications — exported for review")

# 3. Deduplicate: most recent classification wins
library_clean = library.sort_values(['Account_num', 'Year_created']) \
                       .drop_duplicates(subset='Account_num', keep='last')

# 4. Merge — keep every transaction, label match status, forbid fan-out
classified = pd.merge(
    txns,
    library_clean[['Account_num', 'Category', 'Subcategory', 'Report_Line']],
    on='Account_num',
    how='left',
    indicator=True,
    validate='many_to_one'
)

matched = (classified['_merge'] == 'both').sum()
unmatched = (classified['_merge'] == 'left_only').sum()
print(f"Transactions: {rows_in:,} | Mapped: {matched:,} "
      f"({matched / rows_in:.1%}) | Unmapped: {unmatched:,}")

# 5. Exception list: unmapped accounts, largest dollars first
if unmatched > 0:
    (classified[classified['_merge'] == 'left_only']
        .groupby(['Account_num', 'Account_desc'])['Amount']
        .agg(Transaction_count='count', Total_amount='sum')
        .reset_index()
        .sort_values('Total_amount', key=abs, ascending=False)
        .to_excel('EXCEPTIONS_unmapped_accounts.xlsx', index=False))

classified.drop(columns='_merge').to_excel('trial_balance_CLASSIFIED.xlsx', index=False)
```

## Validation (control totals)

- **Rows in vs. rows out**: `len(classified) == rows_in`. With `validate='many_to_one'` and a deduplicated library this cannot drift — if it does, the library still has duplicate keys.
- **Matched + unmatched = total**: `matched + unmatched == rows_in`. Report the coverage percentage each period; it should trend toward 100%.
- **Amount tie-out**: `classified['Amount'].sum() == amount_in` to the penny, and mapped amount + unmapped amount = total amount. Also tie `classified.groupby('Category')['Amount'].sum()` plus the unmapped bucket back to the original total.
- **Library sanity**: after dedup, `library_clean['Account_num'].is_unique` must be `True`.

## Exceptions to surface

- Every account in `EXCEPTIONS_unmapped_accounts.xlsx` — new or mistyped accounts with no classification. Review largest absolute dollars first; a $2M unmapped account matters more than fifty $10 ones.
- Every account in `REVIEW_inconsistent_classifications.xlsx` — the same account classified differently across years. A human must confirm whether it was an intentional reclassification (document it) or a typo/judgment drift (correct the library).
- Mappings never used by any transaction (`right_only` if you re-run with `how='outer'`, or an anti-join): stale library entries worth pruning.
- Near-duplicate category names in the library (`"Personnel"` vs `"Personel"`) — check `library['Category'].unique()` and reconcile spellings before they split your subtotals.

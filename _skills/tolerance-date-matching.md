---
name: tolerance-date-matching
title: Match Records on Nearby Dates with a Tolerance
description: Match two lists on the closest date (not an exact date) using pd.merge_asof with a documented tolerance — for deposits, settlements, and timing differences.
category: reconciliation
tools: pandas
---

## When to use this skill

- You're reconciling two lists where the dates *should* line up but rarely do exactly: bank deposits vs. cash receipts, trade date vs. settlement date, invoice date vs. payment posting date.
- An exact-date VLOOKUP or merge leaves you with a pile of "unmatched" items that a human can see are obviously the same transaction, just a day or three apart.
- You need to pull the record "in effect as of" a cutoff date — the latest rate, address, or price on or before a given date.

The tool is `pd.merge_asof`: for each row on the left, it grabs the closest row on the right (within a key like account ID), looking backward, forward, or nearest — and you can cap how far it's allowed to look with a `tolerance`. Document that tolerance; it's a judgment call an auditor will ask about.

## Inputs it expects

- **Left table**: the records you're trying to match (e.g., GL cash receipts) with a datetime column and a key column (account or entity ID).
- **Right table**: the candidate matches (e.g., bank deposits) with its own datetime column and the same key.
- **A matching direction**: `backward` (closest on-or-before), `forward` (closest on-or-after), or `nearest`.
- **A tolerance**: the maximum allowable date gap, e.g. `pd.Timedelta(days=3)`. Agree on this up front — it is your matching policy.
- Both tables must be **sorted by the date column** before the merge (merge_asof requires it).

## Steps

1. Load both files and convert the date columns with `pd.to_datetime` — merge_asof will not work on text dates.
2. Sort both DataFrames by their date column (ascending). Sorting by the key isn't required, but the dates must be in order.
3. Record the starting row counts of both tables — you'll tie back to these.
4. Run `pd.merge_asof` with `by=` your key column, `left_on=`/`right_on=` the date columns, your chosen `direction`, and the agreed `tolerance`.
5. Rows that found no partner within the tolerance come back with NaN in the right-side columns — split those into an exceptions file.
6. Tie out control totals (below), then hand the exceptions to a reviewer.

## Code

```python
import pandas as pd

# Left: GL cash receipts. Right: bank deposits.
gl = pd.read_excel('gl_cash_receipts.xlsx')        # account_id, receipt_date, gl_amount
bank = pd.read_excel('bank_deposits.xlsx')         # account_id, deposit_date, bank_amount

gl['receipt_date'] = pd.to_datetime(gl['receipt_date'])
bank['deposit_date'] = pd.to_datetime(bank['deposit_date'])

# merge_asof requires both sides sorted by the date column
gl = gl.sort_values('receipt_date')
bank = bank.sort_values('deposit_date')

rows_in = len(gl)

# Documented matching policy: nearest deposit within 3 calendar days, same account
matched = pd.merge_asof(
    gl,
    bank,
    left_on='receipt_date',
    right_on='deposit_date',
    by='account_id',
    direction='nearest',            # or 'backward' / 'forward'
    tolerance=pd.Timedelta(days=3)  # the tolerance — agree on this and write it down
)

# Split matched vs. unmatched (no deposit found within tolerance -> NaN)
unmatched = matched[matched['deposit_date'].isna()]
found = matched[matched['deposit_date'].notna()]

print(f"GL receipts in:        {rows_in:,}")
print(f"Matched to a deposit:  {len(found):,}")
print(f"No match within 3 days:{len(unmatched):,}")

# Flag matches where the amounts still differ — closest date is not proof of same item
found = found.assign(amount_diff=(found['gl_amount'] - found['bank_amount']).round(2))
amount_exceptions = found[found['amount_diff'] != 0]

unmatched.to_excel('EXCEPTIONS_no_date_match.xlsx', index=False)
amount_exceptions.to_excel('EXCEPTIONS_amount_differences.xlsx', index=False)
```

## Validation (control totals)

- **Row counts**: rows out of `merge_asof` must equal rows in on the left (`len(matched) == rows_in`). merge_asof never duplicates or drops left rows — if the count moved, something upstream changed.
- **Matched + unmatched = total**: `len(found) + len(unmatched) == rows_in`. State all three numbers in your workpaper.
- **Amount tie-out**: `gl['gl_amount'].sum()` must equal `found['gl_amount'].sum() + unmatched['gl_amount'].sum()` to the penny.
- **Tolerance check**: `(found['receipt_date'] - found['deposit_date']).abs().max()` must not exceed your documented tolerance.

## Exceptions to surface

- Every row in `EXCEPTIONS_no_date_match.xlsx` — no candidate existed within the tolerance window for that account. These are potential deposits in transit, missing postings, or wrong-account items.
- Rows in `EXCEPTIONS_amount_differences.xlsx` — a date-close match was found, but the amounts differ. Nearest-date is a heuristic, not evidence; a human decides if it's the same transaction with a fee/FX difference or a false match.
- Any right-side (bank) rows that were never used as a match — build this by anti-joining `bank` against `found`; unused deposits are just as interesting as unmatched receipts.
- Cases where one bank deposit matched multiple GL rows (check with `found['deposit_date'].groupby(found['account_id']).count()` or a duplicated-key check) — merge_asof allows many-to-one, and a reviewer must confirm that's the real-world relationship.

---
name: parse-legacy-reports
title: Parse Legacy Text-Dump Reports
description: Extract a clean transaction table from unstructured legacy report text files where account headers, detail lines, repeated page headers, and subtotals are interleaved.
category: cleaning
tools: pandas
---

## When to use this skill

Use this when a legacy accounting system exports a "report" that is really a formatted text dump, not a table. You'll see:

- Account header lines (`0123456-10-001234  Cash Operating Fund`) followed by indented detail lines that **don't repeat the account number**
- Repeated page headers, column headings, and blank lines scattered through the file
- Subtotal and total lines mixed in with real transactions
- Everything landing in **one column** when you open it in Excel, and Text-to-Columns breaking on inconsistent spacing

The pattern: extract structured fields with regex, **forward-fill** header values down to the detail rows that belong to them, then filter to keep only real transaction rows. Typical sources: trial balance dumps, GL detail reports, AS400/mainframe spool files.

## Inputs it expects

- A plain text file (`.txt`, `.prn`, or similar) where each line is one report row
- A recognizable pattern for the account/header identifier (e.g., `1234567-12-123456`) — grab one example line and write its regex
- A recognizable pattern for detail rows (usually a date like `MM/DD/YYYY` or an amount)
- The report's printed grand total, if it has one, for tie-out

## Steps

1. **Read every line into one column** with `pd.read_table(..., header=None)` — resist the urge to split on whitespace up front.
2. **Extract header fields** (account number + description) with `.str.extract()` — only header lines will match; everything else gets NaN.
3. **Extract detail fields** (date, amount) with their own patterns — only transaction lines will match.
4. **Forward-fill** the header columns with `.ffill()` so every detail row inherits the account it sits under.
5. **Filter to detail rows only**: keep rows where the date (or amount) extraction succeeded. This automatically discards page headers, blank lines, and column-heading rows.
6. **Exclude subtotal/total lines** explicitly — they often contain amounts and can sneak past the filter.
7. **Tie out**: transaction count and amount total against the report footer.

## Code

```python
import pandas as pd

# Step 1: read the raw dump -- one line per row, one column
raw = pd.read_table('trial_balance.txt', header=None, names=['line'])
raw['line'] = raw['line'].fillna(' ')
lines_in = len(raw)

# Step 2: extract account header fields (only header lines match)
# Pattern for accounts like 0123456-10-001234
raw[['account_num', 'account_desc']] = raw['line'].str.extract(
    r'(\d{7}-\d{2}-\d{6})\s+(.*)'
)

# Step 3: extract detail fields (only transaction lines match)
raw['txn_date'] = raw['line'].str.extract(r'(\d{2}/\d{2}/\d{4})')
raw['amount_text'] = raw['line'].str.extract(r'([\d,]+\.\d{2}(?:\s*CR)?)\s*$')

# Step 4: forward-fill headers down onto their detail rows
raw['account_num'] = raw['account_num'].ffill()
raw['account_desc'] = raw['account_desc'].ffill()

# Step 5: keep only real transaction rows (a date marks a detail line)
txns = raw[raw['txn_date'].notna()].copy()

# Step 6: drop subtotal/total lines that carry a date or amount
is_total_line = txns['line'].str.contains(r'\b(SUB)?TOTAL\b', case=False, regex=True)
subtotals = txns[is_total_line]
txns = txns[~is_total_line]

# Convert amounts (see clean-credit-debit-amounts skill for full notation handling)
amt = txns['amount_text'].str.strip()
mask_cr = amt.str.upper().str.endswith('CR')
amt.loc[mask_cr] = '-' + amt.loc[mask_cr].str[:-2].str.strip()
txns['amount'] = pd.to_numeric(amt.str.replace(',', ''), errors='coerce')

txns = txns[['account_num', 'account_desc', 'txn_date', 'amount']]

# Control totals
print(f"Lines read: {lines_in}")
print(f"Transactions extracted: {len(txns)}")
print(f"Accounts found: {txns['account_num'].nunique()}")
print(f"Amount total: {txns['amount'].sum():,.2f}")
print(f"Subtotal lines excluded: {len(subtotals)}")

txns.to_excel('trial_balance_clean.xlsx', index=False)
```

## Validation (control totals)

- **Line accounting.** Lines in = transactions kept + header lines + subtotal lines + blank/page-furniture lines. Categorize every line; a residual bucket of "unexplained" lines means your patterns are missing something.
- **Tie the amount total to the report's printed grand total.** The whole point of the exercise — `txns['amount'].sum()` must equal the footer total on the source report to the penny.
- **Tie account subtotals.** Spot-check: `txns.groupby('account_num')['amount'].sum()` for two or three accounts against the subtotal lines you excluded. If they match, your forward-fill assigned rows to the right accounts.
- **Account count sanity.** `txns['account_num'].nunique()` should equal the number of header lines matched — no account should appear in the output that never appeared as a header.
- **No unconverted amounts.** Count NaNs in the amount column after conversion; should be zero or fully explained.

## Exceptions to surface

Hand these lines to a reviewer:

- **Unclassified lines** — anything that isn't a header, detail, subtotal, or known page furniture. These are either a format variant your regex missed or real transactions being silently dropped.
- **Detail rows appearing before the first header** — forward-fill has nothing to fill from; these rows would carry NaN account numbers and must be resolved manually.
- **Subtotal mismatches** — any account where the sum of extracted detail rows doesn't equal the report's printed subtotal for that account (indicates dropped or double-captured lines).
- **Amounts that failed numeric conversion** — usually an unusual notation (see the clean-credit-debit-amounts skill) or a description accidentally captured as an amount.
- **Wrapped description lines** — long account descriptions that spill onto a second line can be misread as detail rows; flag short lines with no date and no amount that sit between a header and its details.

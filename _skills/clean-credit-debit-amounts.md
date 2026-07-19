---
name: clean-credit-debit-amounts
title: Clean Credit/Debit Amount Notation
description: Convert legacy accounting amount text like "1,234.56 CR", "1,234-", or "(1,234.56)" into proper signed numeric values for summing and analysis.
category: cleaning
tools: pandas
---

## When to use this skill

Use this when an amount column arrives as text instead of numbers because the source system marks credits with notation rather than a real minus sign. You'll recognize it immediately:

- **"CR" suffix**: `1,234.56 CR` (credit, should be negative)
- **Trailing minus**: `5,009-` (common in old mainframe/AS400 exports)
- **Parentheses**: `(1,234.56)` (classic accounting display format)
- **Thousands commas**: `15,234.00` (blocks numeric conversion even when the sign is fine)

If you can't sum the column, or Excel/pandas treats the amounts as text, this is your skill. Typical sources: trial balance exports, GL detail dumps, AP/AR aging reports from legacy systems.

## Inputs it expects

- A pandas DataFrame with one or more amount columns stored as **strings** (dtype `object`)
- Amounts may mix notations within the same column (some CR, some plain, some parenthesized)
- A known-good control total, if the source report prints one (e.g., the report footer total) — you'll tie to it at the end

## Steps

1. **Snapshot before you touch anything**: record the row count and, if possible, a hash-total of the raw text column (or the report's printed total).
2. **Strip whitespace** from every value — trailing spaces hide "CR" suffixes from your checks.
3. **Handle each negative notation** with a boolean mask: CR suffix, trailing minus, parentheses. For each, prepend `-` and remove the notation characters.
4. **Remove thousands commas** and convert to float.
5. **Coerce leftovers**: anything that still won't convert becomes NaN via `pd.to_numeric(errors='coerce')` — these are your exceptions, not silent failures.
6. **Tie out**: sum the converted column and compare to the report's control total.

## Code

```python
import pandas as pd
import numpy as np

def clean_accounting_amounts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Convert legacy credit/debit notation to signed floats.

    Handles: '1,234.56 CR', '5,009-', '(1,234.56)', '1,234.56'
    """
    df = df.copy()
    raw = df[column].astype(str).str.strip()

    # Notation 1: 'CR' suffix (case-insensitive) -> negative
    mask_cr = raw.str.upper().str.endswith('CR')
    raw.loc[mask_cr] = '-' + raw.loc[mask_cr].str[:-2].str.strip()

    # Notation 2: trailing minus '5,009-' -> negative
    mask_minus = raw.str.endswith('-') & ~raw.str.startswith('-')
    raw.loc[mask_minus] = '-' + raw.loc[mask_minus].str[:-1]

    # Notation 3: parentheses '(1,234.56)' -> negative
    mask_paren = raw.str.startswith('(') & raw.str.endswith(')')
    raw.loc[mask_paren] = '-' + raw.loc[mask_paren].str[1:-1]

    # Strip commas, convert; anything unconvertible becomes NaN
    raw = raw.str.replace(',', '', regex=False).str.strip()
    df[column + '_clean'] = pd.to_numeric(raw, errors='coerce')

    return df

# --- Usage on a trial balance export ---
tb = pd.read_excel('trial_balance.xlsx', dtype={'beg_balance': str})
rows_in = len(tb)

tb = clean_accounting_amounts(tb, 'beg_balance')

# Control totals
failed = tb[tb['beg_balance_clean'].isna() & tb['beg_balance'].notna()]
print(f"Rows in: {rows_in} | Rows out: {len(tb)}")
print(f"Converted total: {tb['beg_balance_clean'].sum():,.2f}")
print(f"Rows failing conversion: {len(failed)}")
if len(failed) > 0:
    print(failed[['beg_balance']])
```

## Validation (control totals)

- **Row count in = row count out.** This transformation never adds or drops rows — if counts differ, stop.
- **Tie the converted sum to the source report's printed total.** The trial balance footer, GL control total, or batch total should match `df['beg_balance_clean'].sum()` to the penny. Any difference means a notation you didn't handle or a sign flipped the wrong way.
- **Count of negatives should equal count of CR/minus/paren rows.** Compare `(df['beg_balance_clean'] < 0).sum()` against `mask_cr.sum() + mask_minus.sum() + mask_paren.sum()` — a mismatch means a value was already negative or a mask double-fired.
- **No silent NaNs.** `pd.to_numeric(errors='coerce')` converts failures to NaN instead of crashing — count them and confirm the count is zero (or fully explained).

## Exceptions to surface

Route these rows to a human reviewer rather than guessing:

- **Rows that failed conversion** (NaN after coerce) — often "DR" suffixes, "N/A", dashes-as-zero, or stray footer text captured as data
- **Values matching more than one notation** — e.g., `(1,234.56) CR` or `-500-`; the sign intent is ambiguous
- **Amounts that were already negative in the raw text** (`-1,234.56`) alongside CR notation — mixed conventions in one file suggest the export merged two systems
- **Zero amounts carrying CR notation** (`0.00 CR`) — usually harmless, but confirm the system isn't encoding something else
- **Any out-of-balance difference** between your converted total and the report control total, with the specific rows driving it

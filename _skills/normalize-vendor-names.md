---
name: normalize-vendor-names
title: Normalize Vendor and Account Names
description: Standardize vendor names, account numbers, and identifiers (case, whitespace, punctuation, leading zeros, aliases) so joins and lookups match reliably across systems.
category: cleaning
tools: pandas
---

## When to use this skill

Use this when the same vendor, member, or account appears under different spellings across sources, and your merges, lookups, or duplicate checks are missing matches. Classic symptoms:

- `"ACME CORP"`, `" Acme Corp. "`, and `"Acme  Corporation"` counted as three vendors
- Account numbers that won't join: `"0001200-01-000500"` in the GL vs `"1200-1-500"` in the subledger
- Identifiers with dropped leading zeros: CUSIP `"AB1234"` should be `"000AB1234"`; member ID `"123"` vs `"000123"`
- VLOOKUP-style merges returning blanks even though "the vendor is obviously there"

Run this **before** any merge, dedupe, or group-by on a name/ID column. Dirty keys are the #1 cause of "missing match" errors.

## Inputs it expects

- A pandas DataFrame with one or more text key columns (vendor name, account number, CUSIP, member ID)
- Knowledge of the target format: fixed length for padded IDs (e.g., CUSIP = 9 characters), and whether leading zeros should be **added** or **removed**
- Optionally, an alias table mapping known variants to a canonical name (build one as you find variants)

## Steps

1. **Snapshot**: record row count and count of distinct values in the key column before cleaning.
2. **Trim whitespace**: strip leading/trailing spaces, collapse internal runs of spaces to one.
3. **Standardize case**: UPPER for identifiers and tickers; Title Case for people/vendor display names.
4. **Fix zeros**: `.str.zfill(n)` to pad identifiers to fixed length, or `.str.lstrip('0')` to remove leading zeros (guard against `"0000"` becoming empty).
5. **Strip punctuation noise**: trailing periods, `.,` in "Inc." / "Corp.", and zeros after hyphens in structured account numbers.
6. **Apply the alias map** to collapse known variants (`"ACME CORPORATION"` → `"ACME CORP"`).
7. **Validate format** with a regex (e.g., CUSIP must be exactly 9 alphanumerics) and count survivors vs failures.
8. **Compare distinct counts** before and after — the drop tells you how many variants you collapsed.

## Code

```python
import pandas as pd

def normalize_key(series: pd.Series, pad_length: int = None,
                  strip_leading_zeros: bool = False) -> pd.Series:
    """Standardize an identifier or name column for reliable matching."""
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned.str.replace(r'\s+', ' ', regex=True)  # collapse spaces
    cleaned = cleaned.str.upper()

    if strip_leading_zeros:
        cleaned = cleaned.str.lstrip('0').replace('', '0')  # '0000' -> '0'
    elif pad_length:
        cleaned = cleaned.str.zfill(pad_length)

    return cleaned

# --- Usage on AP vendor master + investment holdings ---
ap = pd.read_excel('vendor_master.xlsx', dtype=str)
rows_in = len(ap)
vendors_before = ap['vendor_name'].nunique()

# Vendor names: trim, collapse spaces, uppercase, drop trailing punctuation
ap['vendor_name_clean'] = normalize_key(ap['vendor_name'])
ap['vendor_name_clean'] = ap['vendor_name_clean'].str.replace(r'[.,]+$', '', regex=True)

# Alias map: collapse known variants to one canonical name
alias_map = {
    'ACME CORPORATION': 'ACME CORP',
    'ACME CORP INC': 'ACME CORP',
    'A C M E CORP': 'ACME CORP',
}
ap['vendor_name_clean'] = ap['vendor_name_clean'].replace(alias_map)

# CUSIPs: pad to 9 characters, then validate format
ap['cusip_clean'] = normalize_key(ap['cusip'], pad_length=9)
valid_cusip = ap['cusip_clean'].str.match(r'^[A-Z0-9]{9}$')

# GL account numbers: remove zeros after hyphens, then leading zeros
# '0001200-01-000500' -> '1200-1-500'
ap['account_clean'] = (ap['gl_account'].astype(str).str.strip()
                       .str.replace(r'(?<=-)0+', '', regex=True)
                       .str.lstrip('0'))

# Control totals
print(f"Rows in: {rows_in} | Rows out: {len(ap)}")
print(f"Distinct vendors before: {vendors_before} | after: {ap['vendor_name_clean'].nunique()}")
print(f"Invalid CUSIPs: {(~valid_cusip).sum()}")
if (~valid_cusip).any():
    print(ap.loc[~valid_cusip, ['cusip', 'cusip_clean']])
```

## Validation (control totals)

- **Row count in = row count out.** Normalization changes values, never rows.
- **Distinct-count reconciliation.** Distinct vendors after cleaning should be **≤** distinct before; document the delta (e.g., "412 raw names collapsed to 387 canonical vendors — 25 variants merged"). An *increase* means something went wrong.
- **Amounts unaffected.** If the table carries amounts, `df['amount'].sum()` must be identical before and after — cleaning keys must never touch dollars.
- **Format validation count.** After padding, 100% of identifiers should match the target pattern (e.g., `^[A-Z0-9]{9}$` for CUSIPs). Report the pass rate.
- **Post-clean merge test.** If the point was a join, check the match rate before vs after cleaning — unmatched keys remaining are your exception list.

## Exceptions to surface

Send these to a reviewer — do not auto-resolve:

- **Identifiers that still fail format validation** after padding (wrong length, illegal characters) — may be genuinely bad data from the source
- **Distinct names that collapsed into one canonical value** — list each merged group so a human confirms `"ACME CORP"` and `"ACME CORP INC"` really are the same vendor (they might be a parent and subsidiary)
- **Near-miss pairs not in the alias map** — names that differ only by one or two characters (`"JON SMITH"` vs `"JOHN SMITH"`); flag for review rather than merging automatically
- **Values that became `"0"`** after leading-zero stripping — confirm all-zero IDs are intentional
- **Keys still unmatched after cleaning** in a downstream merge — these need manual research or an alias-map entry

---
name: flag-duplicate-transactions
title: Flag Duplicate Transactions
description: Detect and flag every member of a duplicate group (not just the repeats) so a reviewer can investigate before anything is removed; then dedupe with an audit trail.
category: cleaning
tools: pandas
---

## When to use this skill

Use this when duplicates may be inflating counts or totals and you need to investigate before deleting anything. Warning signs:

- Two people run "how many active members?" and get different numbers
- A vendor payment run shows the same invoice number twice
- A merged dataset suddenly has more rows than either source
- Member/employee counts don't tie to HR or the census

The professional rule: **flag first, investigate, then remove.** A duplicate invoice might be a data error — or a legitimate second payment. Deleting on autopilot destroys the evidence. The key tool is `duplicated(keep=False)`, which flags **every** member of a duplicate group (including the first occurrence) so the reviewer sees the whole group side by side.

## Inputs it expects

- A pandas DataFrame of transactions or member records
- The **business key** that defines "the same record" — e.g., `vendor_id + invoice_num`, or `member_id`. Choosing this key is the judgment call; all-columns-identical is a different (stricter) test worth running too.
- If keeping "most recent," a reliable date column to sort by
- Control totals from the source (record count, amount total) to tie against

## Steps

1. **Snapshot**: row count and amount total before anything else.
2. **Test for fully identical rows** first (`df.duplicated()` with no subset) — these are almost always safe-to-remove load errors, but count them separately.
3. **Flag business-key duplicates with `keep=False`** so every row in each duplicate group is marked — this is the review file, sorted by key so groups sit together.
4. **Investigate**: are the "duplicates" truly the same event, or legitimate multiples (a member with two accounts; two invoices with the same number from different vendors)?
5. **Decide the resolution per pattern**: keep-first, keep-most-recent (sort by date first), or aggregate (`groupby().sum()`) when multiples are legitimate and you need one row per entity.
6. **Dedupe with an audit trail** — keep the removed rows in a separate file with a reason and date.
7. **Reconcile**: rows kept + rows removed = rows in; explain the amount impact.

## Code

```python
import pandas as pd
from datetime import datetime

# Load AP transaction detail
txns = pd.read_excel('ap_transactions.xlsx')
rows_in = len(txns)
amount_in = txns['invoice_amount'].sum()

# --- Step 1: fully identical rows (usually double-loads) ---
exact_dupes = txns.duplicated()          # all columns match
print(f"Fully identical rows: {exact_dupes.sum()}")

# --- Step 2: flag EVERY member of each business-key duplicate group ---
key_cols = ['vendor_id', 'invoice_num']
txns['in_dupe_group'] = txns.duplicated(subset=key_cols, keep=False)

# Review file: whole groups together, so a human sees all versions side by side
review = (txns[txns['in_dupe_group']]
          .sort_values(key_cols + ['invoice_date']))
review.to_excel('duplicates_for_review.xlsx', index=False)
print(f"Rows in duplicate groups (for review): {len(review)}")
print(f"Distinct duplicated keys: {review.drop_duplicates(subset=key_cols).shape[0]}")

# --- Step 3: after review, dedupe with an audit trail ---
def deduplicate_with_audit(df, subset_cols, sort_col=None, keep='first'):
    """Remove duplicates, returning (kept, removed-with-audit-info)."""
    df = df.copy()
    if sort_col:                          # keep most recent: sort, then keep last
        df = df.sort_values(sort_col)
    is_dupe = df.duplicated(subset=subset_cols, keep=keep)
    kept = df[~is_dupe].copy()
    removed = df[is_dupe].copy()
    removed['removal_date'] = datetime.now()
    removed['removal_reason'] = f'Duplicate on {subset_cols} (kept {keep})'
    return kept, removed

txns_clean, txns_removed = deduplicate_with_audit(
    txns, subset_cols=key_cols, sort_col='invoice_date', keep='last'
)
txns_removed.to_excel('removed_duplicates_audit.xlsx', index=False)

# --- Control totals ---
print(f"Rows in: {rows_in} | kept: {len(txns_clean)} | removed: {len(txns_removed)}")
assert len(txns_clean) + len(txns_removed) == rows_in
print(f"Amount in:      {amount_in:,.2f}")
print(f"Amount kept:    {txns_clean['invoice_amount'].sum():,.2f}")
print(f"Amount removed: {txns_removed['invoice_amount'].sum():,.2f}")
print(f"Unique vendor+invoice keys: {txns_clean.drop_duplicates(subset=key_cols).shape[0]}")
```

## Validation (control totals)

- **Row reconciliation.** Rows kept + rows removed = rows in. Assert it in code; never let rows vanish unaccounted.
- **Amount reconciliation.** Amount in = amount kept + amount removed. The "amount removed" figure is your quantified duplicate exposure — report it explicitly (e.g., "removed 14 rows totaling $42,318.55").
- **Key uniqueness after dedupe.** `txns_clean.duplicated(subset=key_cols).sum()` must be 0.
- **Unique-count cross-check.** `df['member_id'].nunique()` before dedupe should equal `len(df)` after keep-first dedupe on `member_id` — two roads to the same number.
- **If aggregating instead of removing**: the grouped total (`groupby(key).sum()`) must equal the pre-aggregation total exactly — aggregation moves no dollars.

## Exceptions to surface

The review file — every member of every duplicate group — goes to a human. Highlight in particular:

- **Same key, different amounts** — same vendor + invoice number but $5,000 vs $5,500. Could be a keying error, a partial payment, or a corrected reissue; only a person (or the vendor) can say.
- **Same key, different dates far apart** — a possible genuine duplicate payment (recovery opportunity) rather than a data glitch.
- **Fully identical rows** — likely double-loaded files; confirm the load history before removing, and note which batch caused it so it doesn't recur.
- **Legitimate-multiple patterns** — one customer with checking + savings + retirement accounts is *not* a duplicate person; these should be aggregated or counted with `nunique()`, never deleted.
- **Near-duplicates the exact match missed** — names or vendors differing by a typo (`"Jon Smith"` / `"John Smith"`); list high-similarity pairs separately for manual confirmation rather than merging automatically.

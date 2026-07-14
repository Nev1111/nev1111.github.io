---
layout: page
title: Data Analytics Quick Reference
subtitle: Practical concepts for accounting data analysis
permalink: /cheatsheet/
---

Use this as a plain-English reference for common accounting analytics tasks.

## Data setup

| Task | Concept | What to check |
|---|---|---|
| Load a report | Source intake | file name, report date, row count, control total |
| Inspect a file | Data profiling | columns, blanks, data types, duplicate keys |
| Standardize fields | Data cleanup | dates, amounts, account numbers, names |
| Preserve source totals | Control check | totals before and after transformation |

## Excel habit → analytics concept

| Excel habit | Analytics concept | Review output |
|---|---|---|
| VLOOKUP / XLOOKUP | table joins | matched and unmatched records |
| Pivot Table | grouped summary | totals by account, department, period |
| SUMIFS / COUNTIFS | conditional aggregation | rule-based totals |
| manual filter | exception criteria | repeatable review list |
| Remove Duplicates | duplicate analysis | duplicate groups with reasons |
| IF formulas | classification rules | documented decision logic |

## Data quality checks

- Missing account/vendor/customer IDs
- Duplicate transaction IDs
- Dates outside the expected period
- Amounts equal to zero
- Round-dollar transactions
- Weekend or holiday activity
- Unmatched master-data records
- Text fields with inconsistent spelling or spacing

## Reconciliation pattern

1. Identify the two sources.
2. Define the matching key.
3. Preserve control totals from both sources.
4. Separate matched and unmatched records.
5. Summarize exceptions by reason.
6. Export a review-ready workpaper.

## Reporting pattern

1. Define the reporting period.
2. Clean the date and amount fields.
3. Group by the business dimensions that matter.
4. Tie totals back to the source report.
5. Save the logic so it can be reused next month.

## Workpaper tabs worth creating

- `Summary`
- `Exceptions`
- `Matched Detail`
- `Data Quality Notes`
- `Source Control Totals`

## Questions to ask before automating

- Is this task repeated every month, quarter, or audit cycle?
- Are the source files consistent enough to standardize?
- What exceptions require human judgment?
- What control total proves the output is complete?
- Who reviews the final workpaper?

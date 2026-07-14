---
layout: page
title: Accounting Analytics Recipes
subtitle: StackOverflow-style answers for spreadsheet problems accountants see every week
permalink: /recipes/
---

This is the quick problem/solution index. Start with the accounting task you recognize, then use the suggested analytics concept to structure the work.

## Lookups, joins, and reconciliations

### How do I replace a fragile lookup workbook?

Use a table-join mindset: identify the shared key, define what counts as a valid match, and create a separate exception list for anything unmatched.

**Good for:** vendor master lookups, account classifications, department mappings, customer IDs.

### How do I find transactions in one report but not another?

Create three buckets: matched, source A only, and source B only. Then summarize the unmatched records by amount, account, vendor, and period.

**Good for:** bank reconciliations, subledger-to-GL checks, payroll comparisons, payment files.

### How do I match records when dates are close but not exact?

Use nearest-match logic, but document the tolerance. For example: same customer, same amount, transaction date within three business days.

**Good for:** deposits, settlement files, investment activity, timing differences.

## Cleaning messy exports

### How do I clean negative numbers exported like `1,234.56-` or `1,234CR`?

Define one standard amount format, convert every export to that standard, then validate totals before and after cleanup.

### How do I extract dollar amounts from descriptions?

Treat the description as a data source. Identify the recurring text pattern, pull the amount into its own field, and review exceptions where no amount is found.

### How do I clean inconsistent account/vendor names?

Standardize case, whitespace, punctuation, abbreviations, and known aliases before comparing records.

## Summaries and reporting

### How do I replace a pivot table rebuild?

Define the rows, columns, values, and aggregation rule once. The repeatable concept is grouped summarization.

### How do I create monthly or fiscal-year summaries?

Create a reporting-period field first. Then summarize by that period instead of rebuilding date logic each month.

### How do I export a clean workpaper?

Separate the output into tabs: Summary, Exceptions, Detail, and Data Quality Notes.

## Quality checks and audit-style testing

### How do I find duplicates without losing the details?

Flag every record involved in a duplicate group. Do not immediately remove duplicates until you understand why they exist.

### How do I spot unusual transactions?

Start with simple tests: round numbers, weekends, missing master-data matches, unusually large amounts, duplicate descriptions, and activity outside expected periods.

---

## Have a recipe request?

Bring a sanitized version of your spreadsheet problem to the [PANDAUDIT Discord]({{ '/community/' | relative_url }}). The best questions become future recipes.

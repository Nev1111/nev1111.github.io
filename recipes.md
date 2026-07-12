---
layout: page
title: Accounting Python Recipes
subtitle: StackOverflow-style answers for accountants replacing Excel routines with pandas
permalink: /recipes/
---

This is the quick problem/solution index. Start with the accounting task you recognize, then jump to the relevant PANDAUDIT guide.

## Lookups, joins, and reconciliations

<div class="pandaudit-recipe-list">

### How do I replace VLOOKUP in pandas?
Use `merge` to join two tables by a shared key, then check for missing matches.

- [When VLOOKUP Fails You: Merge Functions]({% post_url 2026-01-26-when-vlookup-fails-you-merge-functions %})
- [Merge Excel and SQL Databases Safely]({% post_url 2026-01-15-merge-excel-sql-databases-safely %})

### How do I find transactions in one report but not another?
Use an outer merge with `indicator=True`, then filter anything not matched on both sides.

- [The Copy-Paste Nightmare: Automated Reconciliations]({% post_url 2026-01-25-the-copy-paste-nightmare-automated-reconciliations %})
- [Data Analytics Quick Reference]({{ '/cheatsheet/' | relative_url }}#reconciliation-techniques)

### How do I match records when dates are close but not exact?
Use `merge_asof` for nearest-date matching.

- [Performing More Complex Merges]({% post_url 2020-5-5-Performing more complex merges %})
- [Streamline Data Analysis With Python's merge_asof Function]({% post_url 2023-7-2-Streamline-data-analysis-with-pythons's-merge_as_of-function %})

</div>

## Cleaning messy exports

### How do I clean negative numbers exported like `1,234.56-` or `1,234CR`?
Normalize the text first, move the sign to the front, then convert to a number.

- [Credit/Debit Notation Nightmare Solved]({% post_url 2026-01-10-credit-debit-notation-nightmare-solved %})
- [Converting Numeric Negative Legacy Balances]({% post_url 2022-9-17-Converting-numeric-negative-legacy-balances %})

### How do I extract dollar amounts from descriptions?
Use string methods and regular expressions to pull numbers out of text.

- [Text Parsing Adventures: Data Speaks Two Languages]({% post_url 2026-01-29-text-parsing-adventures-data-speaks-two-languages %})
- [Extracting US Amount DataFrame]({% post_url 2022-9-18-Extracting-US-Amount-dataframe %})

### How do I clean inconsistent account/vendor names?
Standardize case, whitespace, punctuation, and known abbreviations before comparing.

- [String Cleaning and Normalization in Python]({% post_url 2026-01-16-string-cleaning-normalization-python %})
- [Master Data Mapping and Classifications]({% post_url 2026-01-17-master-data-mapping-classifications %})

## Summaries and reporting

### How do I replace a Pivot Table?
Use `pivot_table` for spreadsheet-style summaries and `groupby` for programmatic summaries.

- [Pivot Tables on Steroids]({% post_url 2026-01-12-pivot-tables-on-steroids-multi-level-analysis-in-one-line %})
- [Groupby + Transform: The Excel Killer Feature]({% post_url 2026-01-14-groupby-+-transform-the-excel-killer-feature %})

### How do I create monthly or fiscal-year summaries?
Convert dates once, add a period/fiscal column, then group by it.

- [Government Fiscal Year Calculations Made Easy]({% post_url 2026-01-13-government-fiscal-year-calculations-made-easy %})
- [Fiscal Year Fiasco: Excel Dates Hate Accountants]({% post_url 2026-01-27-fiscal-year-fiasco-excel-dates-hate-accountants %})

### How do I export a clean Excel workbook with multiple tabs?
Use `ExcelWriter` and write each output table to its own sheet.

- [End-to-End Workflow Example]({% post_url 2026-01-22-end-to-end-workflow-example %})
- [Data Analytics Quick Reference]({{ '/cheatsheet/' | relative_url }}#data-export-for-reports)

## Quality checks and audit-style testing

### How do I find duplicates without losing the details?
Use `duplicated(keep=False)` to show every row involved in duplicate groups.

- [Handle Duplicates Like a Pro]({% post_url 2026-01-20-handle-duplicates-like-a-pro %})

### How do I spot unusual transactions?
Start with round numbers, weekends, outliers, and missing master-data matches.

- [Data Analytics Quick Reference]({{ '/cheatsheet/' | relative_url }}#anomaly-detection-patterns)
- [The Case of Missing Millions: Rounding Errors]({% post_url 2026-01-28-case-of-missing-millions-rounding-errors %})

---

## Have a recipe request?

Bring a sanitized version of your spreadsheet problem to the [PANDAUDIT Discord]({{ '/community/' | relative_url }}). The best new questions become future recipes.

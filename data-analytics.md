---
layout: page
title: Analytics Map
subtitle: A practical route from messy finance files to reviewable workflows
permalink: /data-analytics/
eyebrow: plot your course
---

Most people in finance do not need abstract theory first. They need a map for recurring spreadsheet work: what comes in, what rule is applied, what exceptions appear, and what output is reviewable.

## The route, in seven waypoints

<div class="legs" markdown="1">

[**Ask the finance question**{: .leg-name} **01**{: .leg-no} <span class="leg-desc">What decision, control, or review are we supporting?</span>](#ask-the-finance-question)

[**Inventory the sources**{: .leg-name} **02**{: .leg-no} <span class="leg-desc">Exports, ledgers, billing files, forecasts, workbooks</span>](#inventory-the-sources)

[**Clean the fields**{: .leg-name} **03**{: .leg-no} <span class="leg-desc">Dates, amounts, IDs, names, blanks, duplicates</span>](#clean-the-fields)

[**Match and classify**{: .leg-name} **04**{: .leg-no} <span class="leg-desc">Lookup rules, mappings, segments, exception logic</span>](#match-and-classify)

[**Summarize for review**{: .leg-name} **05**{: .leg-no} <span class="leg-desc">Grouped totals, trends, reconciled balances</span>](#summarize-for-review)

[**Surface exceptions**{: .leg-name} **06**{: .leg-no} <span class="leg-desc">The rows a person actually needs to inspect</span>](#surface-exceptions)

[**Package the workpaper**{: .leg-name} **07**{: .leg-no} <span class="leg-desc">Summary, detail, controls, notes, and next action</span>](#package-the-workpaper)

[**Hand the route to an agent**{: .leg-name} **08**{: .leg-no} <span class="leg-desc">Turn the repeatable route into a SKILL.md an AI can run</span>]({{ '/ai/' | relative_url }})

</div>

## Ask the finance question

Start with the decision, not the tool:

- Are two reports supposed to agree?
- Which transactions need review?
- What changed from last month?
- Which customers, vendors, accounts, or products are driving the movement?
- What would the reviewer need to sign off confidently?

## Inventory the sources

Write down the source files before touching the data:

- file name
- report date
- system of origin
- row count
- control total
- owner or reviewer

## Clean the fields

Common finance data problems:

- dates stored as text
- amounts with trailing signs or credit/debit labels
- blank IDs
- duplicate records
- inconsistent naming
- headers repeated inside exported reports

## Match and classify

This is where messy files start becoming useful. Define the matching key, the classification rule, and what counts as an exception.

## Summarize for review

Group the data by the dimensions that matter: period, account, department, product, vendor, customer, region, project, or scenario.

## Surface exceptions

The best workflow does not bury reviewers in data. It creates a focused list of items that need judgment.

## Package the workpaper

A good output is easy to review:

- Summary
- Exceptions
- Detail
- Data-quality notes
- Source control totals
- Next action

## Need help plotting a route?

Bring a sanitized example to the [PANDAUDIT Discord]({{ '/community/' | relative_url }}). Describe the source, the rule, the exception, and the output you wish you had.

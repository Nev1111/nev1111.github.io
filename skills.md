---
layout: page
title: Skills Library
subtitle: Ready-made instructions your AI assistant can run
permalink: /skills/
eyebrow: copy, paste, done
---

Each skill below is a ready-made set of instructions for one common finance task.

To try one: **open it, copy the whole page, and paste it into Claude or ChatGPT together
with your file** (remove anything confidential first). The AI does the work; you review
what comes back. Every skill ends with the checks that prove the output ties.

Every skill has the same simple shape: when to use it, what it needs, the steps, and the
checks. Read one like a recipe even if you never hand it to an AI.

## Cleaning messy exports

<div class="legs" markdown="1">

[**Clean credit/debit amounts**{: .leg-name} **01**{: .leg-no} <span class="leg-desc">Turn `1,234.56-` and `1,234CR` into clean numerics that tie out</span>]({{ '/skills/clean-credit-debit-amounts/' | relative_url }})

[**Normalize vendor & account names**{: .leg-name} **02**{: .leg-no} <span class="leg-desc">Standardize case, whitespace, punctuation, and known aliases</span>]({{ '/skills/normalize-vendor-names/' | relative_url }})

[**Parse legacy system reports**{: .leg-name} **03**{: .leg-no} <span class="leg-desc">Extract clean tables from text-dump exports with repeated headers</span>]({{ '/skills/parse-legacy-reports/' | relative_url }})

[**Flag duplicate transactions**{: .leg-name} **04**{: .leg-no} <span class="leg-desc">Find every record in a duplicate group without deleting evidence</span>]({{ '/skills/flag-duplicate-transactions/' | relative_url }})

</div>

## Matching and reconciliation

<div class="legs" markdown="1">

[**Tolerance date matching**{: .leg-name} **05**{: .leg-no} <span class="leg-desc">Match records when dates are close but not exact (merge_asof)</span>]({{ '/skills/tolerance-date-matching/' | relative_url }})

[**Safe Excel-to-SQL merges**{: .leg-name} **06**{: .leg-no} <span class="leg-desc">Join spreadsheet and database data without silent row loss</span>]({{ '/skills/safe-excel-sql-merges/' | relative_url }})

[**Master-data mapping**{: .leg-name} **07**{: .leg-no} <span class="leg-desc">Apply account classifications and department mappings with exception lists</span>]({{ '/skills/master-data-mapping/' | relative_url }})

[**Replace nested IFs with rules**{: .leg-name} **08**{: .leg-no} <span class="leg-desc">Turn 12-level IF formulas into readable, testable classification logic</span>]({{ '/skills/replace-nested-ifs/' | relative_url }})

</div>

## Summaries, periods, and reshaping

<div class="legs" markdown="1">

[**Fiscal period calculations**{: .leg-name} **09**{: .leg-no} <span class="leg-desc">Government fiscal years and quarters computed once, reused everywhere</span>]({{ '/skills/fiscal-period-calculations/' | relative_url }})

[**Group comparisons with transform**{: .leg-name} **10**{: .leg-no} <span class="leg-desc">Compare each row to its group total without losing detail rows</span>]({{ '/skills/groupby-transform-comparisons/' | relative_url }})

[**Reshape with melt & pivot**{: .leg-name} **11**{: .leg-no} <span class="leg-desc">Move between wide report layouts and tall analysis layouts</span>]({{ '/skills/reshape-melt-pivot/' | relative_url }})

[**Multi-year consolidation**{: .leg-name} **12**{: .leg-no} <span class="leg-desc">Stack yearly files with different columns into one reviewable set</span>]({{ '/skills/multi-year-consolidation/' | relative_url }})

</div>

## The five-step habit

1. **Pick the skill** that matches your task, and glance at its checks first.
2. **Copy the whole skill** and paste it into Claude or ChatGPT — or, if you use a coding agent, save it into its skills folder ([Tutorial 2]({{ '/tutorials/' | relative_url }}#tutorial-2-give-a-skill-to-an-ai-coding-agent) shows how).
3. **Attach your file and name the skill**: *"Use the clean-credit-debit-amounts skill on this export."*
4. **Review like a preparer's work**: the checks first, then the exception list, then spot-check detail.
5. **Improve and share**: post what broke in the [Discord]({{ '/community/' | relative_url }}) #skills channel.

Each step above is walked through click-by-click in the [Tutorials]({{ '/tutorials/' | relative_url }}) — including using skills without a terminal, and organizing them into an Obsidian-style [knowledge vault]({{ '/tutorials/' | relative_url }}#tutorial-3-build-your-finance-knowledge-vault-the-obsidian-way). New to the concepts? Start with the [AI Field Kit]({{ '/ai/' | relative_url }}).

## Tried one? Tell me. Missing one? Ask.

The library grows from real use. If you ran a skill, I want to know how it went — the tie-out,
the exceptions, the weird thing the agent did. And if you have a manual process that deserves
to become a skill, describe it and I'll build it.

- Post results or requests in the [community]({{ '/community/' | relative_url }})
- Or email [hello@pandaudit.com](mailto:hello@pandaudit.com)

## More resources

- [Recipes]({{ '/recipes/' | relative_url }}) — classic copy-paste code, no agent required
- [Cheat sheet]({{ '/cheatsheet/' | relative_url }}) — quick pandas reference
- [Analytics map]({{ '/data-analytics/' | relative_url }}) — the thinking behind every skill: source, rule, exception, review

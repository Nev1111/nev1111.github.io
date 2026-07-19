---
layout: page
title: Skills Library
subtitle: Every PANDAUDIT script, rewritten as a skill your AI agent can run
permalink: /skills/
eyebrow: agent-ready markdown
---

In the AI era, a script you copy/paste is only half the asset. The other half is a
**skill**: a markdown document that tells an AI agent *when* to use the technique, *what*
inputs to expect, *how* to run it, and *which* control totals prove it worked.

Every skill below follows the same shape — the same shape used by agent frameworks like
Claude Code's `.claude/skills/` folders:

```markdown
---
name: skill-slug
description: One line an agent uses to decide when this skill applies
---
## When to use this skill
## Inputs it expects
## Steps
## Code
## Validation (control totals)
## Exceptions to surface
```

Use them three ways: **read** them like recipes, **run** the code yourself, or **hand**
the raw markdown to your AI agent and review its output like any other preparer's work.

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

## How to hand a skill to an AI agent

1. **Pick the skill** that matches your task, and read its validation section first.
2. **Save the raw markdown** as `SKILL.md` in your agent's skills folder — or paste it into a chat AI as the procedure to follow.
3. **Point the agent at your file** and name the skill: *"Use the clean-credit-debit-amounts skill on this export."*
4. **Review like a preparer's work**: check the control totals, then the exception list, then spot-check detail.
5. **Improve and share**: post what broke in the [Discord]({{ '/community/' | relative_url }}) Skill Swap channel.

Each step above is walked through click-by-click in the [Agent Tutorials]({{ '/tutorials/' | relative_url }}) — including using skills without a terminal, and organizing them into an Obsidian-style [knowledge vault]({{ '/tutorials/' | relative_url }}#tutorial-3-build-your-finance-knowledge-vault-the-obsidian-way). New to the concepts? Start with the [AI Field Kit]({{ '/ai/' | relative_url }}).

---
layout: post
title: "Your Spreadsheet Scripts Are Now Skills"
subtitle: "Announcing the PANDAUDIT Skills Library — every script, rewritten for the AI era"
tags: [ai, skills, agents, automation, announcement]
---

For years, this site shared Python scripts you could copy into your own finance work: clean the export, match the files, flag the duplicates, tie the totals.

That format just got an upgrade. Every core PANDAUDIT technique now lives in the [Skills Library]({{ '/skills/' | relative_url }}) as a **skill** — a markdown document an AI agent can actually execute.

## What changed

A script answers *how*. A skill also answers *when*, *with what inputs*, and *how you know it worked*. Every skill follows the same shape:

- **When to use this skill** — so an agent (or a colleague) picks the right tool
- **Inputs it expects** — the files and fields, named
- **Steps and code** — the same working pandas logic as before
- **Validation** — control totals: rows in, rows out, amounts tied
- **Exceptions to surface** — the rows a human still has to judge

## Three ways to use one

1. **Read it** like a recipe, same as always.
2. **Run it** yourself — the code is right there.
3. **Hand it to your agent** — save the raw markdown as `SKILL.md` in your agent's skills folder and say: *"Use the clean-credit-debit-amounts skill on this export."*

## Accounting takeaway

The technique didn't change. The packaging did — because your next junior preparer might be an AI agent, and it works best when the procedure is written down. Start with the skill that matches the task you repeated this week, and tell us how it went in the [Discord]({{ '/community/' | relative_url }}) Skill Swap channel.

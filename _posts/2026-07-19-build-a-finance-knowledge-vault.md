---
layout: post
title: "Build a Finance Knowledge Vault (the Obsidian Way)"
subtitle: "Why one folder of markdown files beats every knowledge tool you've abandoned"
tags: [ai, knowledge-base, obsidian, documentation, agents]
---

Every finance team has tried a knowledge tool — the wiki nobody updates, the SharePoint nobody can find anything in, the OneNote from three reorgs ago. The tools failed for the same reason: the knowledge was locked in someone else's format, somewhere off to the side of the actual work.

Obsidian users figured out the fix years ago, and it turns out to be exactly what AI needs too: a **vault**.

## A vault is just a folder

Plain markdown files, in a folder, linking to each other with `[[wiki-links]]`. That's the whole trick. No database. Readable in any editor, on any machine, in ten years. And — this is the new part — readable by an AI agent, which can search it, follow the links, and **cite the exact note** an answer came from.

## What goes in a finance vault

- `procedures/` — your recurring tasks as steps. These are your [skills]({{ '/skills/' | relative_url }}).
- `reference/` — chart-of-accounts logic, fiscal calendar, vendor aliases.
- `decisions/` — why the write-off threshold is what it is, dated.
- `close/` — the checklist, linking to everything above.

When your bank-rec procedure says "normalize names per `[[vendor-aliases]]`", a new hire follows the link — and so does your agent.

## The rule that makes it trustworthy

Point an AI at your vault and ask something you already know. If the answer cites the right note, good. If there's no citation: **no citation, no reliance.** Same standard as any workpaper.

## Start with three files

Not a taxonomy. Not a migration project. Three files: your classification rules, one reconciliation procedure, your fiscal-calendar definitions. Grow it every time you answer the same question twice.

The full walkthrough — including pointing Claude or ChatGPT at your vault — is in the new [Agent Tutorials]({{ '/tutorials/' | relative_url }}). And when your first note becomes your first skill, the [Discord]({{ '/community/' | relative_url }}) Skill Swap channel wants to see it.

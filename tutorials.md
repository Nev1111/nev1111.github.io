---
layout: page
title: Agent Tutorials
subtitle: Step-by-step — from "what's a skill?" to an AI agent doing your prep work
permalink: /tutorials/
eyebrow: hands-on walkthroughs
---

Reading about AI is one thing. This page is the other thing: four walkthroughs, starting
with the easiest possible way to try a skill — copy, paste, done.

<div class="legs" markdown="1">

[**Copy & paste a skill**{: .leg-name} **01**{: .leg-no} <span class="leg-desc">The easy way: use Claude or ChatGPT — nothing to install</span>](#tutorial-1-copy-a-skill-into-claude-or-chatgpt)

[**Use a coding agent**{: .leg-name} **02**{: .leg-no} <span class="leg-desc">For the technical crowd: hand skills to an AI that works on your computer</span>](#tutorial-2-give-a-skill-to-an-ai-coding-agent)

[**Build a knowledge vault**{: .leg-name} **03**{: .leg-no} <span class="leg-desc">One folder of notes that both you and your AI can use</span>](#tutorial-3-build-your-finance-knowledge-vault-the-obsidian-way)

[**Review the output**{: .leg-name} **04**{: .leg-no} <span class="leg-desc">The sign-off checklist: totals, exceptions, spot-checks</span>](#tutorial-4-review-agent-output-like-a-workpaper)

</div>

## Tutorial 1: Copy a skill into Claude or ChatGPT

The easiest way to try a skill. Nothing to install, nothing technical — if you can copy
and paste, you can do this.

**Step 1 — pick a skill.** Go to the [Skills Library]({{ '/skills/' | relative_url }}) and choose one that matches a task you did this month. First-timers: [clean-credit-debit-amounts]({{ '/skills/clean-credit-debit-amounts/' | relative_url }}) is the classic.

**Step 2 — copy the whole skill page** and paste it into a new chat in Claude or ChatGPT with this framing:

> Here is a procedure document. Follow it exactly on the file I attach.
> Report the checks at the end, and list anything unusual instead of
> fixing it silently.

**Step 3 — attach your file** and let it work. Remove confidential information first — names, account numbers, anything you wouldn't put in an email outside the office.

**Step 4 — review the result.** Do the totals still match? What ended up on the exceptions list? [Tutorial 4](#tutorial-4-review-agent-output-like-a-workpaper) is the checklist.

**Tip:** in claude.ai you can save skills to a Project, or in ChatGPT to a custom GPT, so every new chat already knows your procedures. That's a mini [knowledge vault](#tutorial-3-build-your-finance-knowledge-vault-the-obsidian-way) — which brings us to the real thing.

Then come tell the [community]({{ '/community/' | relative_url }}) how it went — or which task you wish had a skill.

## Tutorial 2: Give a skill to an AI coding agent

The step up from Tutorial 1, for when you're comfortable with slightly more technical
tools. A coding agent works directly on your computer: it reads your files, does the
work, and shows you everything it did.

**You need:** an AI coding agent (this walkthrough uses [Claude Code](https://claude.com/claude-code); the pattern is the same in others) and one messy export you know well. Remove confidential information first.

**Step 1 — pick the skill,** same as Tutorial 1.

**Step 2 — install it.** Every skill page links to its raw text. Save it in your project like this:

```text
my-close-work/
├── .claude/
│   └── skills/
│       └── clean-credit-debit-amounts/
│           └── SKILL.md      ← the file you downloaded
└── data/
    └── gl_export_march.xlsx  ← your sanitized file
```

That folder convention is how the agent discovers what it knows how to do. The skill's
`description` line is what it reads to decide when the skill applies — which is why every
PANDAUDIT skill leads with one.

**Step 3 — delegate, specifically.** Start the agent in that folder and give it a memo, not a wish:

> Use the clean-credit-debit-amounts skill on data/gl_export_march.xlsx.
> The amount column is "Net Amt". Control total per the source system is $2,914,003.17.
> Give me the cleaned file, the exception list, and the before/after totals.

**Step 4 — watch what it does.** The agent will read the skill, do the work, and report back. Notice it follows the skill's own checks — that's the point. The procedure you'd give a junior is now something a machine can run.

**Step 5 — review.** Don't skip to "looks good." Use [Tutorial 4](#tutorial-4-review-agent-output-like-a-workpaper).

## Tutorial 3: Build your finance knowledge vault (the Obsidian way)

[Obsidian](https://obsidian.md) popularized a simple, powerful idea: your knowledge lives in a **vault** — a plain folder of `.md` files that link to each other with `[[wiki-links]]`. No database, no lock-in, readable forever.

That same idea is exactly what an **AI knowledge base** is. A vault of markdown files is something both you and an AI agent can search, cite, and follow. Skills are just the executable subset of the vault — procedures instead of notes.

**Step 1 — make the vault.** A folder. That's it. (Open it in Obsidian if you want the nice graph and linking; any editor works.)

```text
finance-vault/
├── procedures/          ← skills live here
│   ├── clean-credit-debit-amounts.md
│   └── bank-rec-monthly.md
├── reference/
│   ├── chart-of-accounts-logic.md
│   ├── fiscal-calendar.md
│   └── vendor-aliases.md
├── decisions/
│   └── 2026-03-writeoff-threshold.md
└── close/
    └── close-checklist.md
```

**Step 2 — seed it with three files.** Don't plan a taxonomy; write the three documents you already re-explain most often:

1. Your account-classification rules (the ones living in your head).
2. One recurring reconciliation, as numbered steps.
3. Your fiscal-calendar definitions (start with the [fiscal-period-calculations]({{ '/skills/fiscal-period-calculations/' | relative_url }}) skill).

**Step 3 — link, don't file.** Inside a note, reference others with `[[vendor-aliases]]`-style links. When your bank-rec procedure says "normalize names per `[[vendor-aliases]]`", both a new hire and an agent can follow the trail. Linking is what turns a pile of notes into a knowledge bank.

**Step 4 — point your agent at it.** With a coding agent, open it in the vault folder — it can read every note. With a chat AI, add the vault files to a Project / custom GPT. Then ask something you already know the answer to and check that it cites the right note. **No citation, no reliance.**

**Step 5 — grow it by subtraction.** Every time you answer a question twice, the second answer becomes a vault note. Every task you do twice becomes a skill in `procedures/`. A year from now the vault, not any one workbook, is your most valuable file.

## Tutorial 4: Review agent output like a workpaper

The agent is a very fast preparer. You're the reviewer. Same discipline as ever:

1. **Tie the control totals first.** Rows in = matched + exceptions. Amount in = amount out ± documented adjustments. If totals don't tie, stop — nothing else matters.
2. **Read the exception list, not the clean list.** The agent's job was to shrink your review to the rows needing judgment. Judge them.
3. **Spot-check the "clean" side.** Sample a few matched/cleaned rows back to source. Trust builds from verification, not vibes.
4. **Check the skill was actually followed.** The skill's Validation section is your review checklist — the agent should have reported each item.
5. **Keep the trail.** Save the skill version, the agent's output, and your notes together. That bundle *is* the workpaper.

Something break? That's genuinely useful — bring it to the [Discord]({{ '/community/' | relative_url }}) #agents channel and the fix becomes an update to the skill for everyone.

## Where next

- [Skills Library]({{ '/skills/' | relative_url }}) — pick your first skill
- [AI Field Kit]({{ '/ai/' | relative_url }}) — the concepts behind all of this
- [Discord]({{ '/community/' | relative_url }}) — share results in #skills and #agents

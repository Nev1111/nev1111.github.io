---
layout: page
title: AI Field Kit
subtitle: Knowledge bases, skills, and agents — explained in finance language
permalink: /ai/
eyebrow: the new toolbox
---

AI did not replace the analytics map. It gave you a junior team member who can follow it —
fast, tireless, and only as good as the instructions and review you provide. This page
explains the AI concepts every finance professional now bumps into, using the work you
already know: exports, reconciliations, close packages, and workpapers.

## The field kit, in six pieces

<div class="legs" markdown="1">

[**Prompts & context**{: .leg-name} **01**{: .leg-no} <span class="leg-desc">The instruction memo you hand the AI — scope, sources, and definitions</span>](#prompts--context)

[**Skills (.md files)**{: .leg-name} **02**{: .leg-no} <span class="leg-desc">Reusable procedures written in markdown that an agent can execute</span>](#skills-md-files)

[**Agents**{: .leg-name} **03**{: .leg-no} <span class="leg-desc">AI that takes actions — runs code, reads files, produces workpapers</span>](#agents)

[**Knowledge bases**{: .leg-name} **04**{: .leg-no} <span class="leg-desc">Your policies, mappings, and procedures organized so AI can cite them</span>](#knowledge-bases)

[**RAG & citations**{: .leg-name} **05**{: .leg-no} <span class="leg-desc">How AI grounds answers in your documents instead of guessing</span>](#rag--citations)

[**The human reviewer**{: .leg-name} **06**{: .leg-no} <span class="leg-desc">Control totals, professional skepticism, and sign-off stay with you</span>](#the-human-reviewer)

</div>

## Prompts & context

A prompt is the memo you would write for a new staff accountant: what the task is, which
files to use, what the rules are, and what the output should look like. Vague memo, vague
work — same as always.

The PANDAUDIT route you already know **is** a great prompt structure:

> "Here is the source (AP export, March, 4,812 rows, control total $2,914,003.17).
> Here is the rule (match to the payment file on vendor + amount, dates within 3 business
> days). Here is what counts as an exception. Give me Summary, Exceptions, Detail, and
> the control totals tying back."

## Skills (.md files)

A **skill** is a procedure written in a plain markdown file — a `SKILL.md` — that tells an
agent when to use a technique, what inputs it expects, the steps, the code, and the
validation checks. Think of it as a workpaper template plus a procedure narrative that a
machine can actually follow.

This is the biggest shift for this site: every PANDAUDIT script now lives in the
[Skills Library]({{ '/skills/' | relative_url }}) as a skill document. You can read one
like a recipe, run the code yourself, or drop the file into your agent's skills folder
and delegate the task.

Why markdown files? They are readable by humans, versionable in git, reviewable like any
workpaper, and every major agent framework (Claude Code, and others) treats them as the
native way to package know-how.

## Agents

A chatbot answers questions. An **agent** takes actions: it reads your export, writes and
runs the cleanup code, checks the totals, and drafts the exception memo — then shows you
its work. If a skill is the procedure narrative, the agent is the staff member executing it.

Rules of engagement that will feel familiar from supervising juniors:

- Give the agent one defined task with named sources, not "fix my close."
- Insist on control totals in every output.
- Sanitize confidential data before it leaves your environment.
- Review the exception list yourself. Judgment is not delegated.

## Knowledge bases

An **AI knowledge base** is your institutional knowledge — chart of accounts logic,
mapping tables, close checklists, policy memos, prior-period workpapers — organized so an
AI can search it and cite it. The finance teams getting real value from AI are not the
ones with the fanciest model; they are the ones whose knowledge is written down.

If you've heard of [Obsidian](https://obsidian.md), you already know the shape: a
**vault** — one folder of plain `.md` files that link to each other with
`[[wiki-links]]`. No database, no vendor lock-in, readable in any editor, versionable in
git. That vault *is* a knowledge base, and it's the ideal one for AI: agents can search
it, follow the links, and cite the exact note an answer came from. Skills are simply the
executable notes in the vault — procedures instead of prose.

Start embarrassingly small: one folder of markdown files. Your account-classification
rules. Your recurring reconciliation procedures. Your fiscal-calendar definitions. Each
document you write becomes something both new hires *and* agents can use. The
[knowledge-vault tutorial]({{ '/tutorials/' | relative_url }}#tutorial-3-build-your-finance-knowledge-vault-the-obsidian-way)
walks through the whole setup in five steps.

## RAG & citations

**Retrieval-Augmented Generation** (RAG) means the AI first retrieves relevant passages
from your knowledge base, then answers using those passages — with citations back to the
source. It is the difference between a colleague who says "per the policy memo dated
March 3, section 2..." and one who says "I'm pretty sure it's fine."

For finance work the rule is simple: **no citation, no reliance.** An AI answer about
your data or your policy should point at the file it came from, the same way a workpaper
points at its support.

## The human reviewer

Nothing on this page removes the reviewer. It moves you *up* a level — from preparer to
reviewer of a very fast preparer:

1. **Control totals first.** Rows in, rows out, amounts tied. If they don't tie, stop.
2. **Exceptions second.** The agent's job is to shrink the review list, not hide it.
3. **Spot-check detail.** Sample the matched items, not just the flagged ones.
4. **Document the delegation.** The skill file + the agent's output *is* your audit trail.

## Where to go next

- Browse the [Skills Library]({{ '/skills/' | relative_url }}) and hand one to an agent this week.
- Read the [Analytics Map]({{ '/data-analytics/' | relative_url }}) — it is the thinking behind every skill.
- Follow the [Agent Tutorials]({{ '/tutorials/' | relative_url }}) and run your first skill this week.
- Compare notes in the [PANDAUDIT Discord]({{ '/community/' | relative_url }}) — Skill Swap channel.

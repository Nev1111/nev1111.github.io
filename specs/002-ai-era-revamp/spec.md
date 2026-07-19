# Feature Spec 002: PANDAUDIT AI-Era Revamp

**Status**: Approved for implementation
**Created**: 2026-07-19
**Site**: pandaudit.com (Jekyll / Beautiful Jekyll, GitHub Pages)
**Branch/Repo**: nev1111.github.io

## 1. Summary

PANDAUDIT currently reads as a well-styled "finance field guide" for data analytics, but
three things hold it back:

1. The **workflow sprint** sidebar widget is a static `25:00` decoration with no function.
2. The site's Python scripts and recipes predate the AI era — they are presented as blog
   posts to copy/paste, not as **skills** an AI agent (or a human using one) can execute.
3. Community and distribution are underpowered: the Discord invite is a single link, and
   there is no LinkedIn/social presence wired into the site.

This revamp turns PANDAUDIT into an **AI-native blog for finance and accounting
professionals**: every script becomes a `SKILL.md` document, a new AI Knowledge Base
explains the concepts (skills, agents, knowledge bases, RAG, prompts) in finance language,
the sprint timer becomes a real focus clock, and Discord + LinkedIn become first-class
growth channels.

**Hard constraint: the visual look and feel does not change.** Same theme, same
`pandaudit.css` design language (plot sidebar, waypoints, legs, cards, buttons), same
playful field-guide voice. New pages reuse existing components.

## 2. Goals

- G1: Give the sprint clock a genuine time-keeping purpose (usable focus timer).
- G2: Re-present all existing scripts/recipes as agent-ready `skills` in Markdown.
- G3: Teach AI concepts (knowledge bases, skills/.md files, agents, prompts, RAG) to a
  finance/accounting audience without dropping the existing analytics content.
- G4: Drive community growth via Discord and advertise via LinkedIn (and adjacent social).
- G5: Position the blog as "AI + analytics for finance" — exciting, current, practical.

## 3. Non-Goals

- No visual redesign, no theme change, no new color palette.
- No backend/server components (site remains static GitHub Pages).
- No paid features, auth, or gated content.
- No deletion of existing analytics content — it is repackaged, not removed.

## 4. Functional Requirements

### FR-1: Functional Workflow Sprint Timer

The sidebar `workflow sprint` block keeps its exact current appearance (label, monospace
clock, prompt text, two buttons) but becomes a working tool:

- FR-1.1: Clicking the clock starts a real 25:00 countdown; clicking again pauses;
  double-click (or a small reset affordance) resets to 25:00.
- FR-1.2: Timer state (remaining seconds, running flag, started-at timestamp) persists in
  `localStorage` so it survives page navigation within the site.
- FR-1.3: Each sprint displays a rotating **sprint mission** drawn from a small JS list of
  finance-flavored prompts (e.g. "Define the source, rule, exception, and output for one
  recurring task", "Convert one recipe you use into a SKILL.md draft", "Write the control
  total check for your close workbook"). The prompt rotates on reset/completion.
- FR-1.4: On completion (0:00), the clock flashes/announces "sprint complete" (CSS class
  toggle only — no new visual language) and suggests posting the result to Discord.
- FR-1.5: Implemented as a small vanilla-JS file `assets/js/sprint-timer.js`, included
  from the base layout. No frameworks. Degrades gracefully to today's static display if
  JS is disabled.

### FR-2: Skills Library (scripts → SKILL.md)

- FR-2.1: New Jekyll collection `_skills` with permalink `/skills/:name/` and an index
  page `/skills/` styled like the existing recipes/blog pages (legs + cards).
- FR-2.2: Each existing script-bearing post in `archived_posts/` and `_posts/` that
  contains reusable Python/pandas logic is converted into a skill document following the
  agent-skills convention:

  ```markdown
  ---
  name: clean-trailing-negative-amounts
  description: Convert legacy amounts like "1,234.56-" or "1,234CR" into clean numerics
  layout: skill
  category: cleaning        # cleaning | reconciliation | summarization | testing | export
  tools: pandas
  ---
  ## When to use this skill
  ## Inputs it expects
  ## Steps
  ## Code
  ## Validation (control totals)
  ## Exceptions to surface
  ```

- FR-2.3: Every skill page includes: (a) a "copy as SKILL.md" code block containing the
  raw markdown so a reader can drop it into their own agent setup (Claude Code
  `.claude/skills/`, ChatGPT custom instructions, etc.), (b) a plain-human "run it
  yourself" section preserving the original script, (c) a Discord CTA.
- FR-2.4: Initial library: at least 12 skills converted from the strongest existing
  posts (amount cleaning, merge_asof matching, duplicates, fiscal periods, groupby/
  transform, pivot/melt reshaping, string normalization, master-data mapping, multi-year
  consolidation, legacy report parsing, nested-IF replacement, workpaper export).
- FR-2.5: The recipes page links each recipe answer to its corresponding skill where one
  exists.

### FR-3: AI Knowledge Base page

- FR-3.1: New page `/ai/` ("AI Field Kit" in nav) explaining, in PANDAUDIT's voice and
  with finance examples: AI knowledge bases, `.md` skill files, agents, prompts/context,
  RAG and source citation, and where a human reviewer stays in the loop (controls,
  professional skepticism, review sign-off).
- FR-3.2: Structured with the existing waypoint/legs components (no new CSS).
- FR-3.3: Cross-links: each concept links to the Skills Library and to at least one blog
  post; the Analytics Map gains a final waypoint "Hand the route to an agent" linking
  to `/ai/`.

### FR-4: Community (Discord) integration

- FR-4.1: Keep invite `discord.gg/hDQKM6ar` as the single canonical invite URL, defined
  once in `_config.yml` and referenced via `site.social-network-links.discord`.
- FR-4.2: Community page gains an AI-era channel map (e.g. "Skill Swap" — share your
  SKILL.md files; "Agent Test Kitchen" — show what your agent did with a skill) alongside
  the existing channels.
- FR-4.3: Discord CTA appears on: sprint completion (FR-1.4), every skill page footer
  (FR-2.3), the AI page, and blog post footers.
- FR-4.4: If GitHub Pages allows (pure iframe embed), add the Discord server widget
  `<iframe src="https://discord.com/widget?id=...">` to the community page; if the server
  ID is unavailable, ship the CTA-only version and leave a TODO comment.

### FR-5: LinkedIn & social distribution

- FR-5.1: Enable LinkedIn in `_config.yml` social links (footer icons) once the profile
  URL is confirmed; wire `rss: true` so the feed is advertised.
- FR-5.2: Add share links (LinkedIn, X, copy-link) to the post layout and skill layout —
  plain anchor `https://www.linkedin.com/sharing/share-offsite/?url=...` style, styled as
  existing `sprint-button`-class buttons; no third-party JS.
- FR-5.3: Growth Lab (`/advertise/`) page updated with a concrete AI-era distribution
  plan: LinkedIn posting cadence tied to new skills ("1 skill = 1 LinkedIn post"),
  Discord weekly challenge, and cross-posting checklist.
- FR-5.4: Ensure OpenGraph/meta tags render correct titles/descriptions for skills so
  LinkedIn shares preview well (Beautiful Jekyll already emits OG tags; verify for the
  new collection).

### FR-6: Blog & homepage repositioning

- FR-6.1: Homepage keeps the current hero design but updates copy to lead with
  "analytics + AI skills for finance" and adds a route card for the Skills Library and
  AI Field Kit.
- FR-6.2: Sidebar nav gains "Skills Library" and "AI Field Kit" waypoints (renumbering
  existing waypoints is fine; component unchanged).
- FR-6.3: Three new launch blog posts (in existing field-notes voice, ~500 words each):
  1. "Your spreadsheet scripts are now skills" — announcing the Skills Library.
  2. "What an AI knowledge base means for accountants" — teaching post.
  3. "A 25-minute sprint that actually counts down" — timer + workflow framing.
- FR-6.4: Existing posts and archived posts remain accessible; nothing is deleted.

## 5. Technical Notes

- Jekyll collection config: `collections: { skills: { output: true, permalink: /skills/:name/ } }`
  plus a `skill` layout deriving from `page.html`.
- Timer JS is the only new JavaScript; it must not touch `beautifuljekyll.js`.
- All new pages use existing CSS classes (`legs`, `pandaudit-card-grid`, `pandaudit-button`,
  `timer`, `sprint-button`); any strictly-necessary new rules are appended to
  `pandaudit.css` and reuse existing custom properties.
- Build must pass with the pinned Gemfile (`bundle exec jekyll build`) with zero new gems.

## 6. Acceptance Criteria

- [ ] Sprint clock counts down, pauses, resets, persists across pages, rotates missions.
- [ ] `/skills/` lists ≥12 skills; each renders frontmatter + copyable SKILL.md block.
- [ ] `/ai/` explains knowledge bases, skills, agents, prompts, RAG with finance examples.
- [ ] Discord invite appears via config on community, skills, AI, and post pages.
- [ ] LinkedIn share button present on posts and skills; social links configured.
- [ ] Homepage and sidebar expose the new sections; visual design unchanged.
- [ ] Three launch posts published; existing content untouched.
- [ ] `bundle exec jekyll build` succeeds; spot-check key pages in `_site/`.

## 7. Out-of-Scope / Follow-ups

- Discord bot automation (existing `discord_bot/` folder) — separate effort.
- Newsletter, analytics/tracking, and paid promotion.
- Converting the remaining long-tail archived posts into skills (do incrementally,
  one LinkedIn post per new skill).

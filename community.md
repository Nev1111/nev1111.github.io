---
layout: page
title: Community Workshop
subtitle: Bring the finance data problem you actually have
permalink: /community/
eyebrow: discord + spreadsheet rescue
---

PANDAUDIT is building a fun, practical workshop for finance people who want better workflows without the jargon.

The site is the field guide. Discord is the workshop table.

<p><a href="https://discord.gg/{{ site.social-network-links.discord }}" class="pandaudit-button" target="_blank" rel="noopener">Join the PANDAUDIT Discord</a></p>

{% if site.discord-server-id != "" %}
<div class="pandaudit-discord-widget">
  <iframe src="https://discord.com/widget?id={{ site.discord-server-id }}&theme=light"
          width="100%" height="420" frameborder="0" loading="lazy"
          sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"
          title="PANDAUDIT Discord — who's online"></iframe>
</div>
{% endif %}

## Good questions to bring

- “I get this export every month. What should I check first?”
- “These two reports never agree. How should I bucket the exceptions?”
- “This dashboard breaks because the source file is messy. What cleanup rules do I need?”
- “How do I document the review so my manager trusts it?”
- “What would a repeatable version of this workbook look like?”

Please remove confidential information before sharing examples.

## Channels to use

<div class="legs" markdown="1">

[**#spreadsheets**{: .leg-name} **01**{: .leg-no} <span class="leg-desc">Messy files, recurring manual work, export cleanup</span>](https://discord.gg/{{ site.social-network-links.discord }})

[**#reconciliations**{: .leg-name} **02**{: .leg-no} <span class="leg-desc">Matches, breaks, timing differences, exception reports</span>](https://discord.gg/{{ site.social-network-links.discord }})

[**#workpapers**{: .leg-name} **03**{: .leg-no} <span class="leg-desc">Review-ready summaries, detail, controls, notes</span>](https://discord.gg/{{ site.social-network-links.discord }})

[**#skills**{: .leg-name} **04**{: .leg-no} <span class="leg-desc">Share results from running a skill, and request new ones</span>](https://discord.gg/{{ site.social-network-links.discord }})

[**#agents**{: .leg-name} **05**{: .leg-no} <span class="leg-desc">Show what your AI agent did — wins and disasters both welcome</span>](https://discord.gg/{{ site.social-network-links.discord }})

</div>

## Weekly challenge

> What is one finance task you repeated this week that felt like it should have a map — or a skill your AI agent could run?

The best community questions become future [recipes]({{ '/recipes/' | relative_url }}), [skills]({{ '/skills/' | relative_url }}), and field notes.

## New here?

- Followed a [tutorial]({{ '/tutorials/' | relative_url }}) and ran your first skill? Post how it went in #skills.
- Built or broke something with a skill from the [Skills Library]({{ '/skills/' | relative_url }})? #agents wants the details.
- Have a manual process that should become a skill? Describe it in #skills or email [hello@pandaudit.com](mailto:hello@pandaudit.com) and I'll build it.
- New to agents and knowledge bases? Skim the [AI Field Kit]({{ '/ai/' | relative_url }}) first, then ask anything.

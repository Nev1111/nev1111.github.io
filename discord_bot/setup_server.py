"""One-shot PANDAUDIT Discord server setup.

Redesigns the server to mirror pandaudit.com: Start Here / Workshop / AI Lab /
Community categories, seeded welcome + channel guide messages, and enables the
server widget used by the site's community page.

Usage:
    DISCORD_BOT_TOKEN=... python3 setup_server.py

Idempotent: existing categories/channels with matching names are reused, never
duplicated. Nothing is deleted — leftover channels are listed at the end so a
human can decide what to remove.
"""
import os
import sys
import time

import requests

API = "https://discord.com/api/v10"
GUILD_ID = "1391419177792962752"  # Pandaudit Community
SITE = "https://pandaudit.com"
INVITE = "https://discord.gg/6WmytaGJam"

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    sys.exit("Set DISCORD_BOT_TOKEN in the environment.")

S = requests.Session()
S.headers.update({"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"})


def call(method, path, **kwargs):
    r = S.request(method, f"{API}{path}", **kwargs)
    if r.status_code == 429:
        time.sleep(float(r.json().get("retry_after", 2)) + 0.5)
        r = S.request(method, f"{API}{path}", **kwargs)
    if not r.ok:
        sys.exit(f"{method} {path} -> {r.status_code}: {r.text[:300]}")
    return r.json() if r.text else {}


# --- the blueprint: mirrors the site's community page -----------------------

STRUCTURE = [
    ("📌 START HERE", [
        ("welcome", "Read this first: what PANDAUDIT is and how this server works.", True),
        ("introductions", "Who you are, what you do in finance, and the recurring task you'd most like to never do manually again.", False),
    ]),
    ("🛠️ THE WORKSHOP", [
        ("spreadsheet-rescue", "Messy files, recurring manual work, export cleanup. Sanitize before sharing!", False),
        ("reconciliation-room", "Matches, breaks, timing differences, exception reports.", False),
        ("dashboard-ingredients", "Data quality before reporting and visualization.", False),
        ("boss-level-workpapers", "Review-ready summaries, detail, controls, and notes.", False),
    ]),
    ("🤖 AI LAB", [
        ("skill-swap", f"Share your SKILL.md files and improve the Skills Library: {SITE}/skills/", False),
        ("agent-test-kitchen", "Show what your AI agent did with a skill — wins AND disasters welcome.", False),
    ]),
    ("☕ COMMUNITY", [
        ("general", "Everything else: careers, tools, finance life.", False),
        ("wins", "Before/afters and small victories. Tied out on the first run? Post it.", False),
    ]),
]

WELCOME = f"""**Welcome to the PANDAUDIT community!** 🐼

This is the workshop table for [pandaudit.com]({SITE}) — practical data analytics and AI skills for people in accounting, audit, and FP&A.

**How it works**
🛠️ **The Workshop** — bring the finance data problem you actually have. Messy exports to #spreadsheet-rescue, breaks to #reconciliation-room, pre-dashboard cleanup to #dashboard-ingredients, review packaging to #boss-level-workpapers.
🤖 **AI Lab** — #skill-swap is for sharing and improving `SKILL.md` files from the [Skills Library]({SITE}/skills/); #agent-test-kitchen is show-and-tell for what your AI agent did with one.
☕ **Community** — say hi in #introductions, celebrate in #wins.

**Three rules**
1. **Sanitize everything.** No real names, accounts, or amounts from your employer.
2. **Bring the control total.** "It looks right" is not a tie-out.
3. **Be kind to beginners.** Everyone's first reconciliation was a disaster.

New to AI skills and agents? Start with the [tutorials]({SITE}/tutorials/)."""

SEEDS = {
    "skill-swap": f"""**What goes here** 📄

A *skill* is a markdown procedure an AI agent can run — when to use it, inputs, steps, code, and the control totals that prove it worked. The library lives at {SITE}/skills/

**Post format that works well:**
1. The task ("monthly AP export cleanup")
2. Your SKILL.md (file or gist link)
3. What you'd like improved

Ran a library skill and it broke on your data? That's gold — post the error and we'll fix the skill for everyone.""",
    "agent-test-kitchen": f"""**Show your agent's work** 🧑‍🍳

Handed a skill to Claude, ChatGPT, or a coding agent? Post the results — screenshots welcome:
• what you asked for (the exact prompt)
• what it produced
• did the control totals tie?
• the weirdest thing it did

Disasters are more educational than wins. Never followed the tutorial? Start here: {SITE}/tutorials/""",
    "introductions": "Tell us three things: what you do, the tool you live in (Excel? SAP? a haunted Access database?), and the one recurring task you'd pay to never do manually again. 👇",
}


def main():
    me = call("GET", "/users/@me")
    print(f"Authenticated as bot: {me['username']}")

    existing = call("GET", f"/guilds/{GUILD_ID}/channels")
    by_name = {}
    for ch in existing:
        by_name.setdefault((ch["type"], ch["name"].lower()), ch)

    created_ids = set()
    for cat_name, channels in STRUCTURE:
        cat = by_name.get((4, cat_name.lower()))
        if not cat:
            cat = call("POST", f"/guilds/{GUILD_ID}/channels",
                       json={"name": cat_name, "type": 4})
            print(f"created category {cat_name}")
        created_ids.add(cat["id"])
        for name, topic, readonly in channels:
            ch = by_name.get((0, name))
            payload = {"name": name, "type": 0, "topic": topic, "parent_id": cat["id"]}
            if readonly:
                payload["permission_overwrites"] = [
                    {"id": GUILD_ID, "type": 0, "deny": "2048"}  # @everyone: no send
                ]
            if not ch:
                ch = call("POST", f"/guilds/{GUILD_ID}/channels", json=payload)
                print(f"  created #{name}")
            else:
                call("PATCH", f"/channels/{ch['id']}", json=payload)
                print(f"  updated #{name}")
            created_ids.add(ch["id"])
            seed = WELCOME if name == "welcome" else SEEDS.get(name)
            if seed and not ch.get("last_message_id"):
                msg = call("POST", f"/channels/{ch['id']}/messages", json={"content": seed})
                call("PUT", f"/channels/{ch['id']}/pins/{msg['id']}")
                print(f"    seeded + pinned message in #{name}")
            time.sleep(0.4)

    widget_channel = next((c["id"] for c in call("GET", f"/guilds/{GUILD_ID}/channels")
                           if c["name"] == "welcome"), None)
    call("PATCH", f"/guilds/{GUILD_ID}/widget",
         json={"enabled": True, "channel_id": widget_channel})
    print("Server widget: ENABLED (site community page will now show it)")

    leftovers = [c for c in existing if c["id"] not in created_ids]
    if leftovers:
        print("\nPre-existing channels not part of the new design (left untouched):")
        for c in leftovers:
            kind = {0: "text", 2: "voice", 4: "category"}.get(c["type"], c["type"])
            print(f"  - {c['name']} ({kind})")
        print("Delete any of these manually if no longer wanted.")

    print("\nDone. Check the server!")


if __name__ == "__main__":
    main()

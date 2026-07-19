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


def call(method, path, fatal=True, **kwargs):
    r = S.request(method, f"{API}{path}", **kwargs)
    if r.status_code == 429:
        time.sleep(float(r.json().get("retry_after", 2)) + 0.5)
        r = S.request(method, f"{API}{path}", **kwargs)
    if not r.ok:
        msg = f"{method} {path} -> {r.status_code}: {r.text[:300]}"
        if fatal:
            sys.exit(msg)
        print(f"  warning (continuing): {msg}")
        return None
    return r.json() if r.text else {}


# --- the blueprint: mirrors the site's community page -----------------------

STRUCTURE = [
    ("START HERE", [
        ("welcome", "What this server is and where things go.", True),
        ("introductions", "Say hi: what you do, and the recurring task you'd most like to stop doing by hand.", False),
    ]),
    ("THE WORKSHOP", [
        ("spreadsheets", "Messy files, recurring manual work, export cleanup. Remove confidential data before posting.", False),
        ("reconciliations", "Matching, breaks, timing differences, exception reports.", False),
        ("dashboards", "Data quality before reporting and visualization.", False),
        ("workpapers", "Packaging work for review: summaries, detail, controls, notes.", False),
    ]),
    ("SKILLS & AGENTS", [
        ("skills", f"Questions, results, and requests for the skills at {SITE}/skills/", False),
        ("agents", "What happened when you handed a skill to an AI — wins and failures both.", False),
    ]),
    ("COMMUNITY", [
        ("general", "Everything else: careers, tools, finance life.", False),
        ("wins", "Small victories and before/afters.", False),
    ]),
]

WELCOME = f"""Welcome to PANDAUDIT.

This server is the workshop behind {SITE} — a place for people in accounting, audit, and FP&A to get help turning manual spreadsheet work into repeatable workflows, with or without an AI agent.

Where things go:
#spreadsheets — messy files and export cleanup
#reconciliations — matching, breaks, exception reports
#dashboards — data quality before reporting
#workpapers — packaging work for review
#skills — questions, results, and requests for the skills at {SITE}/skills/
#agents — what happened when you handed a skill to an AI

House rules: remove confidential data before posting, show your control totals, and be patient with beginners.

If you tried a skill, post how it went — good or bad. If you want a skill that doesn't exist yet, ask in #skills."""

SEEDS = {
    "skills": f"""A skill is a written procedure (a markdown file) that an AI agent can follow — inputs, steps, code, and the checks that prove the output ties. The library is at {SITE}/skills/

If you ran one: post what you asked for, what you got, and whether the totals tied.
If one broke on your data: post the error. That's how the skills get better.
If you want one that doesn't exist yet: describe the task and it can be built.""",
    "agents": f"""Handed a skill to Claude, ChatGPT, or a coding agent? Post what happened — the prompt, the output, whether the totals tied, and anything odd it did along the way. Failures are as useful as wins.

If you haven't tried yet, the walkthrough is at {SITE}/tutorials/""",
    "introductions": "Say hi — what you do, what tools you work in, and the one recurring task you'd most like to stop doing by hand.",
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
                    {"id": GUILD_ID, "type": 0, "deny": "2048"},   # @everyone: no send
                    {"id": me["id"], "type": 1, "allow": "11264"},  # the bot: view + send + manage msgs
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
                if msg and call("PUT", f"/channels/{ch['id']}/messages/pins/{msg['id']}",
                                fatal=False) is not None:
                    print(f"    seeded + pinned message in #{name}")
                elif msg:
                    print(f"    seeded #{name} (pin skipped)")
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

"""Rename PANDAUDIT Discord categories/channels to plain, emoji-free names
and rewrite the bot's pinned seed messages in a plainer voice.

Usage:
    DISCORD_BOT_TOKEN=... python3 humanize_server.py

Safe to re-run: channels already renamed are skipped, and pinned messages are
only edited if they belong to the bot.
"""
import os
import sys
import time

import requests

from setup_server import SEEDS, WELCOME  # single source of truth for copy

API = "https://discord.com/api/v10"
GUILD_ID = "1391419177792962752"  # Pandaudit Community

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    sys.exit("Set DISCORD_BOT_TOKEN in the environment.")

S = requests.Session()
S.headers.update({"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"})

# old name (lowercase) -> new name
CATEGORY_RENAMES = {
    "📌 start here": "START HERE",
    "🛠️ the workshop": "THE WORKSHOP",
    "🤖 ai lab": "SKILLS & AGENTS",
    "☕ community": "COMMUNITY",
}
CHANNEL_RENAMES = {
    "spreadsheet-rescue": "spreadsheets",
    "reconciliation-room": "reconciliations",
    "dashboard-ingredients": "dashboards",
    "boss-level-workpapers": "workpapers",
    "skill-swap": "skills",
    "agent-test-kitchen": "agents",
}
NEW_TOPICS = {
    "welcome": "What this server is and where things go.",
    "introductions": "Say hi: what you do, and the recurring task you'd most like to stop doing by hand.",
    "spreadsheets": "Messy files, recurring manual work, export cleanup. Remove confidential data before posting.",
    "reconciliations": "Matching, breaks, timing differences, exception reports.",
    "dashboards": "Data quality before reporting and visualization.",
    "workpapers": "Packaging work for review: summaries, detail, controls, notes.",
    "skills": "Questions, results, and requests for the skills at https://pandaudit.com/skills/",
    "agents": "What happened when you handed a skill to an AI — wins and failures both.",
    "general": "Everything else: careers, tools, finance life.",
    "wins": "Small victories and before/afters.",
}
# channel (new name) -> replacement pinned text
NEW_PINS = {"welcome": WELCOME, **SEEDS}


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


def main():
    me = call("GET", "/users/@me")
    print(f"Authenticated as bot: {me['username']}")

    channels = call("GET", f"/guilds/{GUILD_ID}/channels")

    for ch in channels:
        if ch["type"] == 4:  # category
            new = CATEGORY_RENAMES.get(ch["name"].lower().strip())
            if new and ch["name"] != new:
                call("PATCH", f"/channels/{ch['id']}", json={"name": new}, fatal=False)
                print(f"category: {ch['name']!r} -> {new!r}")
                time.sleep(0.4)
        elif ch["type"] == 0:  # text channel
            new = CHANNEL_RENAMES.get(ch["name"].lower())
            payload = {}
            if new and ch["name"] != new:
                payload["name"] = new
            topic = NEW_TOPICS.get(new or ch["name"].lower())
            if topic and ch.get("topic") != topic:
                payload["topic"] = topic
            if payload:
                call("PATCH", f"/channels/{ch['id']}", json=payload, fatal=False)
                print(f"channel: #{ch['name']} -> #{new or ch['name']} (topic updated)")
                time.sleep(0.4)

    # refresh listing after renames, then rewrite the bot's pinned seed messages
    channels = call("GET", f"/guilds/{GUILD_ID}/channels")
    for ch in channels:
        if ch["type"] != 0:
            continue
        text = NEW_PINS.get(ch["name"].lower())
        if not text:
            continue
        pins = call("GET", f"/channels/{ch['id']}/pins", fatal=False) or []
        for msg in pins:
            if msg["author"]["id"] == me["id"] and msg["content"] != text:
                call("PATCH", f"/channels/{ch['id']}/messages/{msg['id']}",
                     json={"content": text}, fatal=False)
                print(f"rewrote pinned message in #{ch['name']}")
                time.sleep(0.4)

    print("\nDone. Check the server — names and pins should now be emoji-free.")


if __name__ == "__main__":
    main()

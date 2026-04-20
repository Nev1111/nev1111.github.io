# Discord Integration Setup Guide

This guide will help you set up complete Discord integration for PANDAUDIT, including automatic blog notifications and a comprehensive community bot.

## Overview

The Discord integration is a **two-part system**:

### Part 1: Webhook Integration (Automatic Blog Notifications)
1. **GitHub Actions Workflow** - Automatically detects new blog posts
2. **Discord Webhook** - Sends formatted notifications to #blog-updates channel
3. **Engaging Embeds** - Beautiful, rich notifications with calls-to-action

### Part 2: Discord Bot (Community Management)
1. **Moderation Tools** - Kick, ban, mute, warn, and manage messages
2. **Community Features** - Welcome messages, auto-reactions, engagement
3. **Information Commands** - Help, about, stats, and more
4. **24/7 Availability** - Hosted on cloud platform for always-on operation

## Complete Documentation Set

This is part of a comprehensive Discord integration suite. For detailed information, see:

- **[DISCORD_SETUP.md](./DISCORD_SETUP.md)** (this file) - Overview and webhook setup
- **[DISCORD_BOT_SETUP.md](./DISCORD_BOT_SETUP.md)** - Complete bot deployment guide with hosting options
- **[DISCORD_SERVER_GUIDE.md](./DISCORD_SERVER_GUIDE.md)** - Server structure, channels, roles, and community management
- **[discord_bot/README.md](./discord_bot/README.md)** - Quick start guide for the bot

## Quick Navigation

**Setting up for the first time?**
1. Start with [Part 1: Webhook Setup](#-part-1-webhook-setup-automatic-blog-notifications) (this file)
2. Then follow [DISCORD_BOT_SETUP.md](./DISCORD_BOT_SETUP.md) for bot deployment
3. Finally, use [DISCORD_SERVER_GUIDE.md](./DISCORD_SERVER_GUIDE.md) to optimize your server

**Already have webhook working?**
- Jump to [DISCORD_BOT_SETUP.md](./DISCORD_BOT_SETUP.md) to add bot functionality

**Need server structure advice?**
- Check out [DISCORD_SERVER_GUIDE.md](./DISCORD_SERVER_GUIDE.md)

---

# Part 1: Webhook Setup (Automatic Blog Notifications)

## Quick Setup (5 Minutes)

### Step 1: Create Discord Server (if you don't have one)

1. Open Discord
2. Click the `+` button on the left sidebar
3. Select "Create My Own"
4. Choose "For a club or community"
5. Name your server: **"PANDAUDIT Community"** (or your choice)
6. Click "Create"

### Step 2: Set Up Discord Channels

Create the following channels in your server:

- **#announcements** - Blog post notifications (read-only for members)
- **#general** - General discussion
- **#help** - Python and coding help
- **#showcase** - Members share their automation wins
- **#resources** - Helpful links and materials
- **#bugs-and-issues** - Report problems

**Optional channels:**
- **#excel-hell** - Excel horror stories
- **#introductions** - New member introductions
- **#wins** - Celebrate successes

### Step 3: Create Discord Webhook

1. In your Discord server, go to **Server Settings** (click server name → Server Settings)
2. Navigate to **Integrations** (left sidebar)
3. Click **Webhooks**
4. Click **New Webhook**
5. Configure the webhook:
 - **Name:** `PANDAUDIT Blog Bot`
 - **Channel:** Select `#announcements` (or your preferred channel)
 - **Avatar:** Upload your PANDAUDIT logo (optional)
6. Click **Copy Webhook URL** - **SAVE THIS!** You'll need it in the next step

** IMPORTANT:** Keep your webhook URL secret! Anyone with this URL can post to your Discord channel.

### Step 4: Add Webhook to GitHub Secrets

1. Go to your GitHub repository: https://github.com/nev1111/nev1111.github.io
2. Click **Settings** (top menu)
3. Navigate to **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. Configure the secret:
 - **Name:** `DISCORD_WEBHOOK_URL`
 - **Value:** Paste the webhook URL you copied in Step 3
6. Click **Add secret**

### Step 5: Test the Integration

1. Create a test blog post or modify an existing one
2. Commit and push to the `master` or `main` branch:
 ```bash
 git add _posts/your-post.md
 git commit -m "Test Discord integration"
 git push origin master
 ```
3. Go to **Actions** tab in your GitHub repository
4. Watch the "Discord New Post Notification" workflow run
5. Check your Discord `#announcements` channel - you should see a notification! 

If it doesn't work, see the **Troubleshooting** section below.

---

## Customizing Discord Notifications

### Change Notification Style

Edit `.github/workflows/discord-notify.yml` to customize the embed:

```yaml
# Change embed color (decimal format)
"color": 51455, # Blue (0x00C8FF)
# Other colors:
# 16711680 = Red (0xFF0000)
# 65280 = Green (0x00FF00)
# 16776960 = Yellow (0xFFFF00)

# Customize footer
"footer": {
 "text": "Your Custom Text",
 "icon_url": "https://your-site.com/logo.png"
}
```

### Add Mentions

To mention `@everyone` or a role when a post is published:

```yaml
# In the JSON_PAYLOAD, change the "content" field:
"content": "@everyone **New Blog Post Published!** ",
# OR
"content": "<@&ROLE_ID> **New Blog Post Published!** ",
```

**To get Role ID:**
1. Discord → Server Settings → Roles
2. Right-click on role → Copy ID
3. Enable Developer Mode first: Settings → Advanced → Developer Mode

### Notify Only for Certain Tags

Modify the workflow to filter by tags:

```bash
# In discord-notify.yml, add after extracting tags:
if [[ "$TAGS" == *"featured"* ]]; then
 # Send notification only if post has "featured" tag
 curl -H "Content-Type: application/json" ...
fi
```

---

## Setting Up Discussion Features

### Enable Discord Forum Threads (Recommended)

1. Create a **Forum Channel** called `#blog-discussions`
2. For each new post, the bot can create a thread automatically
3. Members can discuss each post in dedicated threads

**Advanced Setup** (requires custom bot):
- Create a Discord bot with `CREATE_MESSAGES` and `CREATE_THREADS` permissions
- Use bot to automatically create forum threads for each post
- Link threads back to blog posts

### Invite Link for Blog Readers

1. Discord → Server Settings → Invites
2. Create an invite link:
 - **Expire after:** Never
 - **Max uses:** No limit
 - **Grant temporary membership:** Off
3. Copy the invite link: `https://discord.gg/YOUR_CODE`
4. Update `_config.yml`:
 ```yaml
 social-network-links:
 discord: "YOUR_CODE" # Just the code part (e.g., "hDQKM6ar")
 ```

---

## Security Best Practices

### Protect Your Webhook

1. **Never commit webhook URLs to Git!** Always use GitHub Secrets
2. **Regenerate webhook if exposed:** Server Settings → Integrations → Webhooks → Edit → Reset Webhook Token
3. **Use different webhooks for testing and production**

### Rate Limiting

Discord webhooks have rate limits:
- **5 requests per 2 seconds per webhook**
- **30 requests per minute per webhook**

The workflow includes a 2-second delay between posts to avoid rate limiting.

### Webhook Security Settings

In Discord, you can:
- Delete webhook if compromised
- Change channel destination
- Monitor webhook usage (see activity log)

---

## Community Engagement Strategies

### Welcome New Members

Create a welcome message template in `#introductions`:

```
Welcome to PANDAUDIT Community! 

We're a community of finance & accounting professionals learning Python to automate Excel workflows.

 **Get Started:**
- Check out the latest posts: https://pandaudit.com/blog
- Ask questions in #help
- Share your automation wins in #showcase

 **Guidelines:**
- Be respectful and helpful
- No spam or self-promotion
- Share code snippets when asking for help

Happy automating! 
```

### Weekly Challenges

Post weekly challenges in `#general`:

**Example:**
```
 Weekly Challenge: Automate a Pivot Table

This week's challenge: Take an Excel file with monthly sales data and create a pivot table using pandas.

 Deadline: Sunday
 Prize: Featured in next week's showcase post!

Post your solution in this thread! 
```

### Highlight Member Solutions

Create a `#member-spotlight` channel featuring:
- Best solutions to challenges
- Interesting use cases shared by members
- Unique automation workflows

### Host Office Hours

Schedule weekly "office hours" in voice channels:
- Live Q&A sessions
- Code review sessions
- Pair programming
- Screen-sharing for troubleshooting

---

## Monitoring Engagement

### Discord Analytics

Track server growth:
1. Server Settings → Analytics
2. Monitor:
 - New members per week
 - Messages per channel
 - Active members

### GitHub Actions Logs

Monitor notification delivery:
1. Repository → Actions tab
2. Click on workflow runs
3. Check for errors or failed notifications

---

## Troubleshooting

### Notifications Not Appearing

**Check 1: Is the workflow running?**
- Go to Actions tab in GitHub
- Look for "Discord New Post Notification" workflow
- Check if it's being triggered

**Check 2: Is the secret set correctly?**
- GitHub → Settings → Secrets and variables → Actions
- Verify `DISCORD_WEBHOOK_URL` exists
- Make sure there are no extra spaces or quotes

**Check 3: Is the webhook valid?**
- Test the webhook manually:
 ```bash
 curl -H "Content-Type: application/json" \
 -d '{"content": "Test message"}' \
 YOUR_WEBHOOK_URL
 ```
- You should see the message in Discord immediately

**Check 4: Check workflow logs**
- Actions tab → Click on failed/completed run
- Look for error messages
- Common issues:
 - Invalid JSON format
 - Webhook URL expired/deleted
 - Rate limiting

### Webhook Deleted or Expired

1. Discord → Server Settings → Integrations → Webhooks
2. Create new webhook (follow Step 3 above)
3. Update GitHub secret with new URL

### Notifications Delayed

GitHub Actions can have delays during high load periods. Typical delay: 1-5 minutes.

---

## Advanced Customization

### Custom Bot (Alternative to Webhooks)

For more control, create a custom Discord bot:

**Pros:**
- Create forum threads automatically
- Respond to user commands
- Track engagement metrics
- Cross-post to multiple channels

**Cons:**
- More complex setup
- Requires hosting (or use serverless)

**Quick Start:**
1. Discord Developer Portal → New Application
2. Bot tab → Add Bot
3. Copy bot token → Add to GitHub Secrets as `DISCORD_BOT_TOKEN`
4. Modify workflow to use bot API instead of webhooks

### Embed Rich Content

Add images, thumbnails, and fields to embeds:

```json
{
 "embeds": [{
 "title": "New Post Title",
 "description": "Post description",
 "thumbnail": {
 "url": "https://pandaudit.com/assets/img/post-thumbnail.png"
 },
 "image": {
 "url": "https://pandaudit.com/assets/img/post-hero.png"
 },
 "fields": [
 {"name": "Author", "value": "PANDAUDIT Team", "inline": true},
 {"name": "Read Time", "value": "5 min", "inline": true}
 ]
 }]
}
```

---

# Part 2: Discord Bot Setup (Community Management)

## Why Add a Bot?

While webhooks handle automatic blog notifications, a dedicated bot provides:

### \ud83d\udee1\ufe0f **Moderation Tools**
- Kick, ban, and mute problematic users
- Delete messages in bulk
- Issue warnings and track violations
- Automated timeout management

### \ud83c\udf89 **Community Engagement**
- Welcome new members automatically
- Auto-react to posts in #blog-updates
- Provide help commands and information
- Display server statistics

### \ud83d\udcca **Analytics & Monitoring**
- Track server activity
- Monitor bot uptime
- Log moderation actions
- Generate community insights

## \ud83d\ude80 Quick Bot Setup

The PANDAUDIT Discord bot is already created and ready to deploy!

### Step 1: Bot Overview

Your bot includes:
- **Moderation**: `!kick`, `!ban`, `!mute`, `!unmute`, `!warn`, `!clear`
- **General**: `!help`, `!about`, `!latest`, `!ping`, `!invite`, `!stats`
- **Community**: Welcome messages, auto-reactions, rich embeds

All code is in the `discord_bot/` directory of this repository.

### Step 2: Deploy Your Bot

**For detailed deployment instructions, see [DISCORD_BOT_SETUP.md](./DISCORD_BOT_SETUP.md)**

Quick summary:

1. **Get Bot Token**:
 - Discord Developer Portal → Create Application → Bot tab
 - Copy bot token
 - Token already configured: `MTQ1OTIxNTk1ODg3ODA2MDYzNQ.GHa50Q.9Ryxa4qyhiF9bmhQCJts7i5Rryv6jLSwtghBGM`

2. **Choose Hosting**:
 - **Railway** (recommended): Free tier, auto-deploy from GitHub
 - **Replit**: Quick testing, free
 - **Heroku**: Professional, $5-7/mo
 - **VPS**: Full control, $5-10/mo

3. **Deploy**:
 ```bash
 cd discord_bot
 pip install -r requirements.txt
 cp .env.example .env
 # Add your bot token to .env
 python bot.py
 ```

4. **Invite to Server**:
 - Use OAuth2 URL Generator
 - Permissions integer: `1099511689222`
 - Authorize to your PANDAUDIT server

### Step 3: Test Bot

In Discord, try:
- `!ping` - Check bot is online
- `!help` - See all commands
- `!about` - View PANDAUDIT information

Bot should auto-react to messages in #blog-updates with 

### Step 4: Configure Roles

**Important**: Bot must be positioned ABOVE roles it moderates!

1. Server Settings → Roles
2. Drag "PANDAUDIT Bot" role above "Member" and "Moderator" roles
3. Ensure bot has these permissions:
 - Kick Members
 - Ban Members
 - Manage Messages
 - Manage Roles

## Full Documentation

For comprehensive bot setup, including:
- Creating bot application
- All hosting options with step-by-step guides
- Environment configuration
- Troubleshooting common issues
- Maintenance and updates

**See: [DISCORD_BOT_SETUP.md](./DISCORD_BOT_SETUP.md)**

## \ufe0f Server Structure

Need help organizing your Discord server?

**See: [DISCORD_SERVER_GUIDE.md](./DISCORD_SERVER_GUIDE.md)** for:
- Recommended channel structure
- Role configuration
- Permission templates
- Community guidelines
- Moderation strategies
- Engagement tactics
- Growth strategies

---

# Integration Testing

## \u2705 Webhook Test

1. **Create or edit a blog post** in `_posts/`
2. **Commit and push** to master/main branch
3. **Check GitHub Actions**: Should run "Discord New Post Notification" workflow
4. **Check Discord**: New post should appear in #blog-updates

**Expected result**:
```
 New Insights from PANDAUDIT! 

Fresh content alert! Check out our latest analysis on data analytics and automation.

 [Your Post Title]
[Post description/excerpt]

 Ready to level up your data analytics skills? Dive into this comprehensive guide.

 Topics Covered
#tag1 #tag2 #tag3

 What You'll Learn
Practical tips, real-world examples, and actionable insights for finance professionals

 Read the Full Article
[Click here to read now ]
 Share your thoughts and questions in this channel after reading!
```

## \u2705 Bot Test

1. **Check bot is online**: Green circle next to bot name
2. **Test basic command**: Type `!ping`
 - Expected: Bot responds with latency
3. **Test help**: Type `!help`
 - Expected: Bot shows command list
4. **Test auto-reactions**: Post in #blog-updates
 - Expected: Bot adds reactions
5. **Test welcome**: Have someone join server
 - Expected: Bot posts welcome message
6. **Test moderation** (with test user):
 - `!warn @testuser test` - Should issue warning
 - `!mute @testuser 1m test` - Should mute for 1 minute

## \ud83d\udc1b Troubleshooting Integration

### Webhook Not Working

**Issue**: Blog posts published but no Discord notification

**Solutions**:
1. Check GitHub Actions logs:
 - Repo → Actions → Check workflow run
2. Verify secret is set:
 - Repo → Settings → Secrets and variables → Actions
 - Should see `DISCORD_WEBHOOK_URL`
3. Test webhook manually:
 ```bash
 curl -H "Content-Type: application/json" \
 -d '{"content": "Test from PANDAUDIT"}' \
 https://discord.com/api/webhooks/1459221471455870997/cRD-CGI3gBojnsvSiW4Rz1jUGbFGsdyNi0-TApY63-AAL9DtuDqryA10zWqKh0hkCS73
 ```
4. Check webhook is valid:
 - Discord → Server Settings → Integrations → Webhooks
 - Should see "PANDAUDIT Blog Bot"

### Bot Not Responding

**Issue**: Bot shows online but doesn't respond to commands

**Solutions**:
1. Check Message Content Intent:
 - Discord Developer Portal → Bot tab
 - Enable "Message Content Intent"
2. Check bot permissions:
 - Right-click bot → Verify has "Read Messages" and "Send Messages"
3. Check logs:
 - Railway: Dashboard → Logs
 - Heroku: `heroku logs --tail`
 - VPS: `journalctl -u pandaudit-bot -f`
4. Verify bot token:
 - Regenerate if necessary
 - Update .env file
 - Restart bot

### Both Webhook and Bot Working, but...

**Issue**: Want to customize notifications or add features

**Webhook Customization**:
- Edit `.github/workflows/discord-notify.yml`
- Modify embed color, content, fields
- See workflow file for comments

**Bot Customization**:
- Edit `discord_bot/bot.py`
- Add new commands with `@bot.command()` decorator
- Modify existing commands
- See `discord_bot/README.md` for details

---

## Resources

### Official Documentation

- [Discord Webhooks Guide](https://discord.com/developers/docs/resources/webhook)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Discord API Reference](https://discord.com/developers/docs/intro)

### Community Resources

- [Discord.js Guide](https://discordjs.guide/) - For building custom bots
- [Discord Embed Visualizer](https://leovoel.github.io/embed-visualizer/) - Preview embeds
- [Webhook Tester](https://webhook.site/) - Test webhooks safely

---

## Need Help?

### Common Questions

**Q: Can I post to multiple channels?** 
A: Yes! Create multiple webhooks (one per channel) and modify the workflow to send to multiple URLs.

**Q: How do I add emoji to notifications?** 
A: Use Unicode emoji directly in JSON: `"content": " New Post!"` or Discord custom emoji: `:custom_emoji_name:`

**Q: Can I edit notifications after posting?** 
A: Yes, with a bot (not webhooks). Bots can edit/delete their own messages.

**Q: How do I prevent duplicate notifications?** 
A: The workflow only triggers on new/modified files. Editing old posts won't trigger new notifications (unless you push changes to that file).

### Getting Support

- **GitHub Issues:** https://github.com/nev1111/nev1111.github.io/issues
- **Email:** hello@pandaudit.com
- **Discord:** (your community server)

---

## Checklist

Use this checklist to ensure everything is set up correctly:

- [ ] Discord server created
- [ ] Channels organized (#announcements, #general, #help, etc.)
- [ ] Webhook created and URL copied
- [ ] GitHub secret `DISCORD_WEBHOOK_URL` added
- [ ] Test notification sent successfully
- [ ] Invite link generated and added to _config.yml
- [ ] Welcome message created
- [ ] Community guidelines posted
- [ ] Moderators assigned (if applicable)
- [ ] Analytics tracking enabled

---

** Congratulations!** Your Discord integration is now live. Every time you publish a new blog post, your community will be notified automatically.

Happy community building! 

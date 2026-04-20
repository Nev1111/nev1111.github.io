# PANDAUDIT Discord Bot

A comprehensive Discord bot for the PANDAUDIT community featuring moderation tools, community engagement features, and automated blog post notifications.

## Features

### Moderation Commands
- `!kick @user [reason]` - Kick a user from the server
- `!ban @user [reason]` - Ban a user from the server
- `!mute @user [duration] [reason]` - Temporarily mute a user (e.g., 10m, 1h, 1d)
- `!unmute @user` - Unmute a user
- `!clear [number]` - Delete multiple messages (default 10, max 100)
- `!warn @user [reason]` - Issue a warning to a user
- `!warnings @user` - View all warnings for a user

### - General Commands
- `!help [command]` - Show all commands or help for a specific command
- `!about` - Learn about PANDAUDIT and its mission
- `!latest` - Get a link to the latest blog post
- `!ping` - Check bot status and latency
- `!invite` - Get the pandaudit.com website link
- `!stats` - Show server statistics

### Community Features
- **Welcome Messages** - Automatically greets new members with helpful information
- **Auto-Reactions** - Adds reactions ( - ) to posts in #blog-updates
- **Rich Embeds** - Beautiful, informative message formatting
- **Comprehensive Logging** - Tracks all moderation actions
- **Error Handling** - User-friendly error messages

## Quick Start

### Prerequisites
- Python 3.8 or higher
- A Discord bot application (see [Setup Guide](#-setup-guide) below)
- Discord server with appropriate permissions

### Installation

1. **Clone or navigate to the repository:**
 ```bash
 cd discord_bot
 ```

2. **Install dependencies:**
 ```bash
 pip install -r requirements.txt
 ```

3. **Configure environment variables:**
 ```bash
 cp .env.example .env
 # Edit .env and add your DISCORD_BOT_TOKEN
 ```

4. **Run the bot:**
 ```bash
 python bot.py
 ```

## Setup Guide

### Step 1: Create Discord Bot Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Name it "PANDAUDIT Bot" and click **Create**
4. Navigate to the **Bot** tab (left sidebar)
5. Click **Add Bot** → **Yes, do it!**
6. **Important**: Under "Privileged Gateway Intents", enable:
 - Server Members Intent
 - Message Content Intent
7. Click **Reset Token** and copy your bot token
8. Save this token securely - you'll need it for the `.env` file

### Step 2: Configure Bot Permissions

Your bot needs these permissions:
- Read Messages/View Channels
- Send Messages
- Manage Messages
- Embed Links
- Attach Files
- Read Message History
- Add Reactions
- Kick Members (for moderation)
- Ban Members (for moderation)
- Manage Roles (for muting)

**Permission Integer**: `1099511689222`

### Step 3: Invite Bot to Your Server

1. In Discord Developer Portal, go to **OAuth2** → **URL Generator**
2. Select scopes:
 - `bot`
 - `applications.commands` (for future slash commands)
3. Select permissions (or use integer `1099511689222`)
4. Copy the generated URL and open it in your browser
5. Select your server and click **Authorize**

### Step 4: Configure and Run

1. **Create `.env` file:**
 ```bash
 cp .env.example .env
 nano .env # or use your preferred editor
 ```

2. **Add your bot token:**
 ```env
 DISCORD_BOT_TOKEN=MTQ1OTIxNTk1ODg3ODA2MDYzNQ.GHa50Q.9Ryxa4qyhiF9bmhQCJts7i5Rryv6jLSwtghBGM
 ```

3. **Run the bot:**
 ```bash
 python bot.py
 ```

4. **Verify it's working:**
 - Check the console for "Bot is ready!" message
 - In Discord, type `!ping` - the bot should respond
 - Try `!help` to see all commands

## Hosting Options

### Option 1: Replit (Easiest - Free)

1. Create account at [Replit](https://replit.com)
2. Create new Python Repl
3. Upload bot files
4. Add `DISCORD_BOT_TOKEN` to Secrets (lock icon)
5. Click "Run"
6. Use [UptimeRobot](https://uptimerobot.com) to keep it online 24/7

**Pros**: Free, easy setup, no credit card
**Cons**: Bot may sleep after inactivity

### Option 2: Railway (Recommended - Free with limits)

1. Sign up at [Railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Add environment variable: `DISCORD_BOT_TOKEN`
4. Deploy automatically from your repo
5. Free $5 credit per month

**Pros**: Always online, auto-deploys, professional
**Cons**: May need to add credit card after free tier

### Option 3: Heroku (Popular)

1. Create account at [Heroku](https://heroku.com)
2. Install Heroku CLI
3. Create `Procfile`:
 ```
 worker: python bot.py
 ```
4. Create `runtime.txt`:
 ```
 python-3.11.0
 ```
5. Deploy:
 ```bash
 heroku create pandaudit-bot
 heroku config:set DISCORD_BOT_TOKEN=your_token
 git push heroku main
 heroku ps:scale worker=1
 ```

**Pros**: Reliable, popular, good documentation
**Cons**: Requires credit card, free tier limited

### Option 4: VPS (Most Control)

Use any VPS provider (DigitalOcean, Linode, AWS, etc.):

1. **Setup server:**
 ```bash
 apt update && apt upgrade -y
 apt install python3 python3-pip git -y
 ```

2. **Clone and setup:**
 ```bash
 git clone https://github.com/nev1111/nev1111.github.io.git
 cd nev1111.github.io/discord_bot
 pip3 install -r requirements.txt
 ```

3. **Create systemd service** (`/etc/systemd/system/pandaudit-bot.service`):
 ```ini
 [Unit]
 Description=PANDAUDIT Discord Bot
 After=network.target

 [Service]
 Type=simple
 User=ubuntu
 WorkingDirectory=/home/ubuntu/nev1111.github.io/discord_bot
 Environment="DISCORD_BOT_TOKEN=your_token_here"
 ExecStart=/usr/bin/python3 bot.py
 Restart=always
 RestartSec=10

 [Install]
 WantedBy=multi-user.target
 ```

4. **Start service:**
 ```bash
 systemctl daemon-reload
 systemctl enable pandaudit-bot
 systemctl start pandaudit-bot
 systemctl status pandaudit-bot
 ```

**Pros**: Full control, always online, can host other services
**Cons**: Costs $5-10/month, requires maintenance

### Option 5: Local Machine (Testing Only)

**For development/testing only - not recommended for production:**

```bash
python bot.py
# Keep terminal open
```

**Pros**: Free, immediate testing
**Cons**: Bot offline when computer is off

## Configuration

### Environment Variables

Edit `.env` file:

```env
# Required
DISCORD_BOT_TOKEN=your_bot_token_here

# Optional
BOT_PREFIX=!
BOT_STATUS=pandaudit.com | !help
LOG_LEVEL=INFO
```

### Custom Configuration

Edit `config.py` to customize:
- Channel names
- Colors
- Moderation settings
- Auto-reaction settings
- Website URLs

## Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Keep bot token secret** - Regenerate if exposed
3. **Use environment variables** - Never hardcode tokens
4. **Regular updates** - Keep `discord.py` updated
5. **Limit permissions** - Only grant necessary permissions
6. **Monitor logs** - Check `bot.log` regularly

## Troubleshooting

### Bot doesn't start

**Check 1: Token is correct**
```bash
cat .env # Verify token is set correctly
```

**Check 2: Dependencies installed**
```bash
pip install -r requirements.txt --upgrade
```

**Check 3: Intents enabled**
- Discord Developer Portal → Bot → Privileged Gateway Intents
- Enable "Server Members Intent" and "Message Content Intent"

### Bot is online but doesn't respond

**Check 1: Permissions**
- Right-click bot in member list → Verify it has proper roles
- Check channel permissions

**Check 2: Message Content Intent**
- Bot needs this to read command messages
- Enable in Discord Developer Portal

**Check 3: Prefix is correct**
- Default is `!`
- Try `!ping` to test

### Commands don't work

**Check error messages:**
```bash
tail -f bot.log # View real-time logs
```

**Common issues:**
- Missing permissions: Bot needs "Manage Messages", "Kick Members", etc.
- Invalid arguments: Use `!help <command>` for correct usage
- Rate limiting: Wait a few seconds between commands

### Moderation commands fail

**Check bot role hierarchy:**
1. Discord Server Settings → Roles
2. Drag bot role ABOVE roles you want to moderate
3. Bot cannot moderate users with higher/equal roles

### Bot goes offline

**If hosting locally:**
- Use a VPS or cloud hosting service instead

**If on Replit:**
- Use UptimeRobot to ping your bot every 5 minutes

**If on Railway/Heroku:**
- Check logs in dashboard
- Verify dyno/service is running

## Monitoring

### View Logs

```bash
# Real-time logs
tail -f bot.log

# Last 50 lines
tail -n 50 bot.log

# Search for errors
grep ERROR bot.log
```

### Bot Status

In Discord:
- `!ping` - Check if bot is responding
- `!stats` - View server statistics

### System Monitoring (VPS)

```bash
# Check if bot is running
systemctl status pandaudit-bot

# View service logs
journalctl -u pandaudit-bot -f

# Restart bot
systemctl restart pandaudit-bot
```

## Updates

### Update Bot Code

```bash
cd /path/to/discord_bot
git pull origin master
pip install -r requirements.txt --upgrade
python bot.py # or restart service
```

### Update discord.py

```bash
pip install discord.py --upgrade
```

## Resources

### Official Documentation
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [Discord.py Guide](https://discordpy.readthedocs.io/en/stable/)

### Community Resources
- [Discord.py Discord Server](https://discord.gg/dpy)
- [Discord API Discord Server](https://discord.gg/discord-api)
- [Discord Developers](https://discord.com/developers/docs/intro)

### Helpful Tools
- [Discord Permissions Calculator](https://discordapi.com/permissions.html)
- [Discord Embed Visualizer](https://leovoel.github.io/embed-visualizer/)
- [Uptime Robot](https://uptimerobot.com) - Keep bot online

## 🆘 Support

### Need Help?

1. **Check the logs**: `bot.log` contains detailed information
2. **Read the docs**: Most issues are covered in documentation
3. **GitHub Issues**: [Create an issue](https://github.com/nev1111/nev1111.github.io/issues)
4. **Discord Community**: Ask in your PANDAUDIT Discord server

### Common Questions

**Q: Can I customize the welcome message?**
A: Yes! Edit the `on_member_join` function in `bot.py`

**Q: How do I add new commands?**
A: Add a new function decorated with `@bot.command()` in `bot.py`

**Q: Can I use slash commands instead of `!` prefix?**
A: Yes! discord.py supports application commands. Check the [documentation](https://discordpy.readthedocs.io/en/stable/interactions/api.html)

**Q: How do I persist warnings across restarts?**
A: Use a database (SQLite, PostgreSQL, etc.). See commented code in `bot.py` for database setup hints.

**Q: Can the bot create forum threads automatically?**
A: Yes! You'll need to implement thread creation logic. See [Thread documentation](https://discordpy.readthedocs.io/en/stable/api.html#discord.Thread)

## License

This bot is part of the PANDAUDIT project. Feel free to modify and adapt it for your community!

## Credits

Built with:
- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- Python 3.8+
- Love for data analytics and automation 

---

**Happy botting! **

For more information, visit [pandaudit.com](https://pandaudit.com)

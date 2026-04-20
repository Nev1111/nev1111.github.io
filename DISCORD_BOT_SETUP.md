# PANDAUDIT Discord Bot Setup & Deployment Guide

Complete guide to setting up, configuring, and hosting the PANDAUDIT Discord bot.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#-prerequisites)
3. [Initial Setup](#-initial-setup)
4. [Configuration](#-configuration)
5. [Hosting Options](#-hosting-options)
6. [Deployment Guide](#-deployment-guide)
7. [Testing](#-testing)
8. [Maintenance](#-maintenance)
9. [Troubleshooting](#-troubleshooting)

---

## Overview

The PANDAUDIT Discord bot is a comprehensive community management tool featuring:

### Features
- **Moderation**: Kick, ban, mute, warn users, and manage messages
- **Community**: Welcome messages, auto-reactions, engagement tools
- **Information**: Bot status, server stats, help commands
- **Integration**: Connects with pandaudit.com ecosystem

### Technical Stack
- **Language**: Python 3.8+
- **Framework**: discord.py 2.3.2+
- **Dependencies**: See `discord_bot/requirements.txt`
- **Storage**: In-memory (warnings/mutes) - can be extended with database

---

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 128MB minimum (512MB recommended)
- **Storage**: 50MB for bot + dependencies
- **Network**: Internet connection with access to Discord API

### Accounts Needed
1. **Discord Account** - To create bot application
2. **Hosting Account** - Choose from:
 - Replit (free)
 - Railway (free tier)
 - Heroku (requires credit card)
 - VPS (DigitalOcean, Linode, AWS, etc.)

### Skills Required
- Basic command line/terminal knowledge
- Understanding of environment variables
- Basic Git knowledge (for VPS deployment)

---

## Initial Setup

### Step 1: Create Discord Bot Application

1. **Go to Discord Developer Portal**
 - Visit: https://discord.com/developers/applications
 - Log in with your Discord account

2. **Create New Application**
 - Click **"New Application"** (top right)
 - Name: `PANDAUDIT Bot`
 - Click **"Create"**

3. **Configure General Information**
 - Add description: "Community bot for PANDAUDIT - Data Analytics & Automation"
 - Upload bot icon (optional): Use PANDAUDIT logo
 - Add tags: `analytics`, `community`, `moderation`

4. **Create Bot User**
 - Navigate to **"Bot"** tab (left sidebar)
 - Click **"Add Bot"**
 - Click **"Yes, do it!"** to confirm

5. **Configure Bot Settings**
 - **Username**: `PANDAUDIT` (or your preference)
 - **Icon**: Upload PANDAUDIT logo
 - **Public Bot**: Toggle OFF (private to your server only)
 - **Requires OAuth2 Code Grant**: Toggle OFF

6. **Enable Privileged Gateway Intents**
 
 **CRITICAL**: These must be enabled or bot won't work!
 
 Scroll down to **"Privileged Gateway Intents"**:
 - **Server Members Intent** - Toggle ON
 - **Presence Intent** - Toggle OFF (not needed)
 - **Message Content Intent** - Toggle ON
 
 Click **"Save Changes"**

7. **Get Your Bot Token**
 - Click **"Reset Token"** (if first time) or **"View Token"**
 - Click **"Copy"**
 - **SAVE THIS TOKEN SECURELY** - You'll need it later
 - **NEVER share this token publicly!**

### Step 2: Set Up Bot Permissions

1. **Navigate to OAuth2 → URL Generator**
 - Go to **"OAuth2"** tab (left sidebar)
 - Click **"URL Generator"**

2. **Select Scopes**
 - `bot`
 - `applications.commands` (for future slash commands)

3. **Select Bot Permissions**
 
 **General Permissions:**
 - Read Messages/View Channels
 - Send Messages
 - Send Messages in Threads
 - Embed Links
 - Attach Files
 - Read Message History
 - Add Reactions
 
 **Moderation Permissions:**
 - Manage Messages (for !clear command)
 - Kick Members (for !kick command)
 - Ban Members (for !ban command)
 - Manage Roles (for !mute command)
 - Manage Channels (to set muted role permissions)
 
 **Permission Integer**: `1099511689222`
 
 > **Tip**: You can paste this integer directly instead of clicking checkboxes

4. **Copy Generated URL**
 - Scroll down
 - Copy the generated URL
 - Save it - you'll use this to invite the bot

### Step 3: Invite Bot to Your Server

1. **Open Invite URL**
 - Paste the URL from Step 2 into your browser
 - Or use: `https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=1099511689222&scope=bot%20applications.commands`
 - Replace `YOUR_CLIENT_ID` with your Application ID (found in General Information)

2. **Select Server**
 - Choose your PANDAUDIT Discord server from dropdown
 - Click **"Continue"**

3. **Authorize Permissions**
 - Review the permissions list
 - Click **"Authorize"**
 - Complete CAPTCHA if prompted

4. **Verify Bot Joined**
 - Go to your Discord server
 - Bot should appear in member list (offline until you run it)
 - You should see a system message: "PANDAUDIT Bot joined the server"

### Step 4: Configure Bot Role Position

 **IMPORTANT**: Bot can only moderate users with roles BELOW its own role!

1. **Go to Server Settings → Roles**
 - Right-click server name → **"Server Settings"**
 - Click **"Roles"** (left sidebar)

2. **Position Bot Role**
 - Drag **"PANDAUDIT Bot"** role ABOVE roles you want to moderate
 - Example hierarchy:
 ```
 [Admin] <- Can't be moderated by bot
 [PANDAUDIT Bot] <- Bot role
 [Moderator] <- Can be moderated by bot
 [Member] <- Can be moderated by bot
 [everyone] <- Can be moderated by bot
 ```

3. **Save Changes**

---

## Configuration

### Step 1: Download Bot Files

**Option A: Clone from GitHub**
```bash
git clone https://github.com/nev1111/nev1111.github.io.git
cd nev1111.github.io/discord_bot
```

**Option B: Download ZIP**
1. Go to: https://github.com/nev1111/nev1111.github.io
2. Click **"Code"** → **"Download ZIP"**
3. Extract and navigate to `discord_bot/` folder

### Step 2: Install Dependencies

```bash
# Make sure you're in the discord_bot directory
cd discord_bot

# Install required packages
pip install -r requirements.txt

# Or with pip3 (if pip defaults to Python 2)
pip3 install -r requirements.txt
```

**Expected output:**
```
Collecting discord.py>=2.3.2
 Downloading discord.py-2.3.2-py3-none-any.whl
Collecting python-dotenv>=1.0.0
 Downloading python_dotenv-1.0.0-py3-none-any.whl
...
Successfully installed discord.py-2.3.2 python-dotenv-1.0.0 ...
```

### Step 3: Configure Environment Variables

1. **Create `.env` file**
 ```bash
 cp .env.example .env
 ```

2. **Edit `.env` file**
 ```bash
 nano .env # or use your preferred text editor
 ```

3. **Add your bot token**
 ```env
 # Required: Your Discord Bot Token
 DISCORD_BOT_TOKEN=MTQ1OTIxNTk1ODg3ODA2MDYzNQ.GHa50Q.9Ryxa4qyhiF9bmhQCJts7i5Rryv6jLSwtghBGM
 
 # Optional: Customize bot behavior
 BOT_PREFIX=!
 BOT_STATUS=pandaudit.com | !help
 LOG_LEVEL=INFO
 ```

4. **Save and exit**
 - Nano: `Ctrl+X`, `Y`, `Enter`
 - Vim: `Esc`, `:wq`, `Enter`

### Step 4: Test Bot Locally

```bash
python bot.py
# Or: python3 bot.py
```

**Expected output:**
```
2025-01-09 12:00:00 - pandaudit_bot - INFO - Starting PANDAUDIT Discord Bot...
2025-01-09 12:00:01 - pandaudit_bot - INFO - Bot logged in as PANDAUDIT Bot (ID: 1459215958878060635)
2025-01-09 12:00:01 - pandaudit_bot - INFO - Connected to 1 guild(s)
2025-01-09 12:00:01 - pandaudit_bot - INFO - Bot is ready!
```

**Verify in Discord:**
1. Bot should show as **online** (green circle)
2. Type `!ping` - bot should respond with latency
3. Type `!help` - bot should show command list

**If successful**: Bot is working! You can now proceed to hosting.

**If errors**: See [Troubleshooting](#-troubleshooting) section below.

---

## Hosting Options

Comparison of hosting platforms:

| Platform | Cost | Difficulty | Uptime | Best For |
|----------|------|------------|--------|----------|
| **Replit** | Free | Easy | 80% | Quick testing |
| **Railway** | Free tier | Medium | 99.9% | **Recommended** |
| **Heroku** | $7/mo | Medium | 99.9% | Professional |
| **VPS** | $5-10/mo | Hard | 99.9% | Full control |
| **Local** | Free | Easy | 50% | Development only |

**Recommendation**: **Railway** - Best balance of ease, reliability, and cost.

---

## Deployment Guide

### Option 1: Railway (Recommended)

**Why Railway?**
- Free $5 credit per month (enough for small bot)
- Always online (24/7 uptime)
- Automatic deployments from GitHub
- Easy environment variable management
- Simple setup, no credit card required initially

**Step-by-Step:**

1. **Sign Up for Railway**
 - Go to: https://railway.app
 - Click **"Start a New Project"**
 - Sign up with GitHub (recommended) or email

2. **Create New Project**
 - Click **"New Project"**
 - Select **"Deploy from GitHub repo"**
 - Authorize Railway to access your GitHub
 - Select repository: `nev1111/nev1111.github.io`

3. **Configure Deployment**
 - Railway will detect Python app automatically
 - Set **Root Directory**: `discord_bot`
 - Set **Start Command**: `python bot.py`

4. **Add Environment Variables**
 - Click on your project
 - Go to **"Variables"** tab
 - Click **"+ New Variable"**
 - Add:
 - **Name**: `DISCORD_BOT_TOKEN`
 - **Value**: Your bot token
 - Click **"Add"**

5. **Deploy**
 - Click **"Deploy"**
 - Wait for deployment (1-2 minutes)
 - Check logs for "Bot is ready!" message

6. **Verify**
 - Go to Discord server
 - Bot should be online
 - Test with `!ping`

**Auto-Deployment:**
- Every time you push to GitHub, Railway automatically redeploys
- No manual intervention needed!

**Monitoring:**
- View logs: Railway dashboard → Deployments → Logs
- Check metrics: Railway dashboard → Metrics

---

### Option 2: Replit (Easiest)

**Best for**: Quick setup, testing, learning

**Step-by-Step:**

1. **Create Replit Account**
 - Go to: https://replit.com
 - Sign up (free)

2. **Create New Repl**
 - Click **"+ Create Repl"**
 - Template: **"Python"**
 - Title: `PANDAUDIT-Discord-Bot`
 - Click **"Create Repl"**

3. **Upload Bot Files**
 - Click **"Upload file"** (in Files panel)
 - Upload all files from `discord_bot/` directory:
 - `bot.py`
 - `config.py`
 - `requirements.txt`
 - `.env.example`

4. **Configure Secrets**
 - Click **"Secrets"** (lock icon in left sidebar)
 - Click **"New secret"**
 - Key: `DISCORD_BOT_TOKEN`
 - Value: Your bot token
 - Click **"Add new secret"**

5. **Install Dependencies**
 - In Shell (bottom panel), run:
 ```bash
 pip install -r requirements.txt
 ```

6. **Run Bot**
 - Click **"Run"** (big green button at top)
 - Bot should start and show "Bot is ready!" in console

7. **Keep Bot Online 24/7** (Optional)
 - Replit bots sleep after 1 hour of inactivity
 - Use [UptimeRobot](https://uptimerobot.com) to keep it awake:
 1. Create UptimeRobot account
 2. Add new monitor (HTTP(s))
 3. Use your Repl URL
 4. Set interval: 5 minutes
 5. UptimeRobot will "ping" your bot every 5 minutes

**Note**: Replit has usage limits. For production, use Railway or VPS.

---

### Option 3: Heroku

**Best for**: Professional deployment with scaling

**Step-by-Step:**

1. **Sign Up for Heroku**
 - Go to: https://heroku.com
 - Create account (requires credit card, but won't charge for small bot)

2. **Install Heroku CLI**
 
 **MacOS:**
 ```bash
 brew install heroku/brew/heroku
 ```
 
 **Windows:**
 - Download from: https://devcenter.heroku.com/articles/heroku-cli
 
 **Linux:**
 ```bash
 curl https://cli-assets.heroku.com/install.sh | sh
 ```

3. **Login to Heroku**
 ```bash
 heroku login
 # Opens browser for authentication
 ```

4. **Prepare Bot for Heroku**
 
 Create `Procfile` in `discord_bot/` directory:
 ```bash
 echo "worker: python bot.py" > Procfile
 ```
 
 Create `runtime.txt` to specify Python version:
 ```bash
 echo "python-3.11.0" > runtime.txt
 ```

5. **Create Heroku App**
 ```bash
 cd discord_bot
 heroku create pandaudit-discord-bot
 ```

6. **Set Environment Variables**
 ```bash
 heroku config:set DISCORD_BOT_TOKEN="your_token_here"
 ```

7. **Deploy**
 ```bash
 git init # If not already a git repo
 git add .
 git commit -m "Initial bot deployment"
 git push heroku main
 ```

8. **Scale Worker**
 ```bash
 heroku ps:scale worker=1
 ```

9. **View Logs**
 ```bash
 heroku logs --tail
 ```

10. **Verify**
 - Check logs for "Bot is ready!"
 - Test in Discord with `!ping`

**Costs**:
- Eco Dynos: $5/month (1000 hours)
- Basic Dynos: $7/month (always on)

---

### Option 4: VPS (DigitalOcean, Linode, AWS, etc.)

**Best for**: Maximum control, hosting multiple services

**Prerequisites**:
- Basic Linux knowledge
- SSH access to server
- Server with Ubuntu 20.04+ or Debian 11+

**Step-by-Step:**

1. **Create Server**
 - Provider: DigitalOcean, Linode, Vultr, AWS EC2, etc.
 - OS: Ubuntu 22.04 LTS
 - Size: Basic ($5/month is sufficient)
 - Create and note IP address

2. **Connect to Server**
 ```bash
 ssh root@your_server_ip
 ```

3. **Update System**
 ```bash
 apt update && apt upgrade -y
 ```

4. **Install Python and Dependencies**
 ```bash
 apt install python3 python3-pip git -y
 ```

5. **Create Bot User** (security best practice)
 ```bash
 adduser --disabled-password --gecos "" pandaudit
 su - pandaudit
 ```

6. **Clone Repository**
 ```bash
 git clone https://github.com/nev1111/nev1111.github.io.git
 cd nev1111.github.io/discord_bot
 ```

7. **Install Python Dependencies**
 ```bash
 pip3 install -r requirements.txt
 ```

8. **Create `.env` File**
 ```bash
 cp .env.example .env
 nano .env
 # Add your DISCORD_BOT_TOKEN
 # Save: Ctrl+X, Y, Enter
 ```

9. **Test Bot**
 ```bash
 python3 bot.py
 # Should see "Bot is ready!"
 # Press Ctrl+C to stop
 ```

10. **Create Systemd Service** (for auto-start)
 
 Exit to root user:
 ```bash
 exit # Back to root
 ```
 
 Create service file:
 ```bash
 nano /etc/systemd/system/pandaudit-bot.service
 ```
 
 Paste this configuration:
 ```ini
 [Unit]
 Description=PANDAUDIT Discord Bot
 After=network.target
 
 [Service]
 Type=simple
 User=pandaudit
 WorkingDirectory=/home/pandaudit/nev1111.github.io/discord_bot
 Environment="DISCORD_BOT_TOKEN=YOUR_TOKEN_HERE"
 ExecStart=/usr/bin/python3 /home/pandaudit/nev1111.github.io/discord_bot/bot.py
 Restart=always
 RestartSec=10
 StandardOutput=append:/home/pandaudit/bot.log
 StandardError=append:/home/pandaudit/bot_error.log
 
 [Install]
 WantedBy=multi-user.target
 ```
 
 **Replace `YOUR_TOKEN_HERE` with your actual bot token**
 
 Save: `Ctrl+X`, `Y`, `Enter`

11. **Enable and Start Service**
 ```bash
 systemctl daemon-reload
 systemctl enable pandaudit-bot
 systemctl start pandaudit-bot
 ```

12. **Check Status**
 ```bash
 systemctl status pandaudit-bot
 ```
 
 Should show: **active (running)**

13. **View Logs**
 ```bash
 # Service logs
 journalctl -u pandaudit-bot -f
 
 # Or bot logs
 tail -f /home/pandaudit/bot.log
 ```

14. **Useful Commands**
 ```bash
 # Stop bot
 systemctl stop pandaudit-bot
 
 # Restart bot
 systemctl restart pandaudit-bot
 
 # View status
 systemctl status pandaudit-bot
 
 # Disable auto-start
 systemctl disable pandaudit-bot
 ```

**Security Hardening**:
```bash
# Set up firewall
ufw allow 22/tcp # SSH
ufw enable

# Disable root login
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd

# Set up automatic security updates
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades
```

**Updating Bot**:
```bash
su - pandaudit
cd nev1111.github.io
git pull origin master
cd discord_bot
pip3 install -r requirements.txt --upgrade
exit
systemctl restart pandaudit-bot
```

---

## Testing

### Basic Tests

1. **Bot Online Test**
 - Check bot shows as online in Discord
 - Green circle next to bot name

2. **Ping Test**
 ```
 !ping
 ```
 Expected: Bot responds with latency

3. **Help Test**
 ```
 !help
 ```
 Expected: Bot shows command list

4. **About Test**
 ```
 !about
 ```
 Expected: Bot shows PANDAUDIT information

### Moderation Tests

 **Create a test user or use an alternate account**

1. **Clear Test**
 ```
 !clear 5
 ```
 Expected: Deletes 5 messages

2. **Warn Test**
 ```
 !warn @testuser Testing warning system
 ```
 Expected: User receives warning

3. **Mute Test**
 ```
 !mute @testuser 1m Test mute
 ```
 Expected: User muted for 1 minute

4. **Unmute Test**
 ```
 !unmute @testuser
 ```
 Expected: User unmuted

### Community Feature Tests

1. **Welcome Message Test**
 - Have someone join the server
 - Expected: Bot sends welcome message

2. **Auto-Reaction Test**
 - Post a message in #blog-updates channel
 - Expected: Bot adds reactions ( )

3. **Stats Test**
 ```
 !stats
 ```
 Expected: Bot shows server statistics

### Load Testing

```bash
# Send multiple commands quickly
!ping
!ping
!ping
!help
!about
```

Expected: Bot responds to all commands without crashing

---

## Maintenance

### Regular Tasks

**Daily**:
- Monitor bot uptime
- Check for error messages in logs

**Weekly**:
- Review moderation logs
- Check disk space (VPS only)
- Verify bot is responding correctly

**Monthly**:
- Update dependencies
- Review and backup warning data
- Check hosting costs/usage

**Quarterly**:
- Update discord.py to latest version
- Review bot permissions
- Audit moderation logs

### Updating Bot

**Railway/Heroku**: Automatic from GitHub pushes

**VPS**:
```bash
cd /home/pandaudit/nev1111.github.io
git pull origin master
cd discord_bot
pip3 install -r requirements.txt --upgrade
sudo systemctl restart pandaudit-bot
```

**Replit**: Re-upload files or sync with GitHub

### Backup

**Configuration**:
```bash
# Backup .env file
cp .env .env.backup

# Or for VPS
scp root@your_server:/home/pandaudit/nev1111.github.io/discord_bot/.env ./env_backup
```

**Logs**:
```bash
# VPS
scp root@your_server:/home/pandaudit/bot.log ./bot_log_backup

# Railway/Heroku: Download from dashboard
```

### Monitoring

**Discord Status**:
- Use `!ping` periodically
- Monitor bot's online status

**Logs**:
```bash
# Railway: Dashboard → Logs
# Heroku: heroku logs --tail
# VPS: journalctl -u pandaudit-bot -f
```

**Uptime Monitoring** (Recommended):
1. Use [UptimeRobot](https://uptimerobot.com) or [Uptime.com](https://uptime.com)
2. Set up HTTP monitor (if bot has web endpoint)
3. Or use Discord webhook to send periodic heartbeat
4. Get alerts when bot goes down

---

## Troubleshooting

### Bot Won't Start

**Error**: `discord.errors.LoginFailure: Improper token has been passed.`

**Solution**:
- Verify token in `.env` file is correct
- No extra spaces or quotes
- Token should be exactly as copied from Discord Developer Portal
- Regenerate token if needed

**Error**: `discord.errors.PrivilegedIntentsRequired`

**Solution**:
1. Go to Discord Developer Portal
2. Your Application → Bot tab
3. Enable "Server Members Intent" and "Message Content Intent"
4. Save changes
5. Restart bot

**Error**: `ModuleNotFoundError: No module named 'discord'`

**Solution**:
```bash
pip install discord.py
# Or: pip3 install discord.py
```

### Bot Online But Doesn't Respond

**Issue**: Bot shows online but doesn't respond to commands

**Checks**:

1. **Message Content Intent**
 - Developer Portal → Bot → Enable "Message Content Intent"

2. **Permissions**
 - Right-click bot → Check role permissions
 - Bot needs "Read Messages" and "Send Messages"

3. **Channel Permissions**
 - Check channel-specific permissions
 - Bot may be denied in specific channels

4. **Prefix**
 - Make sure you're using correct prefix (default: `!`)
 - Try: `!help` not `/help`

5. **Check Logs**
 ```bash
 tail -f bot.log # Look for errors
 ```

### Moderation Commands Fail

**Error**: `Forbidden: Missing Permissions`

**Solution**:
1. **Check Bot Role Position**
 - Server Settings → Roles
 - Bot role must be ABOVE roles it moderates

2. **Check Permissions**
 - Bot needs:
 - Kick Members (for !kick)
 - Ban Members (for !ban)
 - Manage Roles (for !mute)
 - Manage Messages (for !clear)

3. **Bot Can't Moderate Admins**
 - Bot can't moderate users with roles above its own
 - Bot can't moderate server owner

### Mute Command Not Working

**Issue**: `!mute` command completes but user can still send messages

**Solution**:
1. Check "Muted" role permissions in each channel:
 - Right-click channel → Edit Channel → Permissions
 - Add "Muted" role
 - Deny "Send Messages" and "Speak" (voice)

2. Or let bot auto-create role:
 - Bot will create "Muted" role automatically
 - Bot will set permissions for all channels
 - Ensure bot has "Manage Channels" permission

### Bot Goes Offline Randomly

**Railway/Heroku**: Check logs for errors
```bash
railway logs
# Or: heroku logs --tail
```

**VPS**:
```bash
systemctl status pandaudit-bot
journalctl -u pandaudit-bot -n 50
```

**Common causes**:
- Network issues
- Rate limiting by Discord
- Uncaught exceptions
- Memory issues

**Solution**: Enable auto-restart
- VPS: Already configured in systemd service
- Railway/Heroku: Should auto-restart
- Replit: Use UptimeRobot

### High Memory Usage

**Issue**: Bot using too much RAM

**Checks**:
```bash
# Linux
ps aux | grep python
top -p $(pgrep -f bot.py)
```

**Solutions**:
- Implement database for warnings/mutes instead of in-memory storage
- Clear logs periodically
- Upgrade hosting plan

### Rate Limiting

**Error**: `discord.errors.HTTPException: 429 Too Many Requests`

**Solution**:
- Bot is sending too many requests to Discord
- Add delays between bulk operations
- Don't spam commands
- Implement command cooldowns

### Can't Find Logs

**Railway**: Dashboard → Deployments → Logs

**Heroku**:
```bash
heroku logs --tail -a pandaudit-discord-bot
```

**VPS**:
```bash
# Service logs
journalctl -u pandaudit-bot -f

# Bot logs
tail -f /home/pandaudit/bot.log

# Error logs 
tail -f /home/pandaudit/bot_error.log
```

**Replit**: Console panel at bottom of editor

---

## Additional Resources

### Documentation
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [Discord API Documentation](https://discord.com/developers/docs/intro)

### Community
- [discord.py Discord Server](https://discord.gg/dpy)
- [Discord Developers Discord](https://discord.gg/discord-developers)

### Tools
- [Discord Permissions Calculator](https://discordapi.com/permissions.html)
- [Discord Embed Visualizer](https://leovoel.github.io/embed-visualizer/)
- [UptimeRobot](https://uptimerobot.com) - Keep bot online

### Tutorials
- [discord.py Quickstart](https://discordpy.readthedocs.io/en/stable/quickstart.html)
- [Building Your First Discord Bot](https://realpython.com/how-to-make-a-discord-bot-python/)

---

## Support

Need help?

1. **Check Documentation**: Most issues covered in this guide
2. **Review Logs**: Errors usually point to the problem
3. **Discord Community**: Ask in your PANDAUDIT server
4. **GitHub Issues**: https://github.com/nev1111/nev1111.github.io/issues
5. **discord.py Support**: https://discord.gg/dpy

---

## Success Checklist

Before considering your bot deployment complete:

- [ ] Bot application created in Discord Developer Portal
- [ ] Bot token generated and saved securely
- [ ] Privileged intents enabled (Server Members, Message Content)
- [ ] Bot invited to server with correct permissions
- [ ] Bot role positioned above moderated roles
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `DISCORD_BOT_TOKEN`
- [ ] Bot tested locally and responds to `!ping`
- [ ] Hosting platform chosen and configured
- [ ] Bot deployed and running 24/7
- [ ] Welcome messages working
- [ ] Auto-reactions working in #blog-updates
- [ ] Moderation commands tested
- [ ] Logs accessible and monitoring set up
- [ ] Backup of configuration files created
- [ ] Team members trained on bot commands

---

** Congratulations!** Your PANDAUDIT Discord bot is now live and ready to engage your community.

For ongoing support and updates, visit [pandaudit.com](https://pandaudit.com) or check the [GitHub repository](https://github.com/nev1111/nev1111.github.io).

Happy community building! 

"""Configuration for PANDAUDIT Discord Bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
BOT_STATUS = os.getenv('BOT_STATUS', 'pandaudit.com | !help')

# Optional: Webhook for testing
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Database Configuration (if needed)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_data.db')

# Bot Settings
COMMAND_PREFIX = '!'
BOT_DESCRIPTION = 'PANDAUDIT Community Bot - Data Analytics & Automation'

# Channel Names (customize these based on your server)
CHANNEL_NAMES = {
    'blog_updates': 'blog-updates',
    'welcome': 'welcome',
    'general': 'general',
    'help': 'help',
    'showcase': 'showcase',
    'announcements': 'announcements'
}

# Colors (for embeds)
COLORS = {
    'primary': 0x5865F2,  # Discord Blurple
    'success': 0x57F287,  # Green
    'warning': 0xFEE75C,  # Yellow
    'error': 0xED4245,    # Red
    'info': 0x5865F2,     # Blue
}

# Moderation Settings
MAX_WARNINGS_BEFORE_KICK = 3
DEFAULT_MUTE_DURATION = '10m'
MAX_BULK_DELETE = 100

# Auto-moderation Settings
AUTO_REACT_CHANNELS = ['blog-updates']
AUTO_REACT_EMOJIS = ['👍', '💬', '🔖']

# Website URLs
WEBSITE_URL = 'https://pandaudit.com'
BLOG_URL = 'https://pandaudit.com/blog'
ABOUT_URL = 'https://pandaudit.com/aboutme'
CHEATSHEET_URL = 'https://pandaudit.com/cheatsheet'
STORIES_URL = 'https://pandaudit.com/stories'

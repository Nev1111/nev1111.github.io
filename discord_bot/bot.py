#!/usr/bin/env python3
"""
PANDAUDIT Discord Bot

A comprehensive Discord bot for the PANDAUDIT community with moderation,
general commands, and community engagement features.
"""

import discord
from discord.ext import commands
import os
import sys
import logging
import asyncio
from datetime import datetime, timedelta
import json
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('pandaudit_bot')

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    description='PANDAUDIT Community Bot - Data Analytics & Automation',
    help_command=commands.DefaultHelpCommand()
)

# Store warnings (in production, use a database)
warnings = {}

# Store muted users (in production, use a database)
muted_users = {}


# ============================================================================
# EVENT HANDLERS
# ============================================================================

@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'Bot logged in as {bot.user.name} (ID: {bot.user.id})')
    logger.info(f'Connected to {len(bot.guilds)} guild(s)')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="pandaudit.com | !help"
        )
    )
    logger.info('Bot is ready!')


@bot.event
async def on_member_join(member):
    """Welcome new members."""
    logger.info(f'New member joined: {member.name}')
    
    # Find general or welcome channel
    welcome_channels = ['welcome', 'general', 'introductions']
    channel = None
    
    for channel_name in welcome_channels:
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            break
    
    if channel:
        embed = discord.Embed(
            title=f"Welcome to PANDAUDIT Community! 👋",
            description=f"Hey {member.mention}, welcome to our community of data analytics enthusiasts!",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="🚀 Get Started",
            value="• Check out our latest posts at [pandaudit.com](https://pandaudit.com)\n"
                  "• Ask questions in the help channels\n"
                  "• Share your automation wins in #showcase",
            inline=False
        )
        embed.add_field(
            name="💡 Quick Commands",
            value="• `!help` - See all commands\n"
                  "• `!latest` - Get the latest blog post\n"
                  "• `!about` - Learn about PANDAUDIT",
            inline=False
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Happy learning! 🎉")
        
        await channel.send(embed=embed)


@bot.event
async def on_message(message):
    """Handle messages and auto-reactions."""
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Auto-react to messages in blog-updates channel
    if message.channel.name == 'blog-updates':
        try:
            await message.add_reaction('👍')
            await message.add_reaction('💬')
            await message.add_reaction('🔖')
            logger.info(f'Added reactions to message in {message.channel.name}')
        except Exception as e:
            logger.error(f'Failed to add reactions: {e}')
    
    # Process commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}\nUse `!help {ctx.command}` for usage.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Invalid argument provided. Use `!help {ctx.command}` for usage.")
    else:
        logger.error(f'Command error: {error}')
        await ctx.send("❌ An error occurred while processing the command.")


# ============================================================================
# MODERATION COMMANDS
# ============================================================================

@bot.command(name='kick', help='Kick a user from the server')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
    """Kick a user from the server."""
    try:
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"{member.mention} has been kicked from the server.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
        logger.info(f'{member.name} was kicked by {ctx.author.name}. Reason: {reason}')
    except Exception as e:
        await ctx.send(f"❌ Failed to kick member: {e}")
        logger.error(f'Failed to kick {member.name}: {e}')


@bot.command(name='ban', help='Ban a user from the server')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
    """Ban a user from the server."""
    try:
        await member.ban(reason=reason, delete_message_days=1)
        
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"{member.mention} has been banned from the server.",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
        logger.info(f'{member.name} was banned by {ctx.author.name}. Reason: {reason}')
    except Exception as e:
        await ctx.send(f"❌ Failed to ban member: {e}")
        logger.error(f'Failed to ban {member.name}: {e}')


@bot.command(name='mute', help='Mute a user for a specified duration')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, duration: Optional[str] = "10m", *, reason: Optional[str] = "No reason provided"):
    """Mute a user for a specified duration (e.g., 10m, 1h, 1d)."""
    try:
        # Parse duration
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        unit = duration[-1]
        
        if unit not in time_units:
            await ctx.send("❌ Invalid duration format. Use: 10s, 10m, 1h, or 1d")
            return
        
        amount = int(duration[:-1])
        seconds = amount * time_units[unit]
        
        # Create muted role if it doesn't exist
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted", reason="Auto-created muted role")
            
            # Set permissions for all channels
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        
        # Add muted role
        await member.add_roles(muted_role, reason=reason)
        
        # Store mute info
        unmute_time = datetime.utcnow() + timedelta(seconds=seconds)
        muted_users[member.id] = {
            'unmute_time': unmute_time,
            'role': muted_role,
            'guild_id': ctx.guild.id
        }
        
        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"{member.mention} has been muted.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Duration", value=duration, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
        logger.info(f'{member.name} was muted by {ctx.author.name} for {duration}. Reason: {reason}')
        
        # Schedule unmute
        await asyncio.sleep(seconds)
        if member.id in muted_users:
            await member.remove_roles(muted_role, reason="Mute duration expired")
            del muted_users[member.id]
            await ctx.send(f"🔊 {member.mention} has been automatically unmuted.")
            logger.info(f'{member.name} was automatically unmuted')
    
    except ValueError:
        await ctx.send("❌ Invalid duration format. Use: 10s, 10m, 1h, or 1d")
    except Exception as e:
        await ctx.send(f"❌ Failed to mute member: {e}")
        logger.error(f'Failed to mute {member.name}: {e}')


@bot.command(name='unmute', help='Unmute a user')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    """Unmute a user."""
    try:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role, reason=f"Unmuted by {ctx.author.name}")
            
            if member.id in muted_users:
                del muted_users[member.id]
            
            embed = discord.Embed(
                title="🔊 Member Unmuted",
                description=f"{member.mention} has been unmuted.",
                color=discord.Color.green()
            )
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            logger.info(f'{member.name} was unmuted by {ctx.author.name}')
        else:
            await ctx.send(f"❌ {member.mention} is not muted.")
    except Exception as e:
        await ctx.send(f"❌ Failed to unmute member: {e}")
        logger.error(f'Failed to unmute {member.name}: {e}')


@bot.command(name='clear', help='Delete a number of messages (default 10)')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: Optional[int] = 10):
    """Delete a specified number of messages from the channel."""
    try:
        if amount < 1 or amount > 100:
            await ctx.send("❌ Please specify a number between 1 and 100.")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
        
        msg = await ctx.send(f"🗑️ Deleted {len(deleted) - 1} message(s).")
        await asyncio.sleep(3)
        await msg.delete()
        
        logger.info(f'{ctx.author.name} deleted {len(deleted) - 1} messages in {ctx.channel.name}')
    except Exception as e:
        await ctx.send(f"❌ Failed to delete messages: {e}")
        logger.error(f'Failed to delete messages: {e}')


@bot.command(name='warn', help='Warn a user')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
    """Issue a warning to a user."""
    try:
        if member.id not in warnings:
            warnings[member.id] = []
        
        warning_data = {
            'reason': reason,
            'moderator': ctx.author.name,
            'timestamp': datetime.utcnow().isoformat()
        }
        warnings[member.id].append(warning_data)
        
        warning_count = len(warnings[member.id])
        
        embed = discord.Embed(
            title="⚠️ Warning Issued",
            description=f"{member.mention} has been warned.",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Warning Count", value=f"{warning_count}", inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
        
        # DM the user
        try:
            dm_embed = discord.Embed(
                title="⚠️ You've been warned",
                description=f"You received a warning in {ctx.guild.name}",
                color=discord.Color.yellow()
            )
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            dm_embed.add_field(name="Total Warnings", value=f"{warning_count}", inline=True)
            dm_embed.set_footer(text="Please follow the server rules to avoid further action.")
            
            await member.send(embed=dm_embed)
        except:
            await ctx.send("⚠️ Could not send DM to user.")
        
        logger.info(f'{member.name} was warned by {ctx.author.name}. Reason: {reason}')
    except Exception as e:
        await ctx.send(f"❌ Failed to warn member: {e}")
        logger.error(f'Failed to warn {member.name}: {e}')


@bot.command(name='warnings', help='View warnings for a user')
@commands.has_permissions(manage_messages=True)
async def view_warnings(ctx, member: discord.Member):
    """View all warnings for a user."""
    if member.id not in warnings or not warnings[member.id]:
        await ctx.send(f"✅ {member.mention} has no warnings.")
        return
    
    embed = discord.Embed(
        title=f"⚠️ Warnings for {member.name}",
        description=f"Total warnings: {len(warnings[member.id])}",
        color=discord.Color.yellow()
    )
    
    for i, warn in enumerate(warnings[member.id][-5:], 1):  # Show last 5 warnings
        embed.add_field(
            name=f"Warning {i}",
            value=f"**Reason:** {warn['reason']}\n**By:** {warn['moderator']}\n**Date:** {warn['timestamp'][:10]}",
            inline=False
        )
    
    await ctx.send(embed=embed)


# ============================================================================
# GENERAL COMMANDS
# ============================================================================

@bot.command(name='about', help='Learn about PANDAUDIT')
async def about(ctx):
    """Display information about PANDAUDIT."""
    embed = discord.Embed(
        title="📊 About PANDAUDIT",
        description="Empowering finance professionals with data analytics and automation.",
        color=discord.Color.blue(),
        url="https://pandaudit.com"
    )
    
    embed.add_field(
        name="🎯 Our Mission",
        value="We help accounting and finance professionals navigate the evolving "
              "data analytics landscape with practical guides, real-world examples, and actionable insights.",
        inline=False
    )
    
    embed.add_field(
        name="💡 What We Cover",
        value="• Data Analytics & Visualization\n"
              "• Process Automation\n"
              "• Modern Tools (Python, pandas, Excel)\n"
              "• Real-world Finance Use Cases\n"
              "• Career Development",
        inline=False
    )
    
    embed.add_field(
        name="🔗 Links",
        value="[Website](https://pandaudit.com) • [Blog](https://pandaudit.com/blog) • "
              "[Success Stories](https://pandaudit.com/stories) • [Quick Reference](https://pandaudit.com/cheatsheet)",
        inline=False
    )
    
    embed.set_thumbnail(url="https://pandaudit.com/assets/img/avatar-icon.png")
    embed.set_footer(text="Join our community of data-driven finance professionals!")
    
    await ctx.send(embed=embed)


@bot.command(name='latest', help='Get the latest blog post')
async def latest(ctx):
    """Fetch and display the latest blog post from pandaudit.com."""
    # In a real implementation, you'd scrape the website or use an API
    # For now, we'll provide a generic response with a link
    
    embed = discord.Embed(
        title="📰 Latest from PANDAUDIT",
        description="Check out our latest insights on data analytics and automation!",
        color=discord.Color.green(),
        url="https://pandaudit.com/blog"
    )
    
    embed.add_field(
        name="🔗 Visit Blog",
        value="[pandaudit.com/blog](https://pandaudit.com/blog)",
        inline=False
    )
    
    embed.add_field(
        name="📱 Stay Updated",
        value="New posts are automatically shared in #blog-updates!",
        inline=False
    )
    
    embed.set_footer(text="💬 Share your thoughts after reading!")
    
    await ctx.send(embed=embed)


@bot.command(name='ping', help='Check bot status and latency')
async def ping(ctx):
    """Display bot latency and status."""
    latency = round(bot.latency * 1000, 2)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description="Bot is online and responding.",
        color=discord.Color.green()
    )
    
    embed.add_field(name="⏱️ Latency", value=f"{latency}ms", inline=True)
    embed.add_field(name="📊 Status", value="✅ Online", inline=True)
    embed.add_field(name="🖥️ Servers", value=f"{len(bot.guilds)}", inline=True)
    
    embed.timestamp = datetime.utcnow()
    
    await ctx.send(embed=embed)


@bot.command(name='invite', help='Get the PANDAUDIT website link')
async def invite(ctx):
    """Share the PANDAUDIT website and community invite."""
    embed = discord.Embed(
        title="🔗 Join the PANDAUDIT Community",
        description="Connect with finance professionals exploring data analytics and automation.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🌐 Website",
        value="[pandaudit.com](https://pandaudit.com)",
        inline=False
    )
    
    embed.add_field(
        name="📝 Blog",
        value="[pandaudit.com/blog](https://pandaudit.com/blog)",
        inline=True
    )
    
    embed.add_field(
        name="📚 Resources",
        value="[Quick Reference](https://pandaudit.com/cheatsheet)",
        inline=True
    )
    
    embed.add_field(
        name="💡 Share This Server",
        value="Invite colleagues interested in data analytics to this Discord community!",
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name='help', help='Show all available commands')
async def help_command(ctx, command_name: Optional[str] = None):
    """Custom help command with better formatting."""
    if command_name:
        # Show help for specific command
        command = bot.get_command(command_name)
        if command:
            embed = discord.Embed(
                title=f"📖 Help: {command.name}",
                description=command.help or "No description available.",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Usage",
                value=f"`!{command.name} {command.signature}`",
                inline=False
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Command `{command_name}` not found.")
        return
    
    # Show all commands
    embed = discord.Embed(
        title="🤖 PANDAUDIT Bot Commands",
        description="Here are all available commands. Use `!help <command>` for detailed information.",
        color=discord.Color.blue()
    )
    
    # Moderation Commands
    mod_commands = [
        "**!kick** `@user [reason]` - Kick a user",
        "**!ban** `@user [reason]` - Ban a user",
        "**!mute** `@user [duration] [reason]` - Mute a user (e.g., 10m, 1h)",
        "**!unmute** `@user` - Unmute a user",
        "**!clear** `[number]` - Delete messages (default 10)",
        "**!warn** `@user [reason]` - Warn a user",
        "**!warnings** `@user` - View user's warnings"
    ]
    embed.add_field(
        name="🛡️ Moderation Commands",
        value="\n".join(mod_commands),
        inline=False
    )
    
    # General Commands
    gen_commands = [
        "**!help** `[command]` - Show this help message",
        "**!about** - Learn about PANDAUDIT",
        "**!latest** - Get the latest blog post",
        "**!ping** - Check bot status",
        "**!invite** - Get pandaudit.com link"
    ]
    embed.add_field(
        name="💬 General Commands",
        value="\n".join(gen_commands),
        inline=False
    )
    
    embed.add_field(
        name="🔗 Links",
        value="[Website](https://pandaudit.com) • [Blog](https://pandaudit.com/blog) • [Support](https://pandaudit.com/aboutme)",
        inline=False
    )
    
    embed.set_footer(text="PANDAUDIT Bot • Prefix: !")
    
    await ctx.send(embed=embed)


@bot.command(name='stats', help='Show server statistics')
async def stats(ctx):
    """Display server statistics."""
    guild = ctx.guild
    
    # Count members
    total_members = guild.member_count
    online_members = len([m for m in guild.members if m.status != discord.Status.offline])
    
    # Count channels
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    
    embed = discord.Embed(
        title=f"📊 {guild.name} Statistics",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="👥 Total Members", value=total_members, inline=True)
    embed.add_field(name="🟢 Online", value=online_members, inline=True)
    embed.add_field(name="📅 Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    
    embed.add_field(name="💬 Text Channels", value=text_channels, inline=True)
    embed.add_field(name="🔊 Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.timestamp = datetime.utcnow()
    
    await ctx.send(embed=embed)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point for the bot."""
    # Get bot token from environment variable
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        logger.error('DISCORD_BOT_TOKEN environment variable not set!')
        logger.error('Please set the token in your .env file or environment.')
        sys.exit(1)
    
    try:
        logger.info('Starting PANDAUDIT Discord Bot...')
        bot.run(token)
    except discord.LoginFailure:
        logger.error('Invalid bot token provided!')
        sys.exit(1)
    except Exception as e:
        logger.error(f'Failed to start bot: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()

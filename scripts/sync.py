import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("CORDIA_TOKEN")

# Intents for bot (you don't need to specify message_content here if just syncing)
intents = discord.Intents.default()

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

async def sync_commands():
    async with bot:
        print("Logging in and syncing commands...")
        # Login to Discord using the bot token
        await bot.login(TOKEN)
        
        # Sync the bot's slash commands globally
        synced_commands = await bot.tree.sync()

        # You can also sync commands for a specific guild
        # guild = discord.Object(id=your_guild_id)
        # synced_commands = await bot.tree.sync(guild=guild)

        print(f"Successfully synced {len(synced_commands)} commands.")
        
        # Close the bot after syncing
        await bot.close()

# Run the sync in an asyncio event loop
asyncio.run(sync_commands())

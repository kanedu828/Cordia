import os
import asyncio
import discord
from cordia.cordia_client import CordiaClient
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
# Set intents
intents = discord.Intents.default()
intents.message_content = False
intents.members = True

# Env variables
token = os.getenv("CORDIA_TOKEN")
psql_connection_string = os.getenv("CORDIA_DB_CONNECTION_STRING")
papertrail_address_number = os.getenv("CORDIA_PAPER_TRAIL_ADDRESS")

async def start():
    client = CordiaClient(
        psql_connection_string, int(papertrail_address_number), intents=intents, command_prefix=commands.when_mentioned
    )
    await client.start(token)


if __name__ == "__main__":
    asyncio.run(start())

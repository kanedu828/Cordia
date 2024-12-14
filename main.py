import os
import asyncio
import discord
from cordia.cordia_client import CordiaClient
from dotenv import load_dotenv
from discord.ext import commands

from cordia.web_server import WebServer

load_dotenv()
# Set intents
intents = discord.Intents.default()
intents.message_content = False
intents.members = True

# Env variables
token = os.getenv("CORDIA_TOKEN")
psql_connection_string = os.getenv("CORDIA_DB_CONNECTION_STRING")
papertrail_address_number = os.getenv("CORDIA_PAPER_TRAIL_ADDRESS")
topgg_auth_token = os.getenv("TOPGG_AUTH_TOKEN")


async def start():
    client = CordiaClient(
        psql_connection_string,
        int(papertrail_address_number),
        intents=intents,
        command_prefix=commands.when_mentioned,
    )

    web_server = WebServer(client, topgg_auth_token)
    await asyncio.gather(client.start(token), web_server.start())


if __name__ == "__main__":
    asyncio.run(start())

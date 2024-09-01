from dotenv import load_dotenv
import os
import asyncio
from typing import List
import discord
from cordia.cordia_client import CordiaClient

# Load env variables
load_dotenv()

# Set intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Env variables
token = os.getenv('CORDIA_TOKEN')
psql_connection_string = os.getenv('CORDIA_DB_CONNECTION_STRING')

async def start():
    client = CordiaClient(psql_connection_string, intents=intents, command_prefix=';')
    await client.start(token)

if __name__ == '__main__':
    asyncio.run(start())
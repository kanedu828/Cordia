import os
import asyncio
import discord
from cordia.cordia_client import CordiaClient
from dotenv import load_dotenv

load_dotenv()
# Set intents
intents = discord.Intents.default()
intents.message_content = False
intents.members = True

# Env variables
token = os.getenv("CORDIA_TOKEN")
psql_connection_string = os.getenv("CORDIA_DB_CONNECTION_STRING")


async def sync_commands():
    # Create an instance of your custom CordiaClient
    client = CordiaClient(psql_connection_string, intents=intents, command_prefix=";")

    # Login to Discord
    await client.login(token)

    # Sync global slash commands
    synced_commands = await client.tree.sync()

    print(f"Successfully synced {len(synced_commands)} commands.")

    # Close the bot after syncing
    await client.close()


if __name__ == "__main__":
    asyncio.run(sync_commands())

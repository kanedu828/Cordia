from discord.ext import commands
from typing import List
import asyncpg
import logging

class CordiaClient(commands.Bot):

    # Extensions
    extensions: List[str] = ['cordia.cogs.util']

    def __init__(self, db_connection_string: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool: asyncpg.Pool = None
        self.db_connection_string: str = db_connection_string
        self.logger = self.setup_logger()

    def setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(console_handler)
        
        return logger

    async def setup_hook(self) -> None:
        for extension in CordiaClient.extensions:
            try:
                await self.load_extension(extension)
                self.logger.info(f'{extension} successfully loaded')
            except Exception as e:
                self.logger.error(f'{extension} cannot be loaded. [{str(e)}]')

            try:
                self.pool = await asyncpg.create_pool(self.db_connection_string)
                self.logger.info("Database pool created successfully")
            except Exception as e:
                self.logger.error(f"Failed to create database pool. [{str(e)}]")

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user.name} (ID: {self.user.id})')
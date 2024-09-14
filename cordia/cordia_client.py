from cordia.dao.boss_instance_dao import BossInstanceDao
from cordia.dao.daily_leaderboard_dao import DailyLeaderboardDao
from cordia.dao.item_dao import ItemDao
from cordia.service.battle_service import BattleService
from cordia.service.boss_service import BossService
from cordia.service.cooldown_service import CooldownService
from cordia.service.gear_service import GearService
from cordia.service.item_service import ItemService
from cordia.service.leaderboard_service import LeaderboardService
from cordia.service.loot_service import LootService
from cordia.service.player_service import PlayerService
from discord.ext import commands
from typing import List
import asyncpg
import logging

from cordia.dao.player_dao import PlayerDao
from cordia.service.cordia_service import CordiaService
from cordia.dao.gear_dao import GearDao
from cordia.dao.player_gear_dao import PlayerGearDao


class CordiaClient(commands.Bot):

    # Extensions
    extensions: List[str] = ["cordia.cogs.util", "cordia.cogs.cordia"]

    def __init__(self, db_connection_string: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool: asyncpg.Pool = None
        self.db_connection_string: str = db_connection_string
        self.logger = self.setup_logger()

    def setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(
            filename="discord.log", encoding="utf-8", mode="w"
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        logger.addHandler(console_handler)

        return logger

    async def setup_hook(self) -> None:
        for extension in CordiaClient.extensions:
            try:
                await self.load_extension(extension)
                self.logger.info(f"{extension} successfully loaded")
            except Exception as e:
                self.logger.error(f"{extension} cannot be loaded. [{str(e)}]")

        try:
            self.pool = await asyncpg.create_pool(self.db_connection_string)
            self.logger.info("Database pool created successfully")
        except Exception as e:
            self.logger.error(f"Failed to create database pool. [{str(e)}]")

        # DAOS
        player_dao = PlayerDao(self.pool)
        gear_dao = GearDao(self.pool)
        player_gear_dao = PlayerGearDao(self.pool)
        boss_instance_dao = BossInstanceDao(self.pool)
        item_dao = ItemDao(self.pool)
        daily_leaderboard_dao = DailyLeaderboardDao(self.pool)

        # SERVICES
        player_service = PlayerService(player_dao)
        gear_service = GearService(gear_dao, player_gear_dao)
        boss_service = BossService(boss_instance_dao)
        cooldown_service = CooldownService()
        item_service = ItemService(item_dao)
        loot_service = LootService(gear_service, player_service, item_service)
        leaderboard_service = LeaderboardService(player_dao, daily_leaderboard_dao, self)
        battle_service = BattleService(
            player_service, gear_service, boss_service, cooldown_service, loot_service, leaderboard_service
        )

        self.cordia_service = CordiaService(
            player_service,
            gear_service,
            boss_service,
            battle_service,
            item_service,
            leaderboard_service,
        )

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")

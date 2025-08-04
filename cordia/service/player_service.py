import datetime
import logging
from cordia.dao.player_dao import PlayerDao
from cordia.model.player import Player
from cordia.util.errors import NotEnoughGoldError, GoldLimitReachedError
from cordia.util.stats_util import get_upgrade_points
from cordia.data.locations import location_data
from cordia.util.constants import MAX_GOLD
from cordia.util.exp_util import exp_to_level

# Set up logger for this module
logger = logging.getLogger(__name__)


class PlayerService:
    def __init__(
        self,
        player_dao: PlayerDao,
    ):
        self.player_dao = player_dao
        logger.info("PlayerService initialized")

    async def get_player_by_discord_id(self, discord_id: int) -> Player | None:
        logger.debug(f"Getting player by Discord ID: {discord_id}")
        player = await self.player_dao.get_by_discord_id(discord_id)
        if player:
            level = exp_to_level(player.exp)
            logger.debug(f"Found player {discord_id}: level {level}, exp {player.exp}, gold {player.gold}")
        else:
            logger.debug(f"No player found for Discord ID: {discord_id}")
        return player

    async def insert_player(self, discord_id: int) -> Player:
        logger.info(f"Inserting new player: {discord_id}")
        player = await self.player_dao.insert_player(discord_id)
        level = exp_to_level(player.exp)
        logger.info(f"Created new player {discord_id}: level {level}, exp {player.exp}, gold {player.gold}")
        return player

    async def get_or_insert_player(self, discord_id: int) -> Player:
        logger.debug(f"Getting or inserting player: {discord_id}")
        player = await self.get_player_by_discord_id(discord_id)
        if player:
            logger.debug(f"Retrieved existing player: {discord_id}")
            return player
        else:
            logger.debug(f"Creating new player: {discord_id}")
            player = await self.insert_player(discord_id)
            return player

    async def increment_stat(self, discord_id: int, stat_name: str, increment_by: int):
        logger.info(f"Incrementing stat for user {discord_id}: {stat_name} by {increment_by}")
        player = await self.player_dao.get_by_discord_id(discord_id)
        upgrade_points = get_upgrade_points(player)
        if increment_by > upgrade_points or increment_by < 0:
            logger.error(f"Invalid stat increment for user {discord_id}: {stat_name} by {increment_by}, available points: {upgrade_points}")
            raise ValueError("Invalid increment amount")
        new_stat_value = player.__dict__[stat_name] + increment_by
        await self.player_dao.update_stat(discord_id, stat_name, new_stat_value)
        logger.info(f"Updated stat for user {discord_id}: {stat_name} = {new_stat_value}")

    async def increment_exp(self, discord_id: int, increment_by: int):
        logger.info(f"Incrementing exp for user {discord_id} by {increment_by}")
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_exp = player.exp + increment_by
        await self.player_dao.update_exp(discord_id, new_exp)
        logger.debug(f"Updated exp for user {discord_id}: {new_exp}")

    async def increment_gold(self, discord_id: int, increment_by: int):
        logger.info(f"Incrementing gold for user {discord_id} by {increment_by}")
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_gold = player.gold + increment_by
        if new_gold < 0:
            logger.error(f"Gold would be negative for user {discord_id}: {new_gold}")
            raise NotEnoughGoldError("Gold cannot be less than 0")
        if new_gold > MAX_GOLD:
            logger.warning(f"Gold would exceed max limit for user {discord_id}: {new_gold} > {MAX_GOLD}")
            return
        await self.player_dao.update_gold(discord_id, new_gold)
        logger.debug(f"Updated gold for user {discord_id}: {new_gold}")

    async def increment_rebirth_points(self, discord_id: int, increment_by: int):
        logger.info(f"Incrementing rebirth points for user {discord_id} by {increment_by}")
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_rebirth_points = player.rebirth_points + increment_by
        await self.player_dao.update_rebirth_points(discord_id, new_rebirth_points)
        logger.debug(f"Updated rebirth points for user {discord_id}: {new_rebirth_points}")

    async def update_location(self, discord_id: int, location: str):
        logger.info(f"Updating location for user {discord_id} to {location}")
        if not location in location_data:
            logger.error(f"Invalid location for user {discord_id}: {location}")
            raise ValueError(f"{location} is not a valid location")
        await self.player_dao.update_location(discord_id, location)
        logger.debug(f"Updated location for user {discord_id}: {location}")

    async def update_last_idle_claim(self, discord_id: int, last_idle_claim: datetime):
        logger.debug(f"Updating last idle claim for user {discord_id} to {last_idle_claim}")
        return await self.player_dao.update_last_idle_claim(discord_id, last_idle_claim)

    async def count_players_in_location(self, location: str) -> int:
        logger.debug(f"Counting players in location: {location}")
        count = await self.player_dao.count_players_in_location(location)
        logger.debug(f"Found {count} players in location {location}")
        return count

    async def update_last_boss_killed(self, discord_id: int):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        logger.info(f"Updating last boss killed for user {discord_id} to {current_time}")
        await self.player_dao.update_last_boss_killed(discord_id, current_time)

    async def rebirth_player(self, discord_id: int):
        logger.info(f"Rebirthing player: {discord_id}")
        await self.player_dao.reset_player_stats(discord_id)
        logger.info(f"Player {discord_id} has been rebirthed")

    def get_player_stats(self) -> dict:
        """Get statistics about player operations for monitoring."""
        stats = {
            "service_name": "PlayerService",
            "max_gold_limit": MAX_GOLD
        }
        logger.debug(f"Player service stats: {stats}")
        return stats

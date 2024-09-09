import datetime
from cordia.dao.player_dao import PlayerDao
from cordia.model.player import Player
from cordia.util.stats_util import get_upgrade_points
from cordia.data.locations import location_data


class PlayerService:
    def __init__(
        self,
        player_dao: PlayerDao,
    ):
        self.player_dao = player_dao

    async def get_player_by_discord_id(self, discord_id: int) -> Player | None:
        return await self.player_dao.get_by_discord_id(discord_id)

    async def insert_player(self, discord_id: int) -> Player:
        return await self.player_dao.insert_player(discord_id)

    async def get_or_insert_player(self, discord_id: int) -> Player:
        player = await self.get_player_by_discord_id(discord_id)
        if player:
            return player
        else:
            player = await self.insert_player(discord_id)
            return player

    async def increment_stat(self, discord_id: int, stat_name: str, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        upgrade_points = get_upgrade_points(player)
        if increment_by > upgrade_points or increment_by < 0:
            raise ValueError("Invalid increment amount")
        new_stat_value = player.__dict__[stat_name] + increment_by
        await self.player_dao.update_stat(discord_id, stat_name, new_stat_value)

    async def increment_exp(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_exp = player.exp + increment_by
        await self.player_dao.update_exp(discord_id, new_exp)

    async def increment_gold(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_gold = max(player.gold + increment_by, 0)  # Ensure gold doesn't go below 0
        await self.player_dao.update_gold(discord_id, new_gold)

    async def update_location(self, discord_id: int, location: str):
        if not location in location_data:
            raise ValueError(f"{location} is not a valid locatin")
        await self.player_dao.update_location(discord_id, location)

    async def update_last_idle_claim(self, discord_id: int, last_idle_claim: datetime):
        return await self.player_dao.update_last_idle_claim(discord_id, last_idle_claim)

    async def count_players_in_location(self, location: str) -> int:
        return await self.player_dao.count_players_in_location(location)

    async def update_last_boss_killed(self, discord_id):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        await self.player_dao.update_last_boss_killed(discord_id, current_time)
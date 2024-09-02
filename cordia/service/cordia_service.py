from cordia.dao.player_dao import PlayerDao
from cordia.data.locations import locations

class InvalidLocation(Exception):
    pass

class CordiaService:
    def __init__(self, player_dao: PlayerDao):
        self.player_dao = player_dao

    async def get_by_discord_id(self, discord_id: int):
        return await self.player_dao.get_by_discord_id(discord_id)
    
    async def insert_player(self, discord_id: int):
        await self.player_dao.insert_player(discord_id)

    async def get_or_insert_player(self, discord_id: int):
        return await self.player_dao.get_or_insert_player(discord_id)

    async def increment_strength(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_strength = player['strength'] + increment_by
        await self.player_dao.update_strength(discord_id, new_strength)

    async def increment_persistence(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_persistence = player['persistence'] + increment_by
        await self.player_dao.update_persistence(discord_id, new_persistence)

    async def increment_intelligence(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_intelligence = player['intelligence'] + increment_by
        await self.player_dao.update_intelligence(discord_id, new_intelligence)

    async def increment_exp(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_exp = player['exp'] + increment_by
        await self.player_dao.update_exp(discord_id, new_exp)

    async def increment_gold(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_gold = max(player['gold'] + increment_by, 0)  # Ensure gold doesn't go below 0
        await self.player_dao.update_gold(discord_id, new_gold)
    
    async def update_location(self, discord_id: int, location: str):
        if not location in locations:
            raise InvalidLocation(f'{location} is not a valid locatin')
        await self.player_dao.update_location(discord_id, location)

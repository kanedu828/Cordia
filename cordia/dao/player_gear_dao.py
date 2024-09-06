from typing import List
import asyncpg
from cordia.model.player_gear import PlayerGear

class PlayerGearDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_player_gear(self, discord_id: int) -> List[PlayerGear]:
        query = """
        SELECT pg.id, pg.discord_id, pg.gear_id, pg.slot, g.name, g.stars, g.bonus
        FROM player_gear pg
        JOIN gear g ON pg.gear_id = g.id
        WHERE pg.discord_id = $1
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, discord_id)
            return [PlayerGear(**row) for row in rows]

    async def equip_gear(self, discord_id: int, gear_id: int, slot: str) -> PlayerGear:
        query = """
        INSERT INTO player_gear (discord_id, gear_id, slot)
        VALUES ($1, $2, $3)
        ON CONFLICT (discord_id, slot)
        DO UPDATE SET gear_id = EXCLUDED.gear_id
        """
        async with self.pool.acquire() as connection:
            await connection.fetchrow(query, discord_id, gear_id, slot)

    async def remove_gear(self, discord_id: int, slot: str):
        query = """
        DELETE FROM player_gear
        WHERE discord_id = $1 AND slot = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, discord_id, slot)

    async def get_by_gear_id(self, gear_id: int) -> PlayerGear:
        query = """
        SELECT pg.id, pg.discord_id, pg.gear_id, pg.slot, g.name, g.stars, g.bonus
        FROM player_gear pg
        JOIN gear g ON pg.gear_id = g.id
        WHERE pg.gear_id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, gear_id)
            return PlayerGear(**row) if row else None
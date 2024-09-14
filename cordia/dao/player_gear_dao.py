from typing import List
import asyncpg
from cordia.model.gear_instance import GearInstance


class PlayerGearDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_player_gear(self, discord_id: int) -> List[GearInstance]:
        query = """
        SELECT pg.id, pg.discord_id, pg.gear_id, pg.slot, g.name, g.stars, g.bonus
        FROM player_gear pg
        JOIN gear g ON pg.gear_id = g.id
        WHERE pg.discord_id = $1
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, discord_id)
            return [
                GearInstance(
                    id=row["gear_id"],
                    discord_id=row["discord_id"],
                    slot=row["slot"],
                    name=row["name"],
                    stars=row["stars"],
                    bonus=row["bonus"],
                )
                for row in rows
            ]

    async def equip_gear(
        self, discord_id: int, gear_id: int, slot: str
    ) -> GearInstance:
        query = """
        INSERT INTO player_gear (discord_id, gear_id, slot)
        VALUES ($1, $2, $3)
        ON CONFLICT (discord_id, slot)
        DO UPDATE SET gear_id = EXCLUDED.gear_id
        """
        async with self.pool.acquire() as connection:
            await connection.fetchrow(query, discord_id, gear_id, slot)

    async def remove_all_gear(self, discord_id: int):
        query = """
        DELETE FROM player_gear
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, discord_id)

    async def get_by_gear_id(self, gear_id: int) -> GearInstance:
        query = """
        SELECT pg.id, pg.discord_id, pg.gear_id, pg.slot, g.name, g.stars, g.bonus
        FROM player_gear pg
        JOIN gear g ON pg.gear_id = g.id
        WHERE pg.gear_id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, gear_id)
            return (
                GearInstance(
                    id=row["gear_id"],
                    discord_id=row["discord_id"],
                    slot=row["slot"],
                    name=row["name"],
                    stars=row["stars"],
                    bonus=row["bonus"],
                )
                if row
                else None
            )

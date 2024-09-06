import asyncpg
from cordia.model.gear_instance import GearInstance

class GearDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_gear_by_id(self, id: int) -> GearInstance:
        query = """
        SELECT id, discord_id, name, stars, bonus, created_at, updated_at
        FROM gear
        WHERE id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, id)
            return GearInstance(**row)

    async def insert_gear(self, discord_id: int, name: str) -> GearInstance:
        query = """
        INSERT INTO gear (discord_id, name)
        VALUES ($1, $2)
        RETURNING id, discord_id, name, stars, bonus, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, discord_id, name)
            return GearInstance(**row)

    async def update_gear_stars(self, id: int, stars: int):
        query = """
        UPDATE gear
        SET stars = $1, updated_at = NOW()
        WHERE id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, stars, id)

    async def update_bonus(self, id: int, bonus: str):
        query = """
        UPDATE gear
        SET bonus = $1, updated_at = NOW()
        WHERE id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, bonus, id)

    async def get_gear_by_discord_id(self, discord_id: int) -> list[GearInstance]:
        query = """
        SELECT id, discord_id, name, stars, bonus, created_at, updated_at
        FROM gear
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, discord_id)
            return [GearInstance(**row) for row in rows]

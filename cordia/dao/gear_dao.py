import asyncpg

from cordia.model.gear import GearInstance

class GearDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_gear_by_id(self, id: int) -> GearInstance:
        query = """
        SELECT id, discord_id, name, stars, strength_bonus, persistence_bonus, intelligence_bonus, 
               efficiency_bonus, luck_bonus, created_at, updated_at
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
        RETURNING id, discord_id, name, stars, strength_bonus, persistence_bonus, 
                  intelligence_bonus, efficiency_bonus, luck_bonus, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, discord_id, name)
            return Gear(**row)

    async def update_gear_stars(self, id: int, stars: int):
        query = """
        UPDATE gear
        SET stars = $1, updated_at = NOW()
        WHERE id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, stars, id)

    async def update_bonus(self, id: int, bonus_name: str, bonus_value: str):
        valid_bonuses = {'strength_bonus', 'persistence_bonus', 'intelligence_bonus', 'efficiency_bonus', 'luck_bonus'}
        if bonus_name not in valid_bonuses:
            raise ValueError(f"Invalid bonus name: {bonus_name}. Must be one of {valid_bonuses}")

        query = f"""
        UPDATE gear
        SET {bonus_name} = $1, updated_at = NOW()
        WHERE id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, bonus_value, id)
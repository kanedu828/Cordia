import asyncpg
from cordia.model.boss_instance import BossInstance


class BossInstanceDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def insert_boss(
        self, discord_id: int, current_hp: int, name: str, expiration_time=None
    ) -> BossInstance:
        query = """
        INSERT INTO boss_instance (discord_id, current_hp, name, expiration_time)
        VALUES ($1, $2, $3, COALESCE($4, NOW()))
        ON CONFLICT (discord_id) 
        DO UPDATE SET current_hp = EXCLUDED.current_hp, name = EXCLUDED.name, updated_at = NOW(), expiration_time = COALESCE(EXCLUDED.expiration_time, boss_instance.expiration_time)
        RETURNING id, discord_id, current_hp, name, created_at, updated_at, expiration_time
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                query, discord_id, current_hp, name, expiration_time
            )
            return BossInstance(**row)

    async def update_boss_hp(self, discord_id: int, current_hp: int):
        query = """
        UPDATE boss_instance
        SET current_hp = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, current_hp, discord_id)

    async def get_boss_by_discord_id(self, discord_id: int) -> BossInstance:
        query = """
        SELECT id, discord_id, current_hp, name, created_at, updated_at, expiration_time
        FROM boss_instance
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                query, discord_id
            )  # fetchrow returns a single row
            if row:
                return BossInstance(**row)
            return None  # Return None if no record is found

    async def delete_boss_by_discord_id(self, discord_id: int) -> None:
        query = """
        DELETE FROM boss_instance
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, discord_id)

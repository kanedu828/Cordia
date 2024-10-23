import asyncpg
from cordia.model.achievement_instance import AchievementInstance


class AchievementDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def insert_or_increment_achievement(
        self, discord_id: int, monster: str, count: int = 1
    ) -> AchievementInstance:
        query = """
        INSERT INTO achievement (discord_id, monster, count, created_at, updated_at)
        VALUES ($1, $2, $3, NOW(), NOW())
        ON CONFLICT (discord_id, monster) 
        DO UPDATE SET count = achievement.count + EXCLUDED.count, updated_at = NOW()
        RETURNING id, discord_id, monster, count, created_at, updated_at;
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, discord_id, monster, count)
            return AchievementInstance(**row)

    async def update_achievement_count(self, discord_id: int, monster: str, count: int):
        query = """
        UPDATE achievement
        SET count = $1, updated_at = NOW()
        WHERE discord_id = $2 AND monster = $3
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, count, discord_id, monster)

    async def get_achievements_by_discord_id(
        self, discord_id: int
    ) -> list[AchievementInstance]:
        query = """
        SELECT id, discord_id, monster, count, created_at, updated_at
        FROM achievement
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, discord_id)
            return [AchievementInstance(**row) for row in rows]

    async def delete_achievement(self, discord_id: int, monster: str) -> None:
        query = """
        DELETE FROM achievement
        WHERE discord_id = $1 AND monster = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, discord_id, monster)

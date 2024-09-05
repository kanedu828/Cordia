from datetime import datetime
import asyncpg
from cordia.model.player import Player

class PlayerDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_discord_id(self, discord_id: int) -> Player | None:
        query = """
        SELECT discord_id, strength, persistence, intelligence, efficiency, luck, exp, gold, location, last_idle_claim
        FROM player
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(query, discord_id)
            if not record:
                return None
            return Player(**record)

    async def insert_player(self, discord_id: int) -> Player:
        query = """
        INSERT INTO player (discord_id)
        VALUES ($1)
        RETURNING discord_id, strength, persistence, intelligence, efficiency, luck, exp, gold, location, last_idle_claim
        """
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(query, discord_id)
            return Player(**record)

    async def update_stat(self, discord_id: int, stat_name: str, stat_value: int):
        valid_stats = {'strength', 'persistence', 'intelligence', 'efficiency', 'luck'}
        if stat_name not in valid_stats:
            raise ValueError(f"Invalid stat name: {stat_name}. Must be one of {valid_stats}")

        query = f"""
        UPDATE player
        SET {stat_name} = $1
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, stat_value, discord_id)

    async def update_exp(self, discord_id: int, exp: int):
        query = """
        UPDATE player
        SET exp = $1
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, exp, discord_id)

    async def update_gold(self, discord_id: int, gold: int):
        query = """
        UPDATE player
        SET gold = $1
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, gold, discord_id)

    async def update_location(self, discord_id: int, location: str):
        query = """
        UPDATE player
        SET location = $1
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, location, discord_id)
            
    async def update_last_idle_claim(self, discord_id: int, last_idle_claim: datetime):
            query = """
            UPDATE player
            SET last_idle_claim = $1
            WHERE discord_id = $2
            """
            async with self.pool.acquire() as connection:
                await connection.execute(query, last_idle_claim, discord_id)

    async def count_players_in_location(self, location: str) -> int:
        query = """
        SELECT COUNT(*)
        FROM player
        WHERE location = $1
        """
        async with self.pool.acquire() as connection:
            count = await connection.fetchval(query, location)
            return count

from datetime import datetime
import asyncpg
from cordia.model.player import Player


class PlayerDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_discord_id(self, discord_id: int) -> Player | None:
        query = """
        SELECT discord_id, strength, persistence, intelligence, efficiency, luck, exp, gold, location, last_idle_claim,
               last_boss_killed, created_at, updated_at, rebirth_points, trophies
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
        RETURNING discord_id, strength, persistence, intelligence, efficiency, luck, exp, gold, location, last_idle_claim,
                  last_boss_killed, created_at, updated_at, rebirth_points, trophies
        """
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(query, discord_id)
            return Player(**record)

    async def update_stat(self, discord_id: int, stat_name: str, stat_value: int):
        valid_stats = {"strength", "persistence", "intelligence", "efficiency", "luck"}
        if stat_name not in valid_stats:
            raise ValueError(
                f"Invalid stat name: {stat_name}. Must be one of {valid_stats}"
            )

        query = f"""
        UPDATE player
        SET {stat_name} = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, stat_value, discord_id)

    async def update_exp(self, discord_id: int, exp: int):
        query = """
        UPDATE player
        SET exp = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, exp, discord_id)

    async def update_gold(self, discord_id: int, gold: int):
        query = """
        UPDATE player
        SET gold = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, gold, discord_id)

    async def increment_trophies(self, discord_id: int):
        query = """
        UPDATE player
        SET trophies = trophies + 1, updated_at = NOW()
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, discord_id)

    async def update_rebirth_points(self, discord_id: int, rebirth_points: int):
        query = """
        UPDATE player
        SET rebirth_points = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, rebirth_points, discord_id)

    async def update_location(self, discord_id: int, location: str):
        query = """
        UPDATE player
        SET location = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, location, discord_id)

    async def update_last_idle_claim(self, discord_id: int, last_idle_claim: datetime):
        query = """
        UPDATE player
        SET last_idle_claim = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, last_idle_claim, discord_id)

    async def update_last_boss_killed(
        self, discord_id: int, last_boss_killed: datetime
    ):
        query = """
        UPDATE player
        SET last_boss_killed = $1, updated_at = NOW()
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, last_boss_killed, discord_id)

    async def count_players_in_location(self, location: str) -> int:
        query = """
        SELECT COUNT(*)
        FROM player
        WHERE location = $1
        """
        async with self.pool.acquire() as connection:
            count = await connection.fetchval(query, location)
            return count

    async def get_top_100_players_by_column(self, column: str) -> list[Player]:
        if column not in {"exp", "gold", "rebirth_points", "trophies"}:
            raise ValueError(f"Invalid column for ranking: {column}")

        query = f"""
        SELECT discord_id, strength, persistence, intelligence, efficiency, luck, exp, gold, location, last_idle_claim,
            last_boss_killed, created_at, updated_at, rebirth_points, trophies
        FROM player
        ORDER BY {column} DESC
        LIMIT 100
        """
        async with self.pool.acquire() as connection:
            records = await connection.fetch(query)
            return [Player(**record) for record in records]

    async def get_player_rank_by_column(self, discord_id: int, column: str) -> int:
        if column not in {"exp", "gold", "rebirth_points", "trophies"}:
            raise ValueError(f"Invalid column for ranking: {column}")

        query = f"""
        SELECT COUNT(*)
        FROM player
        WHERE {column} > (SELECT {column} FROM player WHERE discord_id = $1)
        """
        async with self.pool.acquire() as connection:
            rank = await connection.fetchval(query, discord_id)
            return (
                rank + 1
            )  # The rank is +1 because the player is behind 'rank' players

    async def reset_player_stats(self, discord_id: int):
        query = """
        UPDATE player
        SET strength = 1, 
            persistence = 1, 
            intelligence = 1, 
            luck = 1, 
            efficiency = 1, 
            exp = 0, 
            location = 'the_plains_i',
            updated_at = NOW()
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, discord_id)

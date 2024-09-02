import asyncpg

class PlayerDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_discord_id(self, discord_id: int):
        query = """
        SELECT discord_id, strength, persistence, intelligence, exp, gold, location
        FROM player
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, discord_id)

    async def insert_player(self, discord_id: int):
        query = """
        INSERT INTO player (discord_id)
        VALUES ($1)
        RETURNING discord_id, strength, persistence, intelligence, exp, gold, location
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, discord_id)

    async def get_or_insert_player(self, discord_id: int):
        player = await self.get_by_discord_id(discord_id)
        if player:
            return player
        else:
            return await self.insert_player(discord_id)

    async def update_strength(self, discord_id: int, strength: int):
        query = """
        UPDATE player
        SET strength = $1
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, strength, discord_id)

    async def update_persistence(self, discord_id: int, persistence: int):
        query = """
        UPDATE player
        SET persistence = $1
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, persistence, discord_id)

    async def update_intelligence(self, discord_id: int, intelligence: int):
        query = """
        UPDATE player
        SET intelligence = $1
        WHERE discord_id = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, intelligence, discord_id)

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

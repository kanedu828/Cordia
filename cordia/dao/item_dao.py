import asyncpg
from typing import Optional
from cordia.model.item_instance import (
    ItemInstance,
)


class ItemDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def insert_item(self, discord_id: int, name: str, count: int) -> ItemInstance:
        query = """
        INSERT INTO item (discord_id, name, count, created_at, updated_at)
        VALUES ($1, $2, $3, NOW(), NOW())
        ON CONFLICT (discord_id, name)
        DO UPDATE SET count = item.count + EXCLUDED.count, updated_at = NOW()
        RETURNING discord_id, name, count, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, discord_id, name, count)
            return ItemInstance(**row)

    async def update_item_count(self, discord_id: int, name: str, count: int):
        query = """
        UPDATE item
        SET count = $1, updated_at = NOW()
        WHERE discord_id = $2 AND name = $3
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, count, discord_id, name)

    async def get_item(self, discord_id: int, name: str) -> Optional[ItemInstance]:
        query = """
        SELECT discord_id, name, count, created_at, updated_at
        FROM item
        WHERE discord_id = $1 AND name = $2
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, discord_id, name)
            if row:
                return ItemInstance(**row)
            return None

    async def delete_item(self, discord_id: int, name: str) -> None:
        query = """
        DELETE FROM item
        WHERE discord_id = $1 AND name = $2
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, discord_id, name)

    async def get_all_items_for_user(self, discord_id: int) -> list[ItemInstance]:
        query = """
        SELECT discord_id, name, count, created_at, updated_at
        FROM item
        WHERE discord_id = $1
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, discord_id)
            return [ItemInstance(**row) for row in rows]

    async def get_cores_for_user(self, discord_id: int) -> list[ItemInstance]:
        query = """
        SELECT discord_id, name, count, created_at, updated_at
        FROM item
        WHERE discord_id = $1 AND name IN ('basic_core', 'quality_core', 'supreme_core', 'chaos_core')
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, discord_id)
            return [ItemInstance(**row) for row in rows]

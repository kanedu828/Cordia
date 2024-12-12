import asyncpg
from typing import Optional, List
from cordia.model.market_item import MarketItem


class MarketItemDao:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_all_market_items(self) -> list[MarketItem]:
        query = """
        SELECT id, discord_id, item_name, price, count, created_at, updated_at
        FROM market_item
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query)
            return [MarketItem(**row) for row in rows]

    async def delete_market_item(self, market_item_id: int) -> None:
        query = """
        DELETE FROM market_item
        WHERE id = $1
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, market_item_id)

    async def insert_market_item(self, discord_id: int, item_name: str, price: int, count: int) -> MarketItem:
        query = """
        INSERT INTO market_item (discord_id, item_name, price, count, created_at, updated_at)
        VALUES ($1, $2, $3, $4, NOW(), NOW())
        RETURNING id, discord_id, item_name, price, count, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, discord_id, item_name, price, count)
            return MarketItem(**row)

    async def get_market_items_by_name(self, item_name: str) -> list[MarketItem]:
        query = """
        SELECT m.id, m.discord_id, m.item_name, m.price, m.count, m.created_at, m.updated_at
        FROM market_item m
        INNER JOIN item i ON m.item_name = i.id
        WHERE i.item_name = $1
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, item_name)
            return [MarketItem(**row) for row in rows]

    async def get_market_item_by_id(self, market_item_id: int) -> Optional[MarketItem]:
        query = """
        SELECT id, discord_id, item_name, price, count, created_at, updated_at
        FROM market_item
        WHERE id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, market_item_id)
            if row:
                return MarketItem(**row)
            return None

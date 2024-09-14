from datetime import date
import asyncpg
from cordia.model.daily_leaderboard import DailyLeaderboard


class DailyLeaderboardDao:
    VALID_COLUMNS = {"exp", "gold", "monsters_killed"}  # Valid columns for ranking

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def upsert_daily_leaderboard(
        self, discord_id: int, exp: int, gold: int, monsters_killed: int
    ) -> DailyLeaderboard:
        query = """
        INSERT INTO daily_leaderboard (discord_id, exp, gold, monsters_killed, date)
        VALUES ($1, $2, $3, $4, CURRENT_DATE)
        ON CONFLICT (discord_id, date) DO UPDATE
        SET exp = daily_leaderboard.exp + EXCLUDED.exp,
            gold = daily_leaderboard.gold + EXCLUDED.gold,
            monsters_killed = daily_leaderboard.monsters_killed + EXCLUDED.monsters_killed
        RETURNING discord_id, exp, gold, monsters_killed, date
        """
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                query, discord_id, exp, gold, monsters_killed
            )
            return DailyLeaderboard(**record)

    async def get_top_100_daily_players_by_column(
        self, column: str
    ) -> list[DailyLeaderboard]:
        # Ensure the column is valid to prevent SQL injection
        if column not in self.VALID_COLUMNS:
            raise ValueError(
                f"Invalid column for ranking: {column}. Must be one of {self.VALID_COLUMNS}"
            )

        # Use the safe column and query for top players, with current date (CURRENT_DATE) as the date filter
        query = f"""
        SELECT discord_id, exp, gold, monsters_killed, date
        FROM daily_leaderboard
        WHERE date = CURRENT_DATE
        ORDER BY {column} DESC
        LIMIT 100
        """
        async with self.pool.acquire() as connection:
            records = await connection.fetch(query)
            return [DailyLeaderboard(**record) for record in records]

    async def get_player_daily_rank_by_column(
        self, discord_id: int, column: str
    ) -> int:
        # Ensure the column is valid to prevent SQL injection
        if column not in self.VALID_COLUMNS:
            raise ValueError(
                f"Invalid column for ranking: {column}. Must be one of {self.VALID_COLUMNS}"
            )

        # Query to get the rank of the player based on the specified column
        query = f"""
        SELECT COUNT(*) + 1 AS rank
        FROM daily_leaderboard
        WHERE date = CURRENT_DATE
        AND {column} > (SELECT {column} FROM daily_leaderboard WHERE discord_id = $1 AND date = CURRENT_DATE)
        """
        async with self.pool.acquire() as connection:
            rank = await connection.fetchval(query, discord_id)
            if rank is None:
                raise ValueError(
                    f"Player with discord_id {discord_id} not found in today's leaderboard."
                )
            return rank

    async def delete_old_leaderboard_entries(self, cutoff_date: date):
        query = """
        DELETE FROM daily_leaderboard
        WHERE date < $1
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, cutoff_date)

    async def reset_leaderboard_for_date(self, leaderboard_date: date):
        query = """
        DELETE FROM daily_leaderboard
        WHERE date = $1
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, leaderboard_date)

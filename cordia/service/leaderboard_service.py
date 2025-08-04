import pytz
import logging
from cordia.dao.daily_leaderboard_dao import DailyLeaderboardDao
from cordia.dao.player_dao import PlayerDao
from cordia.model.daily_leaderboard import DailyLeaderboard
from cordia.model.player import Player
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
import discord

# Set up logger for this module
logger = logging.getLogger(__name__)


class LeaderboardService:
    def __init__(
        self,
        player_dao: PlayerDao,
        daily_leaderboard_dao: DailyLeaderboardDao,
        bot: commands.Bot,
    ):
        self.player_dao = player_dao
        self.daily_leaderboard_dao = daily_leaderboard_dao
        self.bot = bot
        est = pytz.timezone("America/New_York")

        self.leaderboard_user_cache = {}
        self.scheduler = AsyncIOScheduler()

        # Schedule the trophy awarding task to run 5 minutes before midnight every day
        self.scheduler.add_job(
            self.award_trophies_to_top_players, "cron", hour=23, minute=55, timezone=est
        )
        self.scheduler.start()
        logger.info("LeaderboardService initialized with trophy awarding scheduled")

    async def get_top_100_players_by_column(self, column: str) -> list[Player]:
        logger.debug(f"Getting top 100 players by column: {column}")
        players = await self.player_dao.get_top_100_players_by_column(column)
        logger.debug(f"Retrieved {len(players)} players for column {column}")
        return players

    async def get_player_rank_by_column(self, discord_id: int, column: str) -> int:
        logger.debug(f"Getting rank for user {discord_id} in column {column}")
        rank = await self.player_dao.get_player_rank_by_column(discord_id, column)
        logger.debug(f"User {discord_id} rank in {column}: {rank}")
        return rank

    async def get_leaderboard_user(self, discord_id: int) -> str:
        if discord_id in self.leaderboard_user_cache:
            logger.debug(f"Retrieved cached username for user {discord_id}")
            return self.leaderboard_user_cache[discord_id]
        else:
            logger.debug(f"Fetching username for user {discord_id}")
            try:
                user = await self.bot.fetch_user(discord_id)
                user_name = user.name
                self.leaderboard_user_cache[discord_id] = user_name
                logger.debug(f"Cached username for user {discord_id}: {user_name}")
                return user_name
            except discord.NotFound:
                logger.debug(f"User {discord_id} not found in Discord")
                return f"User_{discord_id}"
            except discord.Forbidden:
                logger.debug(f"Cannot access user {discord_id} (forbidden)")
                return f"User_{discord_id}"
            except Exception as e:
                logger.debug(f"Failed to fetch user {discord_id}: {e}")
                return f"User_{discord_id}"

    async def upsert_daily_leaderboard(
        self, discord_id: int, exp: int, gold: int, monsters_killed: int
    ):
        logger.info(f"Upserting daily leaderboard for user {discord_id}: exp={exp}, gold={gold}, monsters={monsters_killed}")
        await self.daily_leaderboard_dao.upsert_daily_leaderboard(
            discord_id, exp, gold, monsters_killed
        )

    async def get_top_100_daily_players_by_column(
        self, column: str
    ) -> list[DailyLeaderboard]:
        logger.debug(f"Getting top 100 daily players by column: {column}")
        players = await self.daily_leaderboard_dao.get_top_100_daily_players_by_column(
            column
        )
        logger.debug(f"Retrieved {len(players)} daily players for column {column}")
        return players

    async def get_player_daily_rank_by_column(
        self, discord_id: int, column: str
    ) -> int:
        logger.debug(f"Getting daily rank for user {discord_id} in column {column}")
        rank = await self.daily_leaderboard_dao.get_player_daily_rank_by_column(
            discord_id, column
        )
        logger.debug(f"User {discord_id} daily rank in {column}: {rank}")
        return rank

    async def award_trophies_to_top_players(self):
        logger.info("Starting trophy awarding to top players")
        # Get the top 3 players for each category (exp, gold, monsters_killed)
        categories = ["exp", "gold", "monsters_killed"]

        for category in categories:
            logger.debug(f"Awarding trophies for category: {category}")
            top_players = (
                await self.daily_leaderboard_dao.get_top_100_daily_players_by_column(
                    category
                )
            )

            # Award trophies to the top 3 players
            for i, player in enumerate(top_players[:3]):
                await self.player_dao.increment_trophies(player.discord_id)
                logger.info(f"Awarded trophy to user {player.discord_id} for {category} (rank {i+1})")
        
        logger.info("Completed trophy awarding to top players")

    def get_leaderboard_stats(self) -> dict:
        """Get statistics about leaderboard cache for monitoring."""
        stats = {
            "cached_users": len(self.leaderboard_user_cache)
        }
        logger.debug(f"Leaderboard stats: {stats}")
        return stats

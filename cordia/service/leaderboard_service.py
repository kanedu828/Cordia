import pytz
from cordia.dao.daily_leaderboard_dao import DailyLeaderboardDao
from cordia.dao.player_dao import PlayerDao
from cordia.model.daily_leaderboard import DailyLeaderboard
from cordia.model.player import Player
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class LeaderboardService:
    def __init__(
        self, player_dao: PlayerDao, daily_leaderboard_dao: DailyLeaderboardDao, bot
    ):
        self.player_dao = player_dao
        self.daily_leaderboard_dao = daily_leaderboard_dao

        self.bot = bot

        est = pytz.timezone("America/New_York")

        self.leaderboard_user_cache = {}
        self.scheduler = AsyncIOScheduler()

        # # Schedule the trophy awarding task to run 5 minutes before midnight every day
        self.scheduler.add_job(
            self.award_trophies_to_top_players, "cron", hour=23, minute=55, timezone=est
        )
        self.scheduler.start()

    async def get_top_100_players_by_column(self, column: str) -> list[Player]:
        return await self.player_dao.get_top_100_players_by_column(column)

    async def get_player_rank_by_column(self, discord_id: int, column: str) -> int:
        return await self.player_dao.get_player_rank_by_column(discord_id, column)

    async def get_leaderboard_user(self, discord_id: int) -> str:
        if discord_id in self.leaderboard_user_cache:
            return self.leaderboard_user_cache[discord_id]
        else:
            user = await self.bot.fetch_user(discord_id)
            user_name = user.name
            self.leaderboard_user_cache[discord_id] = user_name
            return user_name

    async def upsert_daily_leaderboard(
        self, discord_id: int, exp: int, gold: int, monsters_killed: int
    ):
        await self.daily_leaderboard_dao.upsert_daily_leaderboard(
            discord_id, exp, gold, monsters_killed
        )

    async def get_top_100_daily_players_by_column(
        self, column: str
    ) -> list[DailyLeaderboard]:
        return await self.daily_leaderboard_dao.get_top_100_daily_players_by_column(
            column
        )

    async def get_player_daily_rank_by_column(
        self, discord_id: int, column: str
    ) -> int:
        return await self.daily_leaderboard_dao.get_player_daily_rank_by_column(
            discord_id, column
        )

    async def award_trophies_to_top_players(self):
        # Get the top 3 players for each category (exp, gold, monsters_killed)
        categories = ["exp", "gold", "monsters_killed"]

        for category in categories:
            top_players = (
                await self.daily_leaderboard_dao.get_top_100_daily_players_by_column(
                    category
                )
            )

            # Award trophies to the top 3 players
            for player in top_players[:3]:
                await self.player_dao.increment_trophies(player.discord_id)

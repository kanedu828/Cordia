from cordia.dao.player_dao import PlayerDao
from cordia.model.player import Player


class LeaderboardService:
    def __init__(self, player_dao: PlayerDao, bot):
        self.player_dao = player_dao

        self.bot = bot

        self.leaderboard_user_cache = {}

    async def get_top_100_players_by_exp(self) -> list[Player]:
        return await self.player_dao.get_top_100_players_by_exp()

    async def get_player_rank_by_exp(self, discord_id: int) -> int:
        return await self.player_dao.get_player_rank_by_exp(discord_id)

    async def get_leaderboard_user(self, discord_id: int) -> str:
        if discord_id in self.leaderboard_user_cache:
            return self.leaderboard_user_cache[discord_id]
        else:
            user = await self.bot.fetch_user(discord_id)
            user_name = user.name
            self.leaderboard_user_cache[discord_id] = user_name
            return user_name

import math
from cordia.dao.achievement_dao import AchievementDao
from cordia.model.achievement_instance import AchievementInstance
from cordia.data.achievements import achievement_data
from cordia.model.player_stats import PlayerStats


class AchievementService:
    def __init__(self, achievement_dao: AchievementDao):
        self.achievement_dao = achievement_dao

    async def get_achievements_by_discord_id(
        self, discord_id: int
    ) -> list[AchievementInstance]:
        return await self.achievement_dao.get_achievements_by_discord_id(discord_id)

    async def get_achievement_stat_bonuses(
        self, discord_id: int
    ) -> tuple[PlayerStats, PlayerStats]:
        """
        Returns a tuple of player stats.
        First element is additive stats, second is percentage stats.
        """

        achievements = await self.get_achievements_by_discord_id(discord_id)

        def calculate_stat_bonus(achievement, max_bonus: int = 5) -> PlayerStats:
            achievement_data = achievement.get_achievement_data()
            increments = math.floor(
                achievement.count / achievement_data.monster_killed_increment
            )
            return achievement_data.stat_bonus * min(max_bonus, increments)

        # Filter achievements and calculate additive bonuses
        additive_bonuses = [
            calculate_stat_bonus(a)
            for a in achievements
            if a.get_achievement_data().stat_modifier == "+"
        ]

        # Filter achievements and calculate percentage bonuses
        percentage_bonuses = [
            calculate_stat_bonus(a)
            for a in achievements
            if a.get_achievement_data().stat_modifier == "%"
        ]

        # Sum the bonuses using PlayerStats as the starting point
        additive = sum(additive_bonuses, PlayerStats())
        percentage = sum(percentage_bonuses, PlayerStats())

        return additive, percentage

    async def increment_achievement(
        self, discord_id: int, monster: str, count: int = 1
    ) -> None:
        if monster in achievement_data:
            await self.achievement_dao.insert_or_increment_achievement(
                discord_id, monster, count
            )

    async def update_achievement_count(
        self, discord_id: int, monster: str, count: int
    ) -> None:
        await self.achievement_dao.update_achievement_count(discord_id, monster, count)

    async def delete_achievement(self, discord_id: int, monster: str) -> None:
        await self.achievement_dao.delete_achievement(discord_id, monster)

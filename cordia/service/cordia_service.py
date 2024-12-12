import datetime
from typing import List, Literal, Optional

from cordia.model.achievement_instance import AchievementInstance
from cordia.model.attack_result import AttackResult
from cordia.model.boos_fight_result import BossFightResult
from cordia.model.boss_instance import BossInstance
from cordia.model.daily_leaderboard import DailyLeaderboard
from cordia.model.gear_instance import GearInstance
from cordia.model.item_instance import ItemInstance
from cordia.model.player import Player

from cordia.model.player_stats import PlayerStats
from cordia.service.achievement_service import AchievementService
from cordia.service.battle_service import BattleService
from cordia.service.boss_service import BossService
from cordia.service.gear_service import GearService
from cordia.service.item_service import ItemService
from cordia.service.leaderboard_service import LeaderboardService
from cordia.service.market_service import MarketService
from cordia.service.player_service import PlayerService
from cordia.util.exp_util import exp_to_level


class CordiaService:
    def __init__(
        self,
        player_service: PlayerService,
        gear_service: GearService,
        boss_service: BossService,
        battle_service: BattleService,
        item_service: ItemService,
        leaderboard_service: LeaderboardService,
        achievement_service: AchievementService,
        market_service: MarketService,
    ):
        self.player_service = player_service
        self.gear_service = gear_service
        self.boss_service = boss_service
        self.battle_service = battle_service
        self.item_service = item_service
        self.leaderboard_service = leaderboard_service
        self.achievement_service = achievement_service
        self.market_service = market_service

    # Player
    async def get_player_by_discord_id(self, discord_id: int) -> Player | None:
        return await self.player_service.get_player_by_discord_id(discord_id)

    async def insert_player(self, discord_id: int) -> Player:
        return await self.player_service.insert_player(discord_id)

    async def get_or_insert_player(self, discord_id: int) -> Player:
        return await self.player_service.get_or_insert_player(discord_id)

    async def increment_stat(self, discord_id: int, stat_name: str, increment_by: int):
        await self.player_service.increment_stat(discord_id, stat_name, increment_by)

    async def increment_gold(self, discord_id: int, increment_by: int):
        await self.player_service.increment_gold(discord_id, increment_by)

    async def update_location(self, discord_id: int, location: str):
        await self.player_service.update_location(discord_id, location)

    async def count_players_in_location(self, location: str) -> int:
        return await self.player_service.count_players_in_location(location)

    async def increment_rebirth_points(self, discord_id: int, increment_by: int):
        await self.player_service.increment_rebirth_points(discord_id, increment_by)

    async def rebirth_player(self, discord_id: int):
        await self.player_service.rebirth_player(discord_id)

    # Gear
    async def insert_gear(self, discord_id: int, name: str):
        return await self.gear_service.insert_gear(discord_id, name)

    async def get_gear_by_id(self, id: int) -> GearInstance:
        return await self.gear_service.get_gear_by_id(id)

    async def get_armory(self, discord_id: int) -> List[GearInstance]:
        return await self.gear_service.get_armory(discord_id)

    async def increment_gear_stars(self, gear_id: int, stars: int):
        await self.gear_service.increment_gear_stars(gear_id, stars)

    async def update_gear_bonus(self, gear_id: int, bonus: str):
        await self.gear_service.update_gear_bonus(gear_id, bonus)

    async def equip_highest_level_gear(self, discord_id: int) -> list[str]:
        player = await self.get_player_by_discord_id(discord_id)
        return await self.gear_service.equip_highest_level_gear(
            discord_id, exp_to_level(player.exp)
        )

    # Player Gear
    async def get_player_gear(self, discord_id: int):
        return await self.gear_service.get_player_gear(discord_id)

    async def equip_gear(self, discord_id: int, gear_id: int, slot: str):
        return await self.gear_service.equip_gear(discord_id, gear_id, slot)

    async def remove_all_gear(self, discord_id: int):
        await self.gear_service.remove_all_gear(discord_id)

    async def get_player_gear_by_gear_id(self, gear_id: int) -> GearInstance:
        return await self.gear_service.get_player_gear_by_gear_id(gear_id)

    # Items
    async def insert_item(self, discord_id: int, name: str, count: int):
        await self.item_service.insert_item(discord_id, name, count)

    async def get_inventory(self, discord_id: int) -> list[ItemInstance]:
        return await self.item_service.get_inventory(discord_id)

    async def get_item(self, discord_id: int, name: str) -> Optional[ItemInstance]:
        return await self.item_service.get_item(discord_id, name)

    async def get_cores_for_user(self, discord_id: int) -> list[ItemInstance]:
        return await self.item_service.get_cores_for_user(discord_id)

    # Leaderboard
    async def get_top_100_players_by_column(self, column: str) -> list[Player]:
        return await self.leaderboard_service.get_top_100_players_by_column(column)

    async def get_player_rank_by_column(self, discord_id, column: str) -> int:
        return await self.leaderboard_service.get_player_rank_by_column(
            discord_id, column
        )

    async def get_leaderboard_user(self, discord_id: int) -> str:
        return await self.leaderboard_service.get_leaderboard_user(discord_id)

    async def get_top_100_daily_players_by_column(
        self, column: str
    ) -> list[DailyLeaderboard]:
        return await self.leaderboard_service.get_top_100_daily_players_by_column(
            column
        )

    async def get_player_daily_rank_by_column(
        self, discord_id: int, column: str
    ) -> int:
        return await self.leaderboard_service.get_player_daily_rank_by_column(
            discord_id, column
        )

    # Boss Instance
    async def get_boss_by_discord_id(self, discord_id: int) -> BossInstance:
        return await self.boss_service.get_boss_by_discord_id(discord_id)

    async def update_boss_hp(self, discord_id: int, current_hp: int):
        await self.boss_service.update_boss_hp(discord_id, current_hp)

    async def insert_boss(self, discord_id: int, name: str):
        await self.boss_service.insert_boss(discord_id, name)

    async def delete_boss(self, discord_id):
        await self.boss_service.delete_boss(discord_id)

    def get_boss_time_remaining(self, discord_id) -> datetime:
        return self.boss_service.get_boss_time_remaining(discord_id)

    # Battle
    async def boss_fight(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> BossFightResult:
        return await self.battle_service.boss_fight(discord_id, action)

    async def idle_fight(self, discord_id: int):
        return await self.battle_service.idle_fight(discord_id)

    async def attack(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> AttackResult:
        return await self.battle_service.attack(discord_id, action)

    # Achievement
    async def get_achievements_by_discord_id(
        self, discord_id: int
    ) -> list[AchievementInstance]:
        return await self.achievement_service.get_achievements_by_discord_id(discord_id)

    async def increment_achievement(
        self, discord_id: int, monster: str, count: int = 1
    ):
        await self.achievement_service.increment_achievement(discord_id, monster, count)

    async def get_achievement_stat_bonuses(
        self, discord_id: int
    ) -> tuple[PlayerStats, PlayerStats]:
        return await self.achievement_service.get_achievement_stat_bonuses(discord_id)

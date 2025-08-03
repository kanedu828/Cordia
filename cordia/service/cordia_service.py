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
from cordia.service.vote_service import VoteService
from cordia.util.exp_util import exp_to_level


class CordiaManager:
    def __init__(
        self,
        bot,
        player_service: PlayerService,
        gear_service: GearService,
        boss_service: BossService,
        battle_service: BattleService,
        item_service: ItemService,
        leaderboard_service: LeaderboardService,
        achievement_service: AchievementService,
        market_service: MarketService,
        vote_service: VoteService,
    ):
        self.bot = bot
        self.player_service = player_service
        self.gear_service = gear_service
        self.boss_service = boss_service
        self.battle_service = battle_service
        self.item_service = item_service
        self.leaderboard_service = leaderboard_service
        self.achievement_service = achievement_service
        self.market_service = market_service
        self.vote_service = vote_service



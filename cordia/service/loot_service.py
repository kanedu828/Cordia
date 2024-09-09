from typing import List, Tuple
from cordia.model.gear_instance import GearInstance
from cordia.model.monster import Monster
from cordia.service.gear_service import GearService
from cordia.service.player_service import PlayerService
from cordia.util.stats_util import random_within_range
from cordia.data.gear import gear_data


class LootService:
    def __init__(self, gear_service: GearService, player_service: PlayerService):
        self.gear_service = gear_service
        self.player_service = player_service

    async def handle_loot(
        self, discord_id: int, monster: Monster, player_stats: dict, kills: int
    ) -> Tuple[int, int, List[GearInstance], int]:
        # Calculate EXP and gold
        exp_gained = random_within_range(
            int((monster.exp + min(player_stats["efficiency"], monster.exp)) * kills)
        )
        gold_gained = random_within_range(
            int((monster.gold + min(player_stats["luck"], monster.gold)) * kills)
        )

        # Handle gear drops
        new_gear_loot = []
        sold_gear_amount = 0
        gear_loot = monster.get_dropped_gear(kills)
        for g in gear_loot:
            gd = gear_data[g]
            try:
                await self.gear_service.insert_gear(discord_id, g)
                new_gear_loot.append(gd)
            except:
                sold_gear_amount += gd.gold_value

        await self.player_service.increment_exp(discord_id, exp_gained)
        await self.player_service.increment_gold(
            discord_id, gold_gained + sold_gear_amount
        )

        return exp_gained, gold_gained, new_gear_loot, sold_gear_amount

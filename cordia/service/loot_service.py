from typing import List, Tuple
from cordia.model.gear_instance import GearInstance
from cordia.model.item import Item
from cordia.model.monster import Monster
from cordia.model.player_stats import PlayerStats
from cordia.service.gear_service import GearService
from cordia.service.item_service import ItemService
from cordia.service.player_service import PlayerService
from cordia.util.battle_util import get_diminished_stat
from cordia.util.stats_util import random_within_range
from cordia.data.gear import gear_data
from cordia.data.items import item_data


class LootService:
    def __init__(
        self,
        gear_service: GearService,
        player_service: PlayerService,
        item_service: ItemService,
    ):
        self.gear_service = gear_service
        self.player_service = player_service
        self.item_service = item_service

    async def handle_loot(
        self, discord_id: int, monster: Monster, player_stats: PlayerStats, kills: int
    ) -> Tuple[int, int, List[GearInstance], int, Tuple[Item, int]]:
        # Calculate EXP and gold
        exp_gained = random_within_range(
            int(
                monster.exp
                + get_diminished_stat(monster.exp, player_stats.efficiency, 0.6)
            )
            * kills
        )
        gold_gained = random_within_range(
            int(
                monster.gold + get_diminished_stat(monster.gold, player_stats.luck, 0.6)
            )
            * kills
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

        # Handle item drops
        item_drops = []
        for i, c in monster.get_dropped_items(kills):
            id = item_data[i]
            await self.item_service.insert_item(discord_id, i, c)
            item_drops.append((id, c))

        return exp_gained, gold_gained, new_gear_loot, sold_gear_amount, item_drops

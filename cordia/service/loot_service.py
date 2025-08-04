import logging
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

# Set up logger for this module
logger = logging.getLogger(__name__)


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
        logger.info("LootService initialized")

    async def handle_loot(
        self, discord_id: int, monster: Monster, player_stats: PlayerStats, kills: int
    ) -> Tuple[int, int, List[GearInstance], int, Tuple[Item, int]]:
        logger.info(f"Handling loot for user {discord_id}: {monster.name} x{kills}")
        
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
        logger.debug(f"Calculated rewards for user {discord_id}: exp={exp_gained}, gold={gold_gained}")

        # Handle gear drops
        new_gear_loot = []
        sold_gear_amount = 0
        gear_loot = monster.get_dropped_gear(kills)
        logger.debug(f"Gear drops for user {discord_id}: {len(gear_loot)} items")
        
        for g in gear_loot:
            gd = gear_data[g]
            try:
                await self.gear_service.insert_gear(discord_id, g)
                new_gear_loot.append(gd)
                logger.debug(f"Added gear for user {discord_id}: {g}")
            except Exception as e:
                sold_gear_amount += gd.gold_value
                logger.debug(f"Failed to add gear for user {discord_id}: {g}, sold for {gd.gold_value} gold")

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
            logger.debug(f"Added item for user {discord_id}: {i} x{c}")

        logger.info(f"Completed loot handling for user {discord_id}: exp={exp_gained}, gold={gold_gained}, gear={len(new_gear_loot)}, sold={sold_gear_amount}, items={len(item_drops)}")
        return exp_gained, gold_gained, new_gear_loot, sold_gear_amount, item_drops

    def get_loot_stats(self) -> dict:
        """Get statistics about loot operations for monitoring."""
        stats = {
            "service_name": "LootService"
        }
        logger.debug(f"Loot service stats: {stats}")
        return stats

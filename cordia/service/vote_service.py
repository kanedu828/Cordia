import logging
import random
from cordia.service.item_service import ItemService

# Set up logger for this module
logger = logging.getLogger(__name__)


class VoteService:
    def __init__(self, item_service: ItemService):
        self.item_service = item_service
        logger.info("VoteService initialized")

    async def give_vote_reward(self, discord_id: int):
        logger.info(f"Giving vote reward to user {discord_id}")
        rewards = [
            ("shard", [2, 5]),
            ("basic_core", [2, 5]),
            ("quality_core", [1, 3]),
            ("supreme_core", [1, 2]),
            ("chaos_core", [1, 1]),
        ]
        item_name, count_range = random.choice(rewards)
        count = random.randint(count_range[0], count_range[1])
        await self.item_service.insert_item(discord_id, item_name, count)
        logger.info(f"Gave vote reward to user {discord_id}: {item_name} x{count}")
        return item_name, count

    def get_vote_stats(self) -> dict:
        """Get statistics about vote operations for monitoring."""
        stats = {
            "service_name": "VoteService"
        }
        logger.debug(f"Vote service stats: {stats}")
        return stats

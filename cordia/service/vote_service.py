import random
from cordia.service.item_service import ItemService


class VoteService:
    def __init__(self, item_service: ItemService):
        self.item_service = item_service

    async def give_vote_reward(self, discord_id: int):
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
        return item_name, count

import logging
from typing import Optional
from cordia.dao.item_dao import ItemDao
from cordia.model.item_instance import ItemInstance
from cordia.util.errors import NotEnoughItemsError

# Set up logger for this module
logger = logging.getLogger(__name__)


class ItemService:
    def __init__(self, item_dao: ItemDao):
        self.item_dao = item_dao
        logger.info("ItemService initialized")

    async def insert_item(self, discord_id: int, name: str, count: int) -> None:
        logger.info(f"Inserting item for user {discord_id}: {name} x{count}")
        item = await self.item_dao.get_item(discord_id, name)
        if item and item.count + count < 0:
            logger.error(f"Item count would be negative for user {discord_id}: {name} ({item.count} + {count})")
            raise NotEnoughItemsError("Item count cannot be negative")
        inserted_item = await self.item_dao.insert_item(discord_id, name, count)
        logger.info(f"Inserted item for user {discord_id}: {name} x{inserted_item.count}")
        if inserted_item.count == 0:
            logger.debug(f"Deleting item with zero count for user {discord_id}: {name}")
            await self.item_dao.delete_item(discord_id, name)

    async def get_inventory(self, discord_id: int) -> list[ItemInstance]:
        logger.debug(f"Getting inventory for user {discord_id}")
        inventory = await self.item_dao.get_all_items_for_user(discord_id)
        logger.debug(f"Retrieved {len(inventory)} items for user {discord_id}")
        return inventory

    async def get_item(self, discord_id: int, name: str) -> Optional[ItemInstance]:
        logger.debug(f"Getting item for user {discord_id}: {name}")
        item = await self.item_dao.get_item(discord_id, name)
        if item:
            logger.debug(f"Found item for user {discord_id}: {name} x{item.count}")
        else:
            logger.debug(f"No item found for user {discord_id}: {name}")
        return item

    async def get_cores_for_user(self, discord_id: int) -> list[ItemInstance]:
        logger.debug(f"Getting cores for user {discord_id}")
        cores = await self.item_dao.get_cores_for_user(discord_id)
        logger.debug(f"Retrieved {len(cores)} cores for user {discord_id}")
        return cores

    def get_item_stats(self) -> dict:
        """Get statistics about item operations for monitoring."""
        stats = {
            "service_name": "ItemService"
        }
        logger.debug(f"Item service stats: {stats}")
        return stats

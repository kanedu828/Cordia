from typing import Optional
from cordia.dao.item_dao import ItemDao
from cordia.model.item_instance import ItemInstance


class ItemService:
    def __init__(self, item_dao: ItemDao):
        self.item_dao = item_dao

    async def insert_item(self, discord_id: int, name: str, count: int) -> None:
        inserted_item = await self.item_dao.insert_item(discord_id, name, count)
        if inserted_item.count < 0:
            raise ValueError("Item count cannot be negative")
        if inserted_item.count == 0:
            await self.item_dao.delete_item(discord_id, name)

    async def get_inventory(self, discord_id: int) -> list[ItemInstance]:
        return await self.item_dao.get_all_items_for_user(discord_id)

    async def get_item(self, discord_id: int, name: str) -> Optional[ItemInstance]:
        return await self.item_dao.get_item(discord_id, name)

    async def get_cores_for_user(self, discord_id: int) -> list[ItemInstance]:
        return await self.item_dao.get_cores_for_user(discord_id)

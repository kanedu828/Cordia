from enum import Enum
from cordia.model.gear import Gear
from cordia.model.item import Item
from cordia.data.gear import gear_data
from cordia.data.items import item_data

class ShopItemType(Enum):
    GEAR = "gear"
    ITEM = "item"

class ShopItem:
    item_name: str
    type: ShopItemType
    gold_cost: int = 0
    item_cost: list[tuple[Item, int]]

    def get_item_data(self) -> Gear | Item:
        if self.type == ShopItemType.GEAR:
            return gear_data[self.item_name]
        else:
            return item_data[self.item_name]
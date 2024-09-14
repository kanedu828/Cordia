from dataclasses import dataclass
from enum import Enum
from cordia.model.gear import Gear
from cordia.model.item import Item
from cordia.data.gear import gear_data
from cordia.data.items import item_data


class ShopItemType(Enum):
    GEAR = "gear"
    ITEM = "item"


@dataclass()
class ShopItem:
    item_name: str
    type: ShopItemType
    item_cost: tuple[str, int]
    gold_cost: int = 0

    def get_item_data(self) -> Gear | Item:
        if self.type == ShopItemType.GEAR:
            return gear_data[self.item_name]
        else:
            return item_data[self.item_name]

    def display_item_cost(self) -> str:
        id = item_data[self.item_cost[0]]
        return f"**{self.item_cost[1]}** {id.display_item()}"

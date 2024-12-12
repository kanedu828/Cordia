from dataclasses import dataclass
from datetime import datetime
from cordia.data.items import item_data


@dataclass(frozen=True, kw_only=True)
class MarketItem:
    id: int
    discord_id: int
    item_name: str
    price: int
    count: int
    created_at: datetime
    updated_at: datetime
    
    def get_item_data(self):
        return item_data[self.item_name]

    def display_item(self):
        return f"**{self.count}** {self.get_item_data().display_item()}(s)"

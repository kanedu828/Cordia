from dataclasses import dataclass
from datetime import datetime

from cordia.data.items import item_data


@dataclass()
class ItemInstance:
    discord_id: int
    name: str
    count: int
    created_at: datetime
    updated_at: datetime

    def get_item_data(self):
        return item_data[self.name]

    def display_item(self):
        return f"**{self.count}** {self.get_item_data().display_item()}(s)"

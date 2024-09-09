from dataclasses import dataclass
from datetime import datetime


@dataclass()
class ItemInstance:
    discord_id: int
    name: str
    count: int
    created_at: datetime
    updated_at: datetime

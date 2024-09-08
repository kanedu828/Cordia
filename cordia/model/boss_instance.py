from dataclasses import dataclass
from datetime import datetime


@dataclass()
class BossInstance:
    id: int
    discord_id: int
    current_hp: int
    name: str
    expiration_time: datetime
    created_at: datetime
    updated_at: datetime

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Player:
    discord_id: int
    strength: int
    persistence: int
    intelligence: int
    efficiency: int
    luck: int
    exp: int
    gold: int
    rebirth_points: int
    trophies: int
    location: str
    last_idle_claim: datetime
    last_boss_killed: datetime
    created_at: datetime
    updated_at: datetime

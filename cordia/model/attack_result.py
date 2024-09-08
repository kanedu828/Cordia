from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from cordia.model.gear import Gear
from cordia.model.item import Item
from cordia.model.location import Location


@dataclass
class AttackResult:
    kills: int = 0
    exp: int = 0
    gold: int = 0
    item_loot: List[Item] = field(default_factory=list)
    gear_loot: List[Gear] = field(default_factory=list)
    sold_gear_amount: int = 0
    monster: str = ""
    on_cooldown: bool = False
    cooldown_expiration: datetime = datetime.now(timezone.utc)
    location: Location = None
    player_exp: int = 0
    leveled_up: bool = False
    is_crit: bool = False
    damage: int = 0
    is_combo: bool = False
    weapon: Gear = None

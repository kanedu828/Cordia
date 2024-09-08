from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from cordia.model.boss_instance import BossInstance
from cordia.model.gear import Gear
from cordia.model.item import Item
from cordia.model.location import Location


@dataclass
class BossFightResult:
    boss_instance: BossInstance = None
    killed: bool = False
    exp: int = 0
    gold: int = 0
    item_loot: List[Item] = field(default_factory=list)
    gear_loot: List[Gear] = field(default_factory=list)
    sold_gear_amount: int = 0
    on_cooldown: bool = False
    cooldown_expiration: datetime = datetime.now(timezone.utc)
    leveled_up: bool = False
    is_crit: bool = False
    damage: int = 0
    is_combo: bool = False
    weapon: Gear = None
    boss_expiration: datetime = datetime.now(timezone.utc)
    is_expired: bool = False
    player_exp: int = 0

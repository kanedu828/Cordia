from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from cordia.model.location import Location

@dataclass
class AttackResult:
    kills: int = 0
    exp: int = 0
    gold: int = 0
    loot: List = field(default_factory=list)
    monster: str = ''
    on_cooldown: bool = False
    cooldown_expiration: datetime = datetime.now()
    location: Location = None
    player_exp: int = 0
    leveled_up: bool = False
    is_crit: bool = False
    damage: int = 0
    is_combo: bool = False
    spell_name: str = ''
    spell_text: str = ''
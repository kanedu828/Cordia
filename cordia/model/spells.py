from dataclasses import dataclass
from enum import Enum

class SpellType(Enum):
    DAMAGE = "damage"
    BUFF = "buff"

@dataclass(frozen=True)
class Spell:
    spell_type: SpellType
    name: str
    description: str
    damage: int
    spell_cooldown: int
    cast_text: str
    scaling_stat: str = 'intelligence'
    strike_radius: int = 1
    magic_penetration: int = 0
    buff: str = ''
    scaling_multiplier: int = 1
    
    
    
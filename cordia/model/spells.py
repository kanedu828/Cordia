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
    buff: str = ''
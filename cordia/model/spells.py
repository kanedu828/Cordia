from dataclasses import dataclass
from enum import Enum

from cordia.util.stat_mapping import get_stat_emoji, get_stat_modifier

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
    
    def get_spell_stats_string(self):
        spell_stats = ["damage", "spell_cooldown", "strike_radius", "magic_penetration", "scaling_multiplier"]
        max_stat_length_extra = max(len(stat) for stat in spell_stats)
        spell_stats_string = ""
        for s in spell_stats:
            if self.__dict__[s]:
                spell_stats_string += f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {self.__dict__[s]}{get_stat_modifier(s)}"

        return f"```{spell_stats_string}```"
        
    
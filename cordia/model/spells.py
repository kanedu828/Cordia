from dataclasses import dataclass
from enum import Enum

from cordia.model.player_stats import PlayerStats
from cordia.util.stat_mapping import get_stat_emoji, get_stat_modifier


class SpellType(Enum):
    DAMAGE = "damage"
    BUFF = "buff"


@dataclass(frozen=True)
class Buff:
    stat_bonus: PlayerStats
    duration: int


@dataclass(frozen=True)
class Spell:
    spell_type: SpellType
    name: str
    description: str
    spell_cooldown: int
    cast_text: str
    damage: int = 0
    scaling_stat: str = "intelligence"
    strike_radius: int = 1
    magic_penetration: int = 0
    buff: Buff = None
    scaling_multiplier: float = 1

    def get_spell_stats_string(self):
        spell_stats = [
            "damage",
            "spell_cooldown",
            "strike_radius",
            "magic_penetration",
            "scaling_multiplier",
        ]
        max_stat_length_extra = max(len(stat) for stat in spell_stats)
        spell_stats_string = ""
        if self.spell_type == SpellType.BUFF and self.buff:
            spell_stats = [
                "spell_cooldown",
            ]
            max_stat_length_extra = max(
                len(stat)
                for stat in spell_stats + list(self.buff.stat_bonus.__dict__.keys())
            )
            for s, v in self.buff.stat_bonus.__dict__.items():
                if not v:
                    continue
                spell_stats_string += f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} +{v}{get_stat_modifier(v)}"
            spell_stats_string += f"\n{get_stat_emoji('duration')}{'Duration'.ljust(max_stat_length_extra)} {self.buff.duration}{get_stat_modifier(self.buff.duration)}"

        for s in spell_stats:
            if self.__dict__[s]:
                spell_stats_string += f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {self.__dict__[s]}{get_stat_modifier(s)}"
        spell_stats_string = (
            f"\n🔍{'Type'.ljust(max_stat_length_extra)} {self.spell_type.value.title()}"
            + spell_stats_string
        )
        return f"```{spell_stats_string}```"

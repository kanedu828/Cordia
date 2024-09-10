from dataclasses import dataclass
from enum import Enum
import math
import random
from typing import Literal

from cordia.model.spells import Spell, SpellType


class GearType(Enum):
    WEAPON = "weapon"
    HAT = "hat"
    TOP = "top"
    PANTS = "pants"
    SHOES = "shoes"
    PENDANT = "pendant"
    CAPE = "cape"
    RING = "ring"
    GLOVES = "gloves"


@dataclass(frozen=True, kw_only=True)
class Gear:
    name: str
    type: GearType
    level: int
    gold_value: int
    # Stats
    strength: int = 0
    persistence: int = 0
    intelligence: int = 0
    efficiency: int = 0
    luck: int = 0
    crit_chance: int = 0
    boss_damage: int = 0
    # For Weapons
    attack_cooldown: int = 0
    damage: int = 0
    penetration: int = 0
    combo_chance: int = 0
    strike_radius: int = 0
    spell: Spell = None
    # Gear Set
    gear_set: str = ""

    def get_max_stars(self):
        if self.level < 10:
            return 5
        elif self.level < 25:
            return 10
        elif self.level < 50:
            return 15
        elif self.level < 60:
            return 20
        elif self.level < 100:
            return 25

    def get_bonus_string(
        self, core: Literal["basic_core", "quality_core", "supreme_core", "chaos_core"]
    ):
        """
        Formatted as <stat>:<amount>:<modifier> separated by ;
        ex: intelligence:10:+;strength:21:%
        """
        stat_options = ["strength", "persistence", "intelligence", "efficiency", "luck"]
        weapon_stat_options = ["damage", "boss_damage"]
        spell_stat_options = ["spell_damage"]

        # Add weapon-specific stats if the gear is a weapon
        if self.type == GearType.WEAPON:
            stat_options += weapon_stat_options
        if self.spell and self.spell.spell_type == SpellType.DAMAGE:
            stat_options += spell_stat_options

        # Determine number of lines (number of bonuses)
        lines = random.randint(1, 3)

        # Core-based value modifiers
        flat_modifiers = {
            "basic_core": 0.5,
            "quality_core": 1,
            "supreme_core": 1.5,
            "chaos_core": 2,
        }

        percentage_ranges = {
            "basic_core": (1, 5),
            "quality_core": (6, 10),
            "supreme_core": (11, 15),
            "chaos_core": (16, 20),
        }

        # Build the bonus string
        bonuses = []
        for _ in range(lines):
            rand_stat = random.choice(stat_options)

            # Boss damage can't have a percentage modifier and its value is halved
            if rand_stat == "boss_damage":
                rand_modifier = "+"
                random_val = random.randint(1, self.level)
                random_val = max(1, math.ceil(random_val * flat_modifiers.get(core, 1) / 2))
            else:
                rand_modifier = random.choices(["+", "%"], weights=[0.7, 0.3], k=1)[0]

                if rand_modifier == "+":
                    random_val = random.randint(1, self.level)
                    random_val = math.ceil(random_val * flat_modifiers.get(core, 1))
                else:
                    random_val = random.randint(*percentage_ranges.get(core, (1, 5)))

            bonuses.append(f"{rand_stat}:{random_val}:{rand_modifier}")

        return ";".join(bonuses)

    def get_use_core_cost(self):
        return self.level * 10
from dataclasses import dataclass
from enum import Enum

from cordia.model.spells import Spell

class GearType(Enum):
    WEAPON = "weapon"
    HAT = "hat"
    TOP = "top"
    PANTS = "pants"
    SHOES = "shoes"
    PENDANT = "pendant"
    CAPE = "cape"
    RING = "ring"

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
    gear_set: str = ''

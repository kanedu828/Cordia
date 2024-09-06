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
    
@dataclass(frozen=True)
class GearInstance:
    id: int
    discord_id: int
    name: str
    stars: int
    strength_bonus: str
    persistence_bonus: str
    intelligence_bonus: str
    efficiency_bonus: str
    luck_bonus: str
    created_at: str
    updated_at: str

@dataclass(frozen=True)
class PlayerGear:
    id: int
    discord_id: int
    gear_id: int
    slot: str
    name: str
    stars: int
    strength_bonus: str
    persistence_bonus: str
    intelligence_bonus:str
    efficiency_bonus: str
    luck_bonus: str


@dataclass(frozen=True, kw_only=True)
class Gear:
    name: str
    type: GearType
    level: int
    attack_cooldown: int
    gold_value: int
    strength: int = 0
    persistence: int = 0
    intelligence: int = 0
    efficiency: int = 0
    luck: int = 0
    crit_chance: int = 0
    boss_damage: int = 0
    penetration: int = 0
    combo_chance: int = 0
    strike_radius: int = 1
    spell: Spell = None
    gear_set: str = ''
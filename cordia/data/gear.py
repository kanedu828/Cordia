from enum import Enum

from cordia.data.spells import Spell, SpellType

class GearType(Enum):
    WEAPON = "weapon"
    HAT = "hat"
    TOP = "top"
    PANTS = "pants"
    SHOES = "shoes"
    PENDANT = "pendant"
    CAPE = "cape"
    RING_1 = "ring_1"
    RING_2 = "ring_2"

class Gear:
    def __init__(self, name: str, type: GearType, level: int, attack_cooldown: int, gold_value: int, strength=0, persistence=0, intelligence=0, efficiency=0, luck=0, crit_chance=0, boss_damage=0, penetration=0, spell=None, gear_set=''):
        self.name = name
        self.type = type
        self.strength = strength
        self.persistence = persistence
        self.intelligence = intelligence
        self.efficiency = efficiency
        self.luck = luck
        self.level = level
        self.attack_cooldown = attack_cooldown
        self.spell = spell
        self.gold_value = gold_value
        self.gear_set = gear_set
        self.crit_chance = crit_chance
        self.boss_damage = boss_damage
        self.penetration = penetration

    def __repr__(self):
        return (f"<Gear(name={self.name}, type={self.type}, strength={self.strength}, "
                f"persistence={self.persistence}, intelligence={self.intelligence}, "
                f"efficiency={self.efficiency}, luck={self.luck}, level={self.level}, "
                f"attack_cooldown={self.attack_cooldown}, spell={self.spell}, "
                f"gold_value={self.gold_value})>")

gear_data = {
    "basic_sword": Gear(
        name="Basic Sword",
        type=GearType.WEAPON,
        level=1,
        strength=10,
        persistence=4,
        attack_cooldown=20,
        crit_chance=5,
        gold_value=50
    ),
    "basic_dagger": Gear(
        name="Basic Dagger",
        type=GearType.WEAPON,
        level=1,
        strength=6,
        persistence=6,
        attack_cooldown=10,
        crit_chance=10,
        gold_value=50
    ),
    "basic_bow": Gear(
        name="Basic Bow",
        type=GearType.WEAPON,
        level=1,
        strength=7,
        persistence=10,
        attack_cooldown=30,
        crit_chance=15,
        gold_value=50
    ),
    "basic_wand": Gear(
        name="Basic Wand",
        type=GearType.WEAPON,
        level=1,
        strength=2,
        persistence=3,
        intelligence=10,
        crit_chance=5,
        attack_cooldown=20,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Fireball",
            description="Blast enemies with a fireball.",
            damage=10
        ),
        gold_value=50
    ),
}
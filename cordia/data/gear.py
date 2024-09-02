from enum import Enum

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


class SpellType(Enum):
    DAMAGE = "damage"
    BUFF = "buff"


class Spell:
    def __init__(self, spell_type, name, damage):
        self.spell_type = spell_type
        self.name = name
        self.damage = damage

    def __repr__(self):
        return f"<Spell(type={self.spell_type}, name={self.name}, damage={self.damage})>"


class Gear:
    def __init__(self, name, gear_type, strength, persistence, intelligence, efficiency, luck, level, attack_cooldown, spell, gold_value):
        self.name = name
        self.type = gear_type
        self.strength = strength
        self.persistence = persistence
        self.intelligence = intelligence
        self.efficiency = efficiency
        self.luck = luck
        self.level = level
        self.attack_cooldown = attack_cooldown
        self.spell = spell
        self.gold_value = gold_value

    def __repr__(self):
        return (f"<Gear(name={self.name}, type={self.type}, strength={self.strength}, "
                f"persistence={self.persistence}, intelligence={self.intelligence}, "
                f"efficiency={self.efficiency}, luck={self.luck}, level={self.level}, "
                f"attack_cooldown={self.attack_cooldown}, spell={self.spell}, "
                f"gold_value={self.gold_value})>")


gear_data = {
    "basic_sword": Gear(
        name="Basic Sword",
        gear_type=GearType.WEAPON,
        strength=10,
        persistence=4,
        intelligence=0,
        efficiency=0,
        luck=0,
        level=0,
        attack_cooldown=20,
        spell=None,
        gold_value=50
    ),
    "basic_dagger": Gear(
        name="Basic Dagger",
        gear_type=GearType.WEAPON,
        strength=6,
        persistence=6,
        intelligence=0,
        efficiency=0,
        luck=0,
        level=0,
        attack_cooldown=10,
        spell=None,
        gold_value=50
    ),
    "basic_bow": Gear(
        name="Basic Bow",
        gear_type=GearType.WEAPON,
        strength=7,
        persistence=10,
        intelligence=0,
        efficiency=0,
        luck=0,
        level=0,
        attack_cooldown=30,
        spell=None,
        gold_value=50
    ),
    "basic_wand": Gear(
        name="Basic Wand",
        gear_type=GearType.WEAPON,
        strength=2,
        persistence=3,
        intelligence=10,
        efficiency=0,
        luck=0,
        level=0,
        attack_cooldown=20,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Fireball",
            damage=10
        ),
        gold_value=50
    ),
}
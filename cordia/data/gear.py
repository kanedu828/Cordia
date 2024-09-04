from cordia.model.gear import Gear, GearType
from cordia.model.spells import Spell, SpellType

gear_data = {
    "basic_sword": Gear(
        name="Basic Sword",
        type=GearType.WEAPON,
        level=1,
        strength=10,
        persistence=4,
        attack_cooldown=20,
        crit_chance=5,
        strike_radius=5,
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
        gold_value=50,
        strike_radius=2,
        combo_chance=1,
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
            damage=5,
            spell_cooldown=30,
            cast_text="You summon a small fireball and throw at the enemy.",
            strike_radius=5
        ),
        gold_value=50
    ),
}
from cordia.model.gear import Gear, GearType
from cordia.model.spells import Spell, SpellType

weapon_data = {
    "basic_sword": Gear(
        name="Basic Sword",
        type=GearType.WEAPON,
        level=1,
        damage=10,
        strength=4,
        persistence=2,
        attack_cooldown=20,
        crit_chance=5,
        strike_radius=5,
        gold_value=10,
    ),
    "basic_dagger": Gear(
        name="Basic Dagger",
        type=GearType.WEAPON,
        level=1,
        damage=8,
        strength=2,
        persistence=2,
        attack_cooldown=12,
        crit_chance=10,
        gold_value=10,
        strike_radius=2,
        combo_chance=1,
    ),
    "basic_bow": Gear(
        name="Basic Bow",
        type=GearType.WEAPON,
        level=1,
        damage=7,
        strength=2,
        persistence=10,
        attack_cooldown=30,
        crit_chance=15,
        gold_value=10,
        strike_radius=1,
    ),
    "basic_wand": Gear(
        name="Basic Wand",
        type=GearType.WEAPON,
        level=1,
        damage=2,
        persistence=3,
        intelligence=10,
        crit_chance=5,
        attack_cooldown=20,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Fireball",
            description="Blast enemies with a fireball.",
            damage=12,
            spell_cooldown=30,
            cast_text="You summon a small fireball and throw at it the enemy.",
            strike_radius=5,
        ),
        gold_value=10,
    ),
    "goblin_dagger": Gear(
        name="Goblin Dagger",
        type=GearType.WEAPON,
        level=5,
        damage=15,
        strength=4,
        persistence=2,
        luck=2,
        attack_cooldown=12,
        crit_chance=12,
        strike_radius=2,
        combo_chance=3,
        gold_value=25,
    ),
    "wolf_fang_sword": Gear(
        name="Wolf Fang Sword",
        type=GearType.WEAPON,
        level=10,
        damage=24,
        strength=8,
        persistence=2,
        attack_cooldown=20,
        crit_chance=5,
        strike_radius=5,
        gold_value=25,
    ),
    "hunter_bow": Gear(
        name="Hunter Bow",
        type=GearType.WEAPON,
        level=10,
        damage=18,
        persistence=15,
        strength=2,
        attack_cooldown=30,
        crit_chance=10,
        strike_radius=1,
        gold_value=25,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Volley",
            description="Shoot several arrows at once",
            damage=18,
            spell_cooldown=35,
            cast_text="You shoot several arrows at once.",
            strike_radius=3,
            scaling_stat="persistence",
            scaling_multiplier=0.2,
        ),
    ),
    "red_eye_wand": Gear(
        name="Red Eye Wand",
        type=GearType.WEAPON,
        level=10,
        damage=5,
        persistence=2,
        intelligence=15,
        crit_chance=5,
        attack_cooldown=20,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Poison Sting",
            description="Sting enemies with poison",
            damage=30,
            spell_cooldown=25,
            cast_text="You send a concetrated blast of poison to your enemy.",
            strike_radius=3,
        ),
        gold_value=25,
    ),
    "ancient_forest_sword": Gear(
        name="Ancient Forest Sword",
        type=GearType.WEAPON,
        level=20,
        damage=32,
        boss_damage=5,
        strength=14,
        persistence=3,
        attack_cooldown=25,
        crit_chance=5,
        strike_radius=3,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Vine Strike",
            description="Wraps your sword in vines and strikes your enemy",
            damage=20,
            spell_cooldown=45,
            cast_text="You summon vines to enhance your weapon and you strike your enemy.",
            strike_radius=3,
            scaling_stat="strength",
            scaling_multiplier=0.2,
        ),
        gold_value=50,
    ),
}

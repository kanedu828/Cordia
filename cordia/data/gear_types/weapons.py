from cordia.model.gear import Gear, GearType
from cordia.model.spells import Spell, SpellType

weapon_data = {
    "basic_sword": Gear(
        name="Basic Sword",
        type=GearType.WEAPON,
        level=1,
        damage=10,
        strength=5,
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
        damage=9,
        strength=2,
        persistence=2,
        attack_cooldown=12,
        crit_chance=10,
        gold_value=10,
        strike_radius=2,
        combo_chance=5,
    ),
    "basic_bow": Gear(
        name="Basic Bow",
        type=GearType.WEAPON,
        level=1,
        damage=9,
        strength=2,
        persistence=10,
        attack_cooldown=30,
        crit_chance=15,
        gold_value=10,
        strike_radius=3,
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
            damage=13,
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
        damage=20,
        strength=4,
        persistence=2,
        luck=2,
        attack_cooldown=12,
        crit_chance=12,
        strike_radius=2,
        combo_chance=5,
        gold_value=25,
    ),
    "wolf_fang_dagger": Gear(
        name="Wolf Fang Dagger",
        type=GearType.WEAPON,
        level=10,
        damage=18,
        strength=2,
        efficiency=6,
        attack_cooldown=12,
        crit_chance=10,
        strike_radius=2,
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
        damage=24,
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
            damage=24,
            spell_cooldown=35,
            cast_text="You shoot several arrows at once.",
            strike_radius=3,
            scaling_stat="persistence",
            scaling_multiplier=0.5,
        ),
    ),
    "red_eye_wand": Gear(
        name="Red Eye Wand",
        type=GearType.WEAPON,
        level=10,
        damage=5,
        persistence=2,
        intelligence=17,
        crit_chance=5,
        attack_cooldown=20,
        strike_radius=1,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Poison Sting",
            description="Sting enemies with poison",
            damage=35,
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
            scaling_multiplier=0.25,
        ),
        gold_value=50,
    ),
    "wyvern_tooth_dagger": Gear(
        name="Wyvern Tooth Dagger",
        type=GearType.WEAPON,
        level=20,
        damage=28,
        strength=6,
        attack_cooldown=13,
        crit_chance=15,
        strike_radius=2,
        combo_chance=5,
        gold_value=40,
    ),
    "earth_elemental_staff": Gear(
        name="Earth Elemental Staff",
        type=GearType.WEAPON,
        level=20,
        damage=7,
        intelligence=25,
        persistence=15,
        attack_cooldown=25,
        crit_chance=10,
        strike_radius=1,
        gold_value=40,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Stone Blast",
            description="Hurl sharp stones towards the enemy.",
            damage=50,
            spell_cooldown=30,
            cast_text="You summon sharpened stones and shoot them at your enemy.",
            strike_radius=5,
        ),
    ),
    "wyrm_bow": Gear(
        name="Wyrm Bow",
        type=GearType.WEAPON,
        level=30,
        damage=35,
        persistence=25,
        strength=9,
        attack_cooldown=20,
        crit_chance=20,
        strike_radius=1,
        gold_value=40,
    ),
    "mountain_breaker_blade": Gear(
        name="Mountain Breaker Blade",
        type=GearType.WEAPON,
        level=40,
        damage=92,
        strength=40,
        attack_cooldown=60,
        crit_chance=10,
        strike_radius=8,
        gold_value=50,
    ),
    "thorny_dagger": Gear(
        name="Thorny Dagger",
        type=GearType.WEAPON,
        level=40,
        damage=36,
        strength=13,
        attack_cooldown=13,
        crit_chance=10,
        strike_radius=1,
        combo_chance=7,
        gold_value=40,
    ),
    "staff_of_roots": Gear(
        name="Staff Of Roots",
        type=GearType.WEAPON,
        level=40,
        damage=9,
        intelligence=35,
        luck=5,
        attack_cooldown=30,
        crit_chance=15,
        strike_radius=1,
        gold_value=40,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Entangle Strangle",
            description="Summons roots to entangle foes.",
            damage=68,
            spell_cooldown=30,
            cast_text="Roots sprout from the staff and strangle the enemies",
            strike_radius=5,
        ),
    ),
    "potted_morning_star": Gear(
        name="Potted Morning Star",
        type=GearType.WEAPON,
        level=45,
        damage=60,
        strength=25,
        attack_cooldown=20,
        crit_chance=5,
        strike_radius=3,
        combo_chance=5,
        gold_value=50,
    ),
    "shadow_hunter_bow": Gear(
        name="Shadow Hunter Bow",
        type=GearType.WEAPON,
        level=50,
        damage=40,
        persistence=35,
        efficiency=15,
        attack_cooldown=30,
        crit_chance=50,
        strike_radius=2,
        combo_chance=10,
        gold_value=60,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Shadow Shot",
            description="Shoot several an unseeable arrows to strike your enemy.",
            damage=10,
            scaling_stat="persistence",
            scaling_multiplier=0.5,
            spell_cooldown=5,
            cast_text="Several shadows fly through the floor and strikes your enemy.",
            strike_radius=5,
        ),   
    ),
    "frostblade_dagger": Gear(
        name="Frostblade Dagger",
        type=GearType.WEAPON,
        level=50,
        damage=50,
        persistence=10,
        efficiency=10,
        attack_cooldown=10,
        crit_chance=25,
        strike_radius=2,
        gold_value=60,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Frost Bite",
            description="Imbue your dagger with frost and strike your enemy.",
            damage=75,
            scaling_stat="efficiency",
            scaling_multiplier=0.70,
            spell_cooldown=60,
            cast_text="You imbue your dagger with frost and strike your enemy.",
            strike_radius=1,
        ),
    ),
    "ice_shard_staff": Gear(
        name="Ice Shard Staff",
        type=GearType.WEAPON,
        level=50,
        damage=10,
        intelligence=80,
        luck=10,
        attack_cooldown=30,
        crit_chance=25,
        strike_radius=5,
        gold_value=60,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Glacier Crash",
            description="Summons a glacier for huge damage.",
            damage=85,
            scaling_multiplier=1.25,
            spell_cooldown=35,
            cast_text="A glacier materializes above the enemy, and it crashes on them",
            strike_radius=1,
        ),
    ),
    "frozen_spell_blade": Gear(
        name="Frozen Spell Blade",
        type=GearType.WEAPON,
        level=50,
        damage=45,
        strength=15,
        intelligence=15,
        attack_cooldown=30,
        crit_chance=5,
        strike_radius=2,
        gold_value=60,
        spell=Spell(
            spell_type=SpellType.DAMAGE,
            name="Frost Magic Strike",
            description="Imbues frost magic into your blade to strike your enemies",
            damage=45,
            spell_cooldown=30,
            cast_text="The air grows cold as your strike you enemy.",
            strike_radius=5,
        ),
    ),
}

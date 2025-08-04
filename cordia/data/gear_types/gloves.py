from cordia.model.gear import Gear, GearType
from cordia.model.player_stats import PlayerStats

glove_data = {
    "leather_gloves": Gear(
        name="Leather Gloves",
        type=GearType.GLOVES,
        level=5,
        gold_value=25,
        stats=PlayerStats(strength=3, crit_chance=3),
    ),
    "stone_scale_gloves": Gear(
        name="Stone Scale Gloves",
        type=GearType.GLOVES,
        level=20,
        gold_value=40,
        stats=PlayerStats(strength=7, persistence=5, crit_chance=10),
    ),
    "frost_gloves": Gear(
        name="Frost Gloves",
        type=GearType.GLOVES,
        level=50,
        gold_value=50,
        stats=PlayerStats(intelligence=20, efficiency=5),
    ),
    "shadow_gloves": Gear(
        name="Shadow Gloves",
        type=GearType.GLOVES,
        level=50,
        gold_value=50,
        stats=PlayerStats(persistence=20, luck=5),
    ),
    "crystal_weave_gloves": Gear(
        name="Crystal Weave Gloves",
        type=GearType.GLOVES,
        level=70,
        gold_value=70,
        stats=PlayerStats(intelligence=20, efficiency=15),
    ),
    "royal_crystal_gloves": Gear(
        name="Royal Crystal Gloves",
        type=GearType.GLOVES,
        level=70,
        gold_value=100,
        stats=PlayerStats(intelligence=30, efficiency=30, strength=30, persistence=30),
    ),
    "void_gloves": Gear(
        name="Void Gloves",
        type=GearType.GLOVES,
        level=125,
        gold_value=100,
        stats=PlayerStats(
            boss_damage=15,
            crit_chance=5,
            damage=30,
            spell_damage=30,
        ),
        gear_set="void",
    ),
    "olympian_persistence_gloves": Gear(
        name="Olympian Persistence Gloves",
        type=GearType.GLOVES,
        level=250,
        gold_value=1000,
        stats=PlayerStats(persistence=50),
    ),
    "olympian_luck_gloves": Gear(
        name="Olympian Luck Gloves",
        type=GearType.GLOVES,
        level=250,
        gold_value=1000,
        stats=PlayerStats(luck=50),
    ),
    "olympian_strength_gloves": Gear(
        name="Olympian Strength Gloves",
        type=GearType.GLOVES,
        level=250,
        gold_value=1000,
        stats=PlayerStats(strength=50),
    ),
    "olympian_intelligence_gloves": Gear(
        name="Olympian Intelligence Gloves",
        type=GearType.GLOVES,
        level=250,
        gold_value=1000,
        stats=PlayerStats(intelligence=50),
    ),
}

from cordia.model.gear import Gear, GearType
from cordia.model.player_stats import PlayerStats

cape_data = {
    "rat_skin_cape": Gear(
        name="Rat Skin Cape",
        type=GearType.CAPE,
        level=5,
        gold_value=25,
        stats=PlayerStats(luck=3, efficiency=1),
    ),
    "vine_cloak": Gear(
        name="Vine Cloak",
        type=GearType.CAPE,
        level=15,
        gold_value=30,
        stats=PlayerStats(persistence=6, efficiency=10),
    ),
    "wyvern_wing_cape": Gear(
        name="Wyvern Wing Cape",
        type=GearType.CAPE,
        level=20,
        gold_value=40,
        stats=PlayerStats(persistence=12, efficiency=12),
    ),
    "frost_veil_cloak": Gear(
        name="Frost Veil Cloak",
        type=GearType.CAPE,
        level=50,
        gold_value=50,
        stats=PlayerStats(intelligence=20, efficiency=5),
    ),
    "shadow_cloak": Gear(
        name="Shadow Cloak",
        type=GearType.CAPE,
        level=50,
        gold_value=50,
        stats=PlayerStats(efficiency=5, persistence=20),
    ),
    "crystal_weave_cape": Gear(
        name="Crystal Weave Cape",
        type=GearType.CAPE,
        level=70,
        gold_value=70,
        stats=PlayerStats(efficiency=5, intelligence=30),
    ),
    "souless_cape": Gear(
        name="Souless Cape",
        type=GearType.CAPE,
        level=90,
        gold_value=70,
        stats=PlayerStats(efficiency=10, luck=10, persistence=10, strength=25),
    ),
    "void_cape": Gear(
        name="Void Cape",
        type=GearType.CAPE,
        level=125,
        gold_value=100,
        stats=PlayerStats(
            boss_damage=15,
            penetration=5,
            damage=30,
            spell_damage=30,
        ),
        gear_set="void",
    ),
}

from cordia.model.gear import Gear, GearType


cape_data = {
    "rat_skin_cape": Gear(
        name="Rat Skin Cape",
        type=GearType.CAPE,
        level=5,
        gold_value=25,
        luck=3,
        efficiency=1,
    ),
    "vine_cloak": Gear(
        name="Vine Cloak",
        type=GearType.CAPE,
        level=15,
        gold_value=30,
        persistence=6,
        efficiency=10,
    ),
    "wyvern_wing_cape": Gear(
        name="Wyvern Wing Cape",
        type=GearType.CAPE,
        persistence=12,
        efficiency=12,
        level=20,
        gold_value=40,
    ),
    "frost_veil_cloak": Gear(
        name="Frost Veil Cloak",
        type=GearType.CAPE,
        intelligence=20,
        efficiency=5,
        level=50,
        gold_value=50,
    ),
    "shadow_cloak": Gear(
        name="Shadow Cloak",
        type=GearType.CAPE,
        efficiency=5,
        persistence=20,
        level=50,
        gold_value=50,
    ),
    "crystal_weave_cape": Gear(
        name="Crystal Weave Cape",
        type=GearType.CAPE,
        efficiency=5,
        intelligence=30,
        level=70,
        gold_value=70,
    ),
    "souless_cape": Gear(
        name="Souless Cape",
        type=GearType.CAPE,
        efficiency=10,
        luck=10,
        persistence=10,
        strength=25,
        level=90,
        gold_value=70,
    ),
}

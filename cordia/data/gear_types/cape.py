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
        efficiency=9,
    ),
    "wyvern_wing_cape": Gear(
        name="Wyvern Wing Cape",
        type=GearType.CAPE,
        persistence=6,
        efficiency=6,
        level=20,
        gold_value=40,
    ),
    "frost_veil_cloak": Gear(
        name="Frost Veil Cloak",
        type=GearType.CAPE,
        intelligence=15,
        efficiency=6,
        level=50,
        gold_value=50,
    ),
    "shadow_cloak": Gear(
        name="Shadow Cloak",
        type=GearType.CAPE,
        efficiency=15,
        persistence=8,
        level=50,
        gold_value=50,
    ),
}

from cordia.model.gear import Gear, GearType


top_data = {
    "leather_vest": Gear(
        name="Leather Vest",
        type=GearType.TOP,
        level=5,
        gold_value=25,
        strength=3,
        luck=2,
    ),
    "thick_fat_vest": Gear(
        name="Thick Fat Vest",
        type=GearType.TOP,
        level=10,
        gold_value=25,
        strength=10,
    ),
    "stone_plated_chestplate": Gear(
        name="Stone Plated Chestplate",
        type=GearType.TOP,
        level=20,
        gold_value=40,
        strength=20,
    ),
    "leafy_top": Gear(
        name="Leafy Top",
        type=GearType.TOP,
        level=40,
        gold_value=40,
        strength=20,
        intelligence=20,
    ),
    "ice_crystal_chestplate": Gear(
        name="Ice Crystal Chestplate",
        type=GearType.TOP,
        level=50,
        gold_value=40,
        strength=30,
        intelligence=30,
    ),
    "shadow_master_top": Gear(
        name="Shadow Master Top",
        type=GearType.TOP,
        level=60,
        gold_value=100,
        efficiency=30,
        luck=30,
        persistence=60,
        boss_damage=10,
        gear_set="shadow_master",
        upgrade_item="shadow_master_soul",
    ),
}

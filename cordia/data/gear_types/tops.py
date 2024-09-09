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
        strength=9,
    ),
    "stone_plated_chestplate": Gear(
        name="Stone Plated Chestplate",
        type=GearType.TOP,
        level=20,
        gold_value=40,
        strength=15,
    ),
}

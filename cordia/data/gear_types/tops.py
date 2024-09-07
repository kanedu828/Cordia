from cordia.model.gear import Gear, GearType


top_data = {
    "leather_vest": Gear(
        name="Leather Vest",
        type=GearType.TOP,
        level=5,
        gold_value=25,
        strength=2,
        luck=2,
    ),
    "thick_fat_vest": Gear(
        name="Thick Fat Vest",
        type=GearType.TOP,
        level=10,
        gold_value=25,
        strength=6,
    )
}

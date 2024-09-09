from cordia.model.gear import Gear, GearType


shoes_data = {
    "leather_shoes": Gear(
        name="Leather Shoes",
        type=GearType.SHOES,
        level=5,
        gold_value=25,
        luck=3,
    ),
    "troll_shoes": Gear(
        name="Troll Shoes",
        type=GearType.SHOES,
        level=20,
        strength=15,
        gold_value=40,
    ),
}

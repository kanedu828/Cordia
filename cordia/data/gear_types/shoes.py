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
    "snow_shoes": Gear(
        name="Snow Shoes",
        type=GearType.SHOES,
        level=50,
        strength=12,
        persistence=6,
        efficiency=6,
        gold_value=50,
    ),
    "crystal_boots": Gear(
        name="Crystal Boots",
        type=GearType.SHOES,
        level=70,
        efficiency=25,
        strength=25,
        gold_value=50,
    ),
}

from cordia.model.gear import Gear, GearType


pants_data = {
    "leather_pants": Gear(
        name="Leather Pants",
        type=GearType.PANTS,
        level=5,
        gold_value=25,
        strength=1,
        luck=2,
    ),
    "goblin_king_pants": Gear(
        name="Goblin King Pants",
        type=GearType.PANTS,
        level=20,
        gold_value=50,
        strength=4,
        luck=10,
    ),
}

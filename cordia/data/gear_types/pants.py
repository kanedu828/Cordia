from cordia.model.gear import Gear, GearType


pants_data = {
    "leather_pants": Gear(
        name="Leather Pants",
        type=GearType.PANTS,
        level=5,
        gold_value=25,
        strength=1,
        luck=3,
    ),
    "goblin_king_pants": Gear(
        name="Goblin King Pants",
        type=GearType.PANTS,
        level=20,
        gold_value=50,
        strength=9,
        luck=12,
    ),
    "troll_pants": Gear(
        name="Troll Pants",
        type=GearType.PANTS,
        level=20,
        gold_value=40,
        strength=12,
    ),
    "leafy_pants": Gear(
        name="Leafy Pants",
        type=GearType.PANTS,
        level=40,
        gold_value=40,
        efficiency=9,
        luck=7,
    ),
    "shadow_pants": Gear(
        name="Shadow Pants",
        type=GearType.PANTS,
        level=50,
        gold_value=50,
        efficiency=12,
        persistence=8,
    ),
}

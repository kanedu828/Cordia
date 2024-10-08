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
        strength=12,
        luck=12,
    ),
    "troll_pants": Gear(
        name="Troll Pants",
        type=GearType.PANTS,
        level=20,
        gold_value=40,
        strength=20,
    ),
    "leafy_pants": Gear(
        name="Leafy Pants",
        type=GearType.PANTS,
        level=40,
        gold_value=40,
        efficiency=20,
        luck=20,
    ),
    "shadow_pants": Gear(
        name="Shadow Pants",
        type=GearType.PANTS,
        level=50,
        gold_value=50,
        efficiency=20,
        persistence=30,
    ),
    "shadow_master_pants": Gear(
        name="Shadow Master Pants",
        type=GearType.PANTS,
        level=60,
        gold_value=100,
        efficiency=30,
        luck=30,
        persistence=55,
        gear_set="shadow_master",
        upgrade_item="shadow_master_soul",
    ),
    "volcanic_pants": Gear(
        name="Volcanic Pants",
        type=GearType.PANTS,
        level=80,
        gold_value=100,
        strength=90,
        upgrade_item="volcanic_salamander_tail",
    ),
}

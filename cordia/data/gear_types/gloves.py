from cordia.model.gear import Gear, GearType


glove_data = {
    "leather_gloves": Gear(
        name="Leather Gloves",
        type=GearType.GLOVES,
        strength=3,
        level=5,
        gold_value=25,
        crit_chance=3,
    ),
    "stone_scale_gloves": Gear(
        name="Stone Scale Gloves",
        type=GearType.GLOVES,
        strength=6,
        level=20,
        gold_value=40,
        crit_chance=10,
    ),
}

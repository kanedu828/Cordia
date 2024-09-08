from cordia.model.gear import Gear, GearType


glove_data = {
    "leather_gloves": Gear(
        name="Leather Gloves",
        type=GearType.GLOVES,
        strength=3,
        level=5,
        gold_value=25,
        crit_chance=3,
    )
}

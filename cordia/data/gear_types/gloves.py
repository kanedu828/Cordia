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
    "frost_gloves": Gear(
        name="Frost Gloves",
        type=GearType.GLOVES,
        intelligence=18,
        efficiency=7,
        level=50,
        gold_value=50,
    ),
    "shadow_gloves": Gear(
        name="Shadow Gloves",
        type=GearType.GLOVES,
        persistence=15,
        efficiency=7,
        level=50,
        gold_value=50,
    ),
}

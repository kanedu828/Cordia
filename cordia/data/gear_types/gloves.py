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
        strength=7,
        persistence=5,
        level=20,
        gold_value=40,
        crit_chance=10,
    ),
    "frost_gloves": Gear(
        name="Frost Gloves",
        type=GearType.GLOVES,
        intelligence=20,
        efficiency=5,
        level=50,
        gold_value=50,
    ),
    "shadow_gloves": Gear(
        name="Shadow Gloves",
        type=GearType.GLOVES,
        persistence=20,
        luck=5,
        level=50,
        gold_value=50,
    ),
    "crystal_weave_gloves": Gear(
        name="Crystal Weave Gloves",
        type=GearType.GLOVES,
        intelligence=20,
        efficiency=15,
        level=70,
        gold_value=70,
    ),
    "royal_crystal_gloves": Gear(
        name="Royal Crystal Gloves",
        type=GearType.GLOVES,
        level=70,
        intelligence=30,
        efficiency=30,
        strength=30,
        persistence=30,
        gold_value=100,
    )
}

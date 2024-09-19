from cordia.model.gear import Gear, GearType


hat_data = {
    "leather_hat": Gear(
        name="Leather Hat",
        type=GearType.HAT,
        level=5,
        gold_value=25,
        luck=3,
    ),
    "wolf_cap": Gear(
        name="Wolf Cap",
        type=GearType.HAT,
        level=10,
        strength=5,
        persistence=3,
        gold_value=25,
    ),
    "stone_plated_helmet": Gear(
        name="Stone Plated Helmet",
        type=GearType.HAT,
        level=20,
        strength=20,
        gold_value=40,
    ),
    "flower_crown": Gear(
        name="Flower Crown",
        type=GearType.HAT,
        level=40,
        intelligence=30,
        luck=10,
        gold_value=45,
    ),
    "shadow_hood": Gear(
        name="Shadow Hood",
        type=GearType.HAT,
        level=50,
        efficiency=18,
        luck=10,
        persistence=22,
        gold_value=50,
    ),
    "frost_hood": Gear(
        name="Frost Hood",
        type=GearType.HAT,
        level=50,
        intelligence=35,
        persistence=15,
        gold_value=50,
    ),
    "crystal_helmet": Gear(
        name="Crystal Helmet",
        type=GearType.HAT,
        level=70,
        intelligence=50,
        efficiency=20,
        gold_value=70,
    ),
    "royal_crystal_helmet": Gear(
        name="Royal Crystal Helmet",
        type=GearType.HAT,
        level=70,
        intelligence=40,
        efficiency=40,
        strength=40,
        persistence=40,
        gold_value=100,
    )
}

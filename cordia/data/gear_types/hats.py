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
        strength=15,
        gold_value=40,
    ),
}

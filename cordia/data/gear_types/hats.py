from cordia.model.gear import Gear, GearType


hat_data = {
    "leather_hat": Gear(
        name="Leather Hat",
        type=GearType.HAT,
        level=5,
        gold_value=25,
        luck=2,
    ),
    "wolf_cap": Gear(
        name="Wolf Cap",
        type=GearType.HAT,
        level=10,
        strength=4,
        persistence=2,
        gold_value=25,
    ),
}

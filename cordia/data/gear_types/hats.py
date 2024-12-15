from cordia.model.gear import Gear, GearType
from cordia.model.player_stats import PlayerStats

hat_data = {
    "leather_hat": Gear(
        name="Leather Hat",
        type=GearType.HAT,
        level=5,
        gold_value=25,
        stats=PlayerStats(luck=3),
    ),
    "wolf_cap": Gear(
        name="Wolf Cap",
        type=GearType.HAT,
        level=10,
        gold_value=25,
        stats=PlayerStats(strength=5, persistence=3),
    ),
    "stone_plated_helmet": Gear(
        name="Stone Plated Helmet",
        type=GearType.HAT,
        level=20,
        gold_value=40,
        stats=PlayerStats(strength=20),
    ),
    "flower_crown": Gear(
        name="Flower Crown",
        type=GearType.HAT,
        level=40,
        gold_value=45,
        stats=PlayerStats(intelligence=30, luck=10),
    ),
    "shadow_hood": Gear(
        name="Shadow Hood",
        type=GearType.HAT,
        level=50,
        gold_value=50,
        stats=PlayerStats(efficiency=18, luck=10, persistence=22),
    ),
    "frost_hood": Gear(
        name="Frost Hood",
        type=GearType.HAT,
        level=50,
        gold_value=50,
        stats=PlayerStats(intelligence=35, persistence=15),
    ),
    "crystal_helmet": Gear(
        name="Crystal Helmet",
        type=GearType.HAT,
        level=70,
        gold_value=70,
        stats=PlayerStats(intelligence=50, efficiency=20),
    ),
    "royal_crystal_helmet": Gear(
        name="Royal Crystal Helmet",
        type=GearType.HAT,
        level=70,
        gold_value=100,
        stats=PlayerStats(intelligence=20, efficiency=20, strength=50, persistence=20),
    ),
    "mystical_guardian_mage_hat": Gear(
        name="Mystical Guardian Mage Hat",
        type=GearType.HAT,
        level=125,
        gold_value=500,
        stats=PlayerStats(intelligence=125),
        upgrade_item="mystical_guardian_soul",
        gear_set="mystical_guardian",
    ),
    "mystical_guardian_hunter_hat": Gear(
        name="Mystical Guardian Hunter Hat",
        type=GearType.HAT,
        level=125,
        gold_value=500,
        stats=PlayerStats(persistence=125),
        upgrade_item="mystical_guardian_soul",
        gear_set="mystical_guardian",
    ),
    "gamblers_hat": Gear(
        name="Gamblers Hat",
        type=GearType.HAT,
        level=125,
        gold_value=500,
        stats=PlayerStats(luck=125),
        gear_set="gamblers",
    ),
    "ancient_ocean_guardian_warrior_hat": Gear(
        name="Ancient Ocean Guardian Warrior Hat",
        type=GearType.HAT,
        level=125,
        gold_value=500,
        stats=PlayerStats(strength=125),
        upgrade_item="ancient_ocean_guardian_soul",
        gear_set="ancient_ocean_guardian",
    ),
    "ancient_ocean_guardian_assassin_hat": Gear(
        name="Ancient Ocean Guardian Assassin Hat",
        type=GearType.HAT,
        level=125,
        gold_value=500,
        stats=PlayerStats(efficiency=125),
        upgrade_item="ancient_ocean_guardian_soul",
        gear_set="ancient_ocean_guardian",
    ),
}

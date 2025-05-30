from cordia.model.gear import Gear, GearType
from cordia.model.player_stats import PlayerStats

pants_data = {
    "leather_pants": Gear(
        name="Leather Pants",
        type=GearType.PANTS,
        level=5,
        gold_value=25,
        stats=PlayerStats(strength=1, luck=3),
    ),
    "goblin_king_pants": Gear(
        name="Goblin King Pants",
        type=GearType.PANTS,
        level=20,
        gold_value=50,
        stats=PlayerStats(strength=12, luck=12),
    ),
    "troll_pants": Gear(
        name="Troll Pants",
        type=GearType.PANTS,
        level=20,
        gold_value=40,
        stats=PlayerStats(strength=20),
    ),
    "leafy_pants": Gear(
        name="Leafy Pants",
        type=GearType.PANTS,
        level=40,
        gold_value=40,
        stats=PlayerStats(efficiency=20, luck=20),
    ),
    "shadow_pants": Gear(
        name="Shadow Pants",
        type=GearType.PANTS,
        level=50,
        gold_value=50,
        stats=PlayerStats(efficiency=20, persistence=30),
    ),
    "shadow_master_pants": Gear(
        name="Shadow Master Pants",
        type=GearType.PANTS,
        level=60,
        gold_value=100,
        stats=PlayerStats(efficiency=30, luck=30, persistence=55),
        gear_set="shadow_master",
        upgrade_item="shadow_master_soul",
    ),
    "volcanic_pants": Gear(
        name="Volcanic Pants",
        type=GearType.PANTS,
        level=80,
        gold_value=100,
        stats=PlayerStats(strength=90),
        upgrade_item="volcanic_salamander_tail",
    ),
    "mystical_guardian_mage_pants": Gear(
        name="Mystical Guardian Mage Pants",
        type=GearType.PANTS,
        level=125,
        gold_value=500,
        stats=PlayerStats(intelligence=200, spell_damage=10),
        upgrade_item="mystical_guardian_soul",
        gear_set="mystical_guardian",
    ),
    "mystical_guardian_hunter_pants": Gear(
        name="Mystical Guardian Hunter Pants",
        type=GearType.PANTS,
        level=125,
        gold_value=500,
        stats=PlayerStats(persistence=200, damage=10),
        upgrade_item="mystical_guardian_soul",
        gear_set="mystical_guardian",
    ),
    "gamblers_pants": Gear(
        name="Gamblers Pants",
        type=GearType.PANTS,
        level=125,
        gold_value=500,
        stats=PlayerStats(luck=125),
        gear_set="gamblers",
    ),
    "ancient_ocean_guardian_warrior_pants": Gear(
        name="Ancient Ocean Guardian Warrior Pants",
        type=GearType.PANTS,
        level=125,
        gold_value=500,
        stats=PlayerStats(strength=125, damage=10),
        upgrade_item="ancient_ocean_guardian_soul",
        gear_set="ancient_ocean_guardian",
    ),
    "ancient_ocean_guardian_assassin_pants": Gear(
        name="Ancient Ocean Guardian Assassin Pants",
        type=GearType.PANTS,
        level=125,
        gold_value=500,
        stats=PlayerStats(efficiency=125, damage=10),
        upgrade_item="ancient_ocean_guardian_soul",
        gear_set="ancient_ocean_guardian",
    ),
}

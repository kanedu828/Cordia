from cordia.model.gear import Gear, GearType
from cordia.model.player_stats import PlayerStats

pendant_data = {
    "red_eye_pendant": Gear(
        name="Red Eye Pendant",
        type=GearType.PENDANT,
        level=10,
        gold_value=25,
        stats=PlayerStats(intelligence=6),
    ),
    "polished_stone_pendant": Gear(
        name="Polished Stone Pendant",
        type=GearType.PENDANT,
        level=20,
        gold_value=40,
        stats=PlayerStats(strength=10, persistence=5),
    ),
    "tangling_choker": Gear(
        name="Tangling Choker",
        type=GearType.PENDANT,
        level=40,
        gold_value=45,
        stats=PlayerStats(strength=15, luck=5),
    ),
    "shadow_pendant": Gear(
        name="Shadow Pendant",
        type=GearType.PENDANT,
        level=50,
        gold_value=50,
        stats=PlayerStats(persistence=20, efficiency=5),
    ),
    "ice_queen_pendant": Gear(
        name="Ice Queen Pendant",
        type=GearType.PENDANT,
        level=60,
        gold_value=100,
        stats=PlayerStats(
            persistence=20,
            efficiency=20,
            intelligence=30,
            boss_damage=10,
        ),
        gear_set="ice_queen",
        upgrade_item="ice_queen_soul",
    ),
    "soul_stealer_pendant": Gear(
        name="Soul Stealer Pendant",
        type=GearType.PENDANT,
        level=100,
        gold_value=100,
        stats=PlayerStats(
            persistence=40,
            strength=40,
            intelligence=40,
            boss_damage=10,
            crit_chance=10,
            damage=10,
        ),
        upgrade_item="soul_stealer_soul",
        gear_set="soul_stealer",
    ),
    "void_pendant": Gear(
        name="Void Pendant",
        type=GearType.PENDANT,
        level=125,
        gold_value=100,
        stats=PlayerStats(
            boss_damage=15,
            damage=30,
            spell_damage=30,
        ),
        gear_set="void",
    ),
}

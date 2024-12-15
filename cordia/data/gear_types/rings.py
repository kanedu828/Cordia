from cordia.model.gear import Gear, GearType
from cordia.model.player_stats import PlayerStats

ring_data = {
    "red_eye_ring": Gear(
        name="Red Eye Ring",
        type=GearType.RING,
        level=10,
        gold_value=25,
        stats=PlayerStats(intelligence=6),
    ),
    "polished_stone_ring": Gear(
        name="Polished Stone Ring",
        type=GearType.RING,
        level=20,
        gold_value=45,
        stats=PlayerStats(strength=10),
    ),
    "hibiscus_ring": Gear(
        name="Hibiscus Ring",
        type=GearType.RING,
        level=40,
        gold_value=45,
        stats=PlayerStats(strength=5, intelligence=15),
    ),
    "ice_crystal_ring": Gear(
        name="Ice Crystal Ring",
        type=GearType.RING,
        level=50,
        gold_value=50,
        stats=PlayerStats(intelligence=20, luck=5),
    ),
    "ice_queen_ring": Gear(
        name="Ice Queen Ring",
        type=GearType.RING,
        level=60,
        gold_value=100,
        stats=PlayerStats(
            intelligence=35,
            efficiency=20,
            crit_chance=7,
        ),
        gear_set="ice_queen",
        upgrade_item="ice_queen_soul",
    ),
    "soul_stealer_ring": Gear(
        name="Soul Stealer Ring",
        type=GearType.RING,
        level=100,
        gold_value=100,
        stats=PlayerStats(
            persistence=40,
            strength=40,
            intelligence=40,
            boss_damage=10,
            damage=10,
        ),
        upgrade_item="soul_stealer_soul",
        gear_set="soul_stealer",
    ),
    "void_ring": Gear(
        name="Void Ring",
        type=GearType.RING,
        level=125,
        gold_value=100,
        stats=PlayerStats(
            boss_damage=25,
            damage=30,
            spell_damage=30,
        ),
        gear_set="void",
    ),
}

from cordia.model.gear import Gear, GearType


ring_data = {
    "red_eye_ring": Gear(
        name="Red Eye Ring",
        type=GearType.RING,
        level=10,
        gold_value=25,
        intelligence=6,
    ),
    "polished_stone_ring": Gear(
        name="Polished Stone Ring",
        type=GearType.RING,
        level=20,
        gold_value=45,
        strength=10,
    ),
    "hibiscus_ring": Gear(
        name="Hibiscus Ring",
        type=GearType.RING,
        level=40,
        gold_value=45,
        strength=5,
        intelligence=15,
    ),
    "ice_crystal_ring": Gear(
        name="Ice Crystal Ring",
        type=GearType.RING,
        level=50,
        gold_value=50,
        intelligence=20,
        luck=5,
    ),
    "ice_queen_ring": Gear(
        name="Ice Queen Ring",
        type=GearType.RING,
        level=60,
        gold_value=100,
        intelligence=35,
        efficiency=20,
        crit_chance=7,
        gear_set="ice_queen",
        upgrade_item="ice_queen_soul",
    ),
}

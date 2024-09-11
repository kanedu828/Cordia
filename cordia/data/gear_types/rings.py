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
        strength=6,
    ),
    "ice_crystal_ring": Gear(
        name="Ice Crystal Ring",
        type=GearType.RING,
        level=50,
        gold_value=50,
        intelligence=10,
    ),
}

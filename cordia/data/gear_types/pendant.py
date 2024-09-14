from cordia.model.gear import Gear, GearType


pendant_data = {
    "red_eye_pendant": Gear(
        name="Red Eye Pendant",
        type=GearType.PENDANT,
        level=10,
        gold_value=25,
        intelligence=6,
    ),
    "polished_stone_pendant": Gear(
        name="Polished Stone Pendant",
        type=GearType.PENDANT,
        level=20,
        gold_value=40,
        strength=6,
    ),
    "tangling_choker": Gear(
        name="Tangling Choker",
        type=GearType.PENDANT,
        level=40,
        gold_value=45,
        strength=10,
    ),
    "shadow_pendant": Gear(
        name="Shadow Pendant",
        type=GearType.PENDANT,
        level=50,
        gold_value=50,
        persistence=6,
        efficiency=6,
    ),
    "ice_queen_pendant": Gear(
        name="Ice Queen Pendant",
        type=GearType.PENDANT,
        level=60,
        gold_value=100,
        persistence=6,
        efficiency=30,
        intelligence=30,
        boss_damage=10,
        gear_set="ice_queen",
        upgrade_item="ice_queen_soul",
    ),
}

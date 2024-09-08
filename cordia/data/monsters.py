from cordia.model.monster import Monster

monster_data = {
    "rat": Monster(
        name="Rat", level=1, hp=10, gold=2, exp=5, gear_loot=[("rat_skin_cape", 0.02)]
    ),
    "goblin": Monster(
        name="Goblin",
        level=5,
        hp=15,
        gold=5,
        exp=8,
        gear_loot=[
            ("leather_vest", 0.02),
            ("leather_pants", 0.02),
            ("leather_shoes", 0.02),
            ("leather_gloves", 0.02),
            ("leather_hat", 0.02),
            ("basic_sword", 0.05),
            ("basic_wand", 0.05),
            ("basic_dagger", 0.05),
            ("basic_bow", 0.05),
            ("goblin_dagger", 0.02),
        ],
    ),
    "wolf": Monster(
        name="Wolf",
        level=13,
        hp=20,
        gold=9,
        exp=15,
        gear_loot=[("wolf_fang_sword", 0.02), ("wolf_cap", 0.02), ("hunter_bow", 0.02)],
    ),
    "bear": Monster(
        name="Bear",
        level=18,
        hp=33,
        gold=10,
        exp=25,
        gear_loot=[("hunter_bow", 0.02), ("thick_fat_vest", 0.02)],
    ),
    "giant_spider": Monster(
        name="Giant Spider",
        level=25,
        hp=50,
        gold=20,
        exp=35,
        gear_loot=[("red_eye_wand", 0.02), ("red_eye_ring", 0.02)],
    ),
    "dryad": Monster(
        name="Dryad",
        level=45,
        hp=120,
        gold=50,
        exp=60,
        gear_loot=[("ancient_forest_sword", 0.20)],
    ),
}

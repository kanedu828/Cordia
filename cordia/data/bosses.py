from cordia.model.monster import Monster

boss_data = {
    "goblin_king": Monster(
        name="Goblin King",
        level=20,
        hp=1250,
        gold=75,
        exp=150,
        defense=10,
        gear_loot=[
            ("leather_vest", 0.40),
            ("leather_pants", 0.40),
            ("leather_shoes", 0.40),
            ("leather_gloves", 0.40),
            ("goblin_dagger", 0.40),
            ("goblin_king_pants", 0.30),
        ],
    ),
    "ancient_treant": Monster(
        name="Ancient Treant",
        level=35,
        hp=2000,
        gold=125,
        exp=300,
        defense=25,
        resistance=25,
        gear_loot=[
            ("red_eye_ring", 0.40),
            ("hunter_bow", 0.40),
            ("red_eye_wand", 0.40),
            ("thick_fat_vest", 0.40),
            ("red_eye_pendant", 0.40),
            ("wolf_cap", 0.40),
            ("vine_cloak", 0.30),
            ("ancient_forest_sword", 0.20),
        ],
    ),
}

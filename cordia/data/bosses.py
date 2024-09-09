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
            ("hunter_bow", 0.40),
            ("vine_cloak", 0.30),
            ("ancient_forest_sword", 0.20),
        ],
    ),
    "mountain_behemoth": Monster(
        name="Mountain Behemoth",
        level=50,
        hp=5000,
        gold=250,
        exp=650,
        defense=50,
        gear_loot=[
            ("earth_elemental_staff", 0.10),
            ("stone_plated_chestplate", 0.30),
            ("stone_plated_helmet", 0.30),
            ("polished_stone_ring", 0.30),
            ("polished_stone_pendant", 0.30),
            ("mountain_breaker_blade", 0.10),
        ],
    ),
}

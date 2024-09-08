from cordia.model.monster import Monster

boss_data = {
    "goblin_king": Monster(
        name="Goblin King",
        level=20,
        hp=500,
        gold=75,
        exp=150,
        defense=10,
        gear_loot=[
            ("leather_vest", 0.20),
            ("leather_pants", 0.20),
            ("leather_shoes", 0.20),
            ("leather_gloves", 0.20),
            ("goblin_dagger", 0.20),
            ("goblin_king_pants", 0.10),
        ],
    ),
}

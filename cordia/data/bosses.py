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
            ("goblin_king_pants", 0.40),
        ],
    ),
}

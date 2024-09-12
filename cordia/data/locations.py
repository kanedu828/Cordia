from cordia.model.location import Location

location_data = {
    "the_plains_i": Location(
        name="The Plains I", level_unlock=0, monsters=[("rat", 0.75), ("goblin", 0.25)]
    ),
    "the_plains_ii": Location(
        name="The Plains II", level_unlock=5, monsters=[("goblin", 0.75), ("bandit", 0.25)]
    ),
    "the_plains_iii": Location(
        name="The Plains III",
        level_unlock=10,
        monsters=[("goblin", 0.25), ("bandit", 0.75)],
    ),
    "the_forest_i": Location(
        name="The Forest I", level_unlock=15, monsters=[("wolf", 0.70), ("bear", 0.30)]
    ),
    "the_forest_ii": Location(
        name="The Forest II",
        level_unlock=20,
        monsters=[("bear", 0.60), ("giant_spider", 0.40)],
    ),
    "the_forest_iii": Location(
        name="The Forest III",
        level_unlock=25,
        monsters=[("giant_spider", 0.95), ("dryad", 0.05)],
    ),
    "the_mountains_i": Location(
        name="The Mountains I",
        level_unlock=30,
        monsters=[("rock_golem", 0.40), ("wyvern", 0.40), ("mountain_troll", 0.20)],
    ),
    "the_mountains_ii": Location(
        name="The Mountains II",
        level_unlock=40,
        monsters=[
            ("mountain_troll", 0.15),
            ("stone_drake", 0.45),
            ("earth_elemental", 0.38),
            ("cave_wyrm", 0.02),
        ],
    ),
    "philpots_garden": Location(
        name="Philpots Garden",
        level_unlock=50,
        monsters=[
            ("brussel_sprout", 0.7),
            ("tangling_hibiscus", 0.3)
        ]
    ),
    "shadowreach_cavern": Location(
        name="Shadowreach Cavern",
        level_unlock=60,
        monsters=[
            ("cave_stalker", 0.6),
            ("cave_phantom", 0.3),
            ("shadewalker", 0.1)
        ]
    ),
    "frostveil_expanse": Location(
        name="Frostveil Expanse",
        level_unlock=70,
        monsters=[
            ("snowstalker_wolf", 0.6),
            ("glacial_wraith", 0.3),
            ("frost_elemental", 0.1)
        ]
    ),
}

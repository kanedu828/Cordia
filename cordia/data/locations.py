from cordia.model.location import Location

location_data = {
    "the_plains_i": Location(
        name="The Plains I", level_unlock=0, monsters=[("rat", 0.75), ("goblin", 0.25)]
    ),
    "the_plains_ii": Location(
        name="The Plains II",
        level_unlock=5,
        monsters=[("goblin", 0.75), ("bandit", 0.25)],
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
        monsters=[("brussel_sprout", 0.7), ("tangling_hibiscus", 0.3)],
    ),
    "shadowreach_cavern": Location(
        name="Shadowreach Cavern",
        level_unlock=60,
        monsters=[("cave_stalker", 0.6), ("cave_phantom", 0.3), ("shadewalker", 0.1)],
    ),
    "frostveil_expanse": Location(
        name="Frostveil Expanse",
        level_unlock=70,
        monsters=[
            ("snowstalker_wolf", 0.6),
            ("glacial_wraith", 0.3),
            ("frost_elemental", 0.1),
        ],
    ),
    "crystal_lake": Location(
        name="Crystal Lake",
        level_unlock=80,
        monsters=[
            ("crystal_warrior", 0.3),
            ("crystal_reptile", 0.7),
        ],
    ),
    "volcanic_wasteland": Location(
        name="Volcanic Wasteland",
        level_unlock=90,
        monsters=[
            ("volcanic_salamander", 1.0),
        ],
    ),
    "desolate_plains": Location(
        name="Desolate Plains",
        level_unlock=100,
        monsters=[("souless_wanderer", 0.4), ("souless_scorpion", 0.6)],
    ),
    "mystical_forest": Location(
        name="Mystical Forest",
        level_unlock=125,
        monsters=[("eldergrove_spirit", 0.95), ("blossomthorn_fairy", 0.05)],
    ),
    "ancient_ocean_ruins": Location(
        name="Ancient Ocean Ruins",
        level_unlock=150,
        monsters=[("ancient_shark", 0.95), ("ancient_giant_squid", 0.05)],
    ),
    "the_void": Location(
        name="The Void", level_unlock=175, monsters=[("void_entity", 1.00)]
    ),
}

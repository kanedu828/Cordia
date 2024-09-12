from cordia.model.monster import Monster

monster_data = {
    "rat": Monster(
        name="Rat", level=1, hp=5, gold=2, exp=5, gear_loot=[("rat_skin_cape", 0.02)]
    ),
    "goblin": Monster(
        name="Goblin",
        level=5,
        hp=13,
        gold=5,
        exp=10,
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
    "bandit": Monster(
        name="Bandit",
        level=10,
        hp=20,
        gold=5,
        exp=20,
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
        level=17,
        hp=28,
        gold=10,
        exp=25,
        gear_loot=[("wolf_fang_sword", 0.02), ("wolf_cap", 0.02), ("hunter_bow", 0.02), ("wolf_fang_dagger", 0.02)],
    ),
    "bear": Monster(
        name="Bear",
        level=23,
        hp=43,
        gold=18,
        exp=36,
        gear_loot=[("hunter_bow", 0.02), ("thick_fat_vest", 0.02)],
    ),
    "giant_spider": Monster(
        name="Giant Spider",
        level=30,
        hp=55,
        gold=24,
        exp=48,
        gear_loot=[("red_eye_wand", 0.02), ("red_eye_ring", 0.02)],
    ),
    "rock_golem": Monster(
        name="Rock Golem",
        level=35,
        hp=75,
        gold=30,
        exp=67,
        defense=20,
        gear_loot=[("polished_stone_ring", 0.02), ("polished_stone_pendant", 0.02)],
    ),
    "wyvern": Monster(
        name="Wyvern",
        level=38,
        hp=72,
        gold=30,
        exp=65,
        defense=10,
        resistance=10,
        gear_loot=[("wyvern_tooth_dagger", 0.02), ("wyvern_wing_cape", 0.02)],
    ),
    "mountain_troll": Monster(
        name="Mountain Troll",
        level=40,
        hp=86,
        gold=73,
        exp=73,
        defense=10,
        gear_loot=[("troll_shoes", 0.02), ("troll_pants", 0.02)],
    ),
    "dryad": Monster(
        name="Dryad",
        level=45,
        hp=250,
        gold=100,
        exp=232,
        gear_loot=[
            ("ancient_forest_sword", 0.20),
        ],
        item_loot=[
            ("supreme_core", 0.10),
            ("chaos_core", 0.05),
        ],
    ),
    "stone_drake": Monster(
        name="Stone Drake",
        level=45,
        hp=102,
        gold=42,
        exp=93,
        defense=20,
        gear_loot=[("stone_scale_gloves", 0.02), ("stone_plated_helmet", 0.02)],
    ),
    "earth_elemental": Monster(
        name="Earth Elemental",
        level=48,
        hp=132,
        gold=51,
        exp=121,
        defense=25,
        gear_loot=[("earth_elemental_staff", 0.02), ("stone_plated_chestplate", 0.02)],
    ),
    "brussel_sprout": Monster(
        name="Brussel Sprout",
        level=53,
        hp=110,
        gold=40,
        exp=95,
        resistance=10,
        gear_loot=[
            ("thorny_dagger", 0.02),
            ("staff_of_roots", 0.02),
            ("leafy_top", 0.02),
            ("leafy_pants", 0.02)
        ]
    ),
    "tangling_hibiscus": Monster(
        name="Tangling Hibiscus",
        level=56,
        hp=120,
        gold=42,
        exp=100,
        defense=5,
        resistance=20,
        gear_loot=[
            ("tangling_choker", 0.02),
            ("flower_crown", 0.02),
            ("hibiscus_ring", 0.02)
        ]
    ),
    "cave_wyrm": Monster(
        name="Cave Wyrm",
        level=70,
        hp=350,
        gold=120,
        exp=321,
        defense=10,
        resistance=10,
        gear_loot=[
            ("earth_elemental_staff", 0.10),
            ("wyrm_bow", 0.10),
        ],
        item_loot=[
            ("supreme_core", 0.10),
            ("chaos_core", 0.05),
        ],
    ),
    "cave_stalker": Monster(
        name="Cave Stalker",
        level=63,
        hp=550,
        gold=210,
        exp=520,
        defense=10,
        resistance=10,
        gear_loot=[
            ("shadow_hunter_bow", 0.02),
            ("shadow_gloves", 0.02),
            ("shadow_hood", 0.02),
            ("shadow_pants", 0.02)
        ]
    ),
    "cave_phantom": Monster(
        name="Cave Phantom",
        level=67,
        hp=520,
        gold=170,
        exp=500,
        resistance=40,
        gear_loot=[
            ("shadow_cloak", 0.025),
            ("shadow_gloves", 0.02),
            ("shadow_hood", 0.02),
            ("shadow_pants", 0.02),
            ("shadow_pendant", 0.02)
        ]
    ),
    "shadewalker": Monster(
        name="Shadewalker",
        level=74,
        hp=850,
        gold=360,
        exp=740,
        defense=15,
        resistance=50,
        gear_loot=[
            ("shadow_hunter_bow", 0.02),
            ("shadow_gloves", 0.02),
            ("shadow_hood", 0.02),
            ("shadow_pants", 0.02)
        ]
    ),
    "snowstalker_wolf": Monster(
        name="Snowstalker Wolf",
        level=75,
        hp=650,
        gold=240,
        exp=500,
        defense=15,
        gear_loot=[
            ("frostblade_dagger", 0.025),
            ("frost_gloves", 0.02),
            ("frost_hood", 0.02),
            ("frost_veil_cloak", 0.02),
            ("snow_shoes", 0.02)
        ]
    ),
    "glacial_wraith": Monster(
        name="Glacial Wraith",
        level=78,
        hp=580,
        gold=210,
        exp=500,
        resistance=30,
        gear_loot=[
            ("ice_shard_staff", 0.025),
            ("frozen_spell_blade", 0.025),
            ("frost_veil_cloak", 0.02),
            ("frost_gloves", 0.02),
            ("frost_hood", 0.02)
            
        ]
    ),
    "frost_elemental": Monster(
        name="Frost Elemental",
        level=85,
        hp=800,
        gold=300,
        exp=720,
        defense=50,
        gear_loot=[
            ("frozen_spell_blade", 0.02),
            ("ice_crystal_ring", 0.02),
            ("snow_shoes", 0.02),
            ("ice_crystal_chestplate", 0.02)
        ]
    ),
}

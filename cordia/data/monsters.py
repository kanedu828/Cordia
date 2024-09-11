from cordia.model.monster import Monster

monster_data = {
    "rat": Monster(
        name="Rat", level=1, hp=10, gold=2, exp=5, gear_loot=[("rat_skin_cape", 0.02)]
    ),
    "goblin": Monster(
        name="Goblin",
        level=5,
        hp=17,
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
        level=17,
        hp=35,
        gold=9,
        exp=12,
        gear_loot=[("wolf_fang_sword", 0.02), ("wolf_cap", 0.02), ("hunter_bow", 0.02)],
    ),
    "bear": Monster(
        name="Bear",
        level=23,
        hp=50,
        gold=10,
        exp=16,
        gear_loot=[("hunter_bow", 0.02), ("thick_fat_vest", 0.02)],
    ),
    "giant_spider": Monster(
        name="Giant Spider",
        level=30,
        hp=70,
        gold=20,
        exp=22,
        gear_loot=[("red_eye_wand", 0.02), ("red_eye_ring", 0.02)],
    ),
    "rock_golem": Monster(
        name="Rock Golem",
        level=35,
        hp=105,
        gold=30,
        exp=34,
        defense=20,
        gear_loot=[("polished_stone_ring", 0.05), ("polished_stone_pendant", 0.05)],
    ),
    "wyvern": Monster(
        name="Wyvern",
        level=38,
        hp=85,
        gold=27,
        exp=34,
        defense=10,
        resistance=10,
        gear_loot=[("wyvern_tooth_dagger", 0.05), ("wyvern_wing_cape", 0.05)],
    ),
    "mountain_troll": Monster(
        name="Mountain Troll",
        level=40,
        hp=120,
        gold=35,
        exp=40,
        defense=10,
        gear_loot=[("troll_shoes", 0.05), ("troll_pants", 0.05)],
    ),
    "stone_drake": Monster(
        name="Stone Drake",
        level=52,
        hp=125,
        gold=35,
        exp=40,
        defense=20,
        gear_loot=[("stone_scale_gloves", 0.05), ("stone_plated_helmet", 0.05)],
    ),
    "earth_elemental": Monster(
        name="Earth Elemental",
        level=55,
        hp=142,
        gold=35,
        exp=45,
        defense=25,
        gear_loot=[("earth_elemental_staff", 0.05), ("stone_plated_chestplate", 0.05)],
    ),
    "dryad": Monster(
        name="Dryad",
        level=45,
        hp=250,
        gold=50,
        exp=60,
        gear_loot=[
            ("ancient_forest_sword", 0.20),
        ],
        item_loot=[
            ("supreme_core", 0.10),
            ("chaos_core", 0.05),
        ],
    ),
    "cave_wyrm": Monster(
        name="Cave Wyrm",
        level=70,
        hp=350,
        gold=60,
        exp=120,
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
        level=74,
        hp=550,
        gold=85,
        exp=42,
        defense=10,
        resistance=10,
        gear_loot=[
            ("shadow_hunter_bow", 0.02),
            ("shadow_gloves", 0.05),
            ("shadow_hood", 0.05),
            ("shadow_pants", 0.05)
        ]
    ),
    "snowstalker_wolf": Monster(
        name="Snowstalker Wolf",
        level=75,
        hp=600,
        gold=20,
        exp=70,
        defense=15,
        gear_loot=[
            ("frostblade_dagger", 0.025),
            ("frost_gloves", 0.05),
            ("frost_hood", 0.05),
            ("frost_veil_cloak", 0.05),
            ("snow_shoes", 0.05)
        ]
    ),
    "cave_phantom": Monster(
        name="Cave Phantom",
        level=77,
        hp=550,
        gold=90,
        exp=40,
        resistance=40,
        gear_loot=[
            ("shadow_cloak", 0.025),
            ("shadow_gloves", 0.05),
            ("shadow_hood", 0.05),
            ("shadow_pants", 0.05),
            ("shadow_pendant", 0.05)
        ]
    ),
    "glacial_wraith": Monster(
        name="Glacial Wraith",
        level=78,
        hp=450,
        gold=30,
        exp=72,
        resistance=30,
        gear_loot=[
            ("ice_shard_staff", 0.025),
            ("frozen_spell_blade", 0.025),
            ("frost_veil_cloak", 0.05),
            ("frost_gloves", 0.05),
            ("frost_hood", 0.05)
            
        ]
    ),
    "frost_elemental": Monster(
        name="Frost Elemental",
        level=85,
        hp=800,
        gold=30,
        exp=75,
        defense=50,
        gear_loot=[
            ("frozen_spell_blade", 0.05),
            ("ice_crystal_ring", 0.05),
            ("snow_shoes", 0.05),
            ("ice_crystal_chestplate", 0.05)
        ]
    ),
    "shadewalker": Monster(
        name="Shadewalker",
        level=84,
        hp=850,
        gold=90,
        exp=45,
        defense=15,
        resistance=50,
        gear_loot=[
            ("shadow_hunter_bow", 0.05),
            ("shadow_gloves", 0.05),
            ("shadow_hood", 0.05),
            ("shadow_pants", 0.05)
        ]
    )
}

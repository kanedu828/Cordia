from cordia.model.player_stats import PlayerStats


gear_set_data = {
    "ice_queen": {
        1: PlayerStats(),
        2: PlayerStats(intelligence=30, strength=30, efficiency=30),
        3: PlayerStats(spell_damage=30, crit_chance=10, spell_penetration=5),
    },
    "shadow_master": {
        1: PlayerStats(),
        2: PlayerStats(persistence=30, strength=30, luck=30),
        3: PlayerStats(damage=30, boss_damage=10, crit_chance=10),
    },
    "soul_stealer": {
        1: PlayerStats(),
        2: PlayerStats(damage=25, spell_damage=25),
        3: PlayerStats(damage=50, boss_damage=10, spell_damage=50),
    },
    "gamblers": {
        1: PlayerStats(),
        2: PlayerStats(luck=50),
        3: PlayerStats(damage=50, crit_chance=10),
        4: PlayerStats(luck=50),
        5: PlayerStats(damage=100, crit_chance=10, combo_chance=10),
    },
    "mystical_guardian": {
        1: PlayerStats(),
        2: PlayerStats(intelligence=50, persistence=50),
        3: PlayerStats(boss_damage=10, spell_damage=50),
        4: PlayerStats(intelligence=50, persistence=50),
        5: PlayerStats(boss_damage=100, spell_damage=100, spell_penetration=5),
    },
    "ancient_ocean_guardian": {
        1: PlayerStats(),
        2: PlayerStats(strength=50, efficiency=50),
        3: PlayerStats(damage=50, boss_damage=10),
        4: PlayerStats(strength=50, efficiency=50),
        5: PlayerStats(damage=100, boss_damage=20, penetration=5),
    },
    "void": {
        1: PlayerStats(),
        2: PlayerStats(damage=30, spell_damage=30),
        3: PlayerStats(boss_damage=25, penetration=5, spell_penetration=5),
        4: PlayerStats(
            damage=100,
            spell_damage=100,
            boss_damage=50,
            strike_radius=1,
            combo_chance=5,
        ),
    },
    "olympian": {
        1: PlayerStats(),
        2: PlayerStats(strength=75, efficiency=75, persistence=75, intelligence=75, luck=75),
        3: PlayerStats(damage=25),
        4: PlayerStats(boss_damage=40),
        5: PlayerStats(penetration=10, spell_penetration=10),
    },
    "olympian_god": {
        1: PlayerStats(damage=50),
        2: PlayerStats(penetration=10, spell_penetration=10),
        3: PlayerStats(boss_damage=40),
    },
}

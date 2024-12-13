from cordia.model.player_stats import PlayerStats


gear_set_data = {
    "ice_queen": {
        1: PlayerStats(),
        2: PlayerStats(intelligence=30, strength=30, efficiency=30),
        3: PlayerStats(spell_damage=30, crit_chance=10, penetration=10),
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
}

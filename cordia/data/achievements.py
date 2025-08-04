from cordia.model.achievement import Achievement
from cordia.model.player_stats import PlayerStats


achievement_data = {
    "goblin": Achievement(
        monster="Goblin",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(strength=2),
        stat_modifier="+",
    ),
    "goblin_king": Achievement(
        monster="Goblin King",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(strength=2),
        stat_modifier="%",
    ),
    "giant_spider": Achievement(
        monster="Giant Spider",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(intelligence=2),
        stat_modifier="+",
    ),
    "dryad": Achievement(
        monster="Dryad",
        monster_killed_increment=10,
        stat_bonus=PlayerStats(crit_chance=1),
        stat_modifier="+",
    ),
    "ancient_treant": Achievement(
        monster="Ancient Treant",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(intelligence=2),
        stat_modifier="%",
    ),
    "mountain_troll": Achievement(
        monster="Mountain Troll",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(damage=1),
        stat_modifier="+",
    ),
    "cave_wyrm": Achievement(
        monster="Cave Wyrm",
        monster_killed_increment=10,
        stat_bonus=PlayerStats(penetration=1),
        stat_modifier="+",
    ),
    "mountain_behemoth": Achievement(
        monster="Mountain Behemoth",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(damage=5),
        stat_modifier="+",
    ),
    "brussel_sprout": Achievement(
        monster="Brussel Sprout",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(spell_damage=1),
        stat_modifier="+",
    ),
    "philpot": Achievement(
        monster="Philpot",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(spell_damage=5),
        stat_modifier="+",
    ),
    "shadewalker": Achievement(
        monster="Shadewalker",
        monster_killed_increment=25,
        stat_bonus=PlayerStats(strength=1),
        stat_modifier="%",
    ),
    "shadow_master": Achievement(
        monster="Shadow Master",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(crit_chance=1),
        stat_modifier="+",
    ),
    "frost_elemental": Achievement(
        monster="Frost Elemental",
        monster_killed_increment=25,
        stat_bonus=PlayerStats(intelligence=1),
        stat_modifier="%",
    ),
    "ice_queen": Achievement(
        monster="Ice Queen",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(intelligence=5),
        stat_modifier="%",
    ),
    "crystal_warrior": Achievement(
        monster="Crystal Warrior",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(efficiency=1),
        stat_modifier="%",
    ),
    "royal_crystal_guard": Achievement(
        monster="Royal Crystal Guard",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(penetration=1),
        stat_modifier="+",
    ),
    "volcanic_salamander": Achievement(
        monster="Volcanic Salamander",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(persistence=1),
        stat_modifier="%",
    ),
    "souless_wanderer": Achievement(
        monster="Souless Wanderer",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(luck=1),
        stat_modifier="%",
    ),
    "soul_stealer": Achievement(
        monster="Soul Stealer",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(boss_damage=5),
        stat_modifier="+",
    ),
    "blossomthorn_fairy": Achievement(
        monster="Blossomthorn Fairy",
        monster_killed_increment=20,
        stat_bonus=PlayerStats(intelligence=3),
        stat_modifier="%",
    ),
    "mystical_guardian": Achievement(
        monster="Mystical Guardian",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(damage=10),
        stat_modifier="+",
    ),
    "ancient_giant_squid": Achievement(
        monster="Ancient Giant Squid",
        monster_killed_increment=20,
        stat_bonus=PlayerStats(strength=3),
        stat_modifier="%",
    ),
    "ancient_ocean_guardian": Achievement(
        monster="Ancient Ocean Guardian",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(boss_damage=3),
        stat_modifier="+",
    ),
    "void_entity": Achievement(
        monster="Void Entity",
        monster_killed_increment=200,
        stat_bonus=PlayerStats(boss_damage=3),
        stat_modifier="+",
    ),
    "olympian_general": Achievement(
        monster="Olympian General",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(damage=10),
        stat_modifier="+",
    ),
    "olympian_titan": Achievement(
        monster="Olympian Titan",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(damage=3),
        stat_modifier="%",
    ),
    "hermes": Achievement(
        monster="Hermes",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(efficiency=5),
        stat_modifier="%",
    ),
    "hercules": Achievement(
        monster="Hercules",
        monster_killed_increment=5,
        stat_bonus=PlayerStats(strength=5),
        stat_modifier="%",
    ),
}

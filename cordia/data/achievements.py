from cordia.model.achievement import Achievement
from cordia.model.player_stats import PlayerStats


achievement_data = {
    "goblin": Achievement(
        monster="Goblin",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(strength=2),
        stat_modifier="+",
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
    "brussel_sprout": Achievement(
        monster="Brussel Sprout",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(spell_damage=1),
        stat_modifier="+",
    ),
    "shadewalker": Achievement(
        monster="Shadewalker",
        monster_killed_increment=25,
        stat_bonus=PlayerStats(strength=1),
        stat_modifier="%",
    ),
    "frost_elemental": Achievement(
        monster="Frost Elemental",
        monster_killed_increment=25,
        stat_bonus=PlayerStats(intelligence=1),
        stat_modifier="%",
    ),
    "crystal_warrior": Achievement(
        monster="Crystal Warrior",
        monster_killed_increment=100,
        stat_bonus=PlayerStats(efficiency=1),
        stat_modifier="%",
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
}

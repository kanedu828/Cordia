from typing import List
from cordia.util.exp_util import exp_to_level, level_to_exp
from cordia.model.gear import Gear, PlayerGear
from cordia.model.player import Player
from cordia.data.gear import gear_data

def exp_bar(exp, bar_length=10, filled_char="🟩", empty_char="⬜"):
    """
    Generate an experience bar using emojis or characters.

    :param exp: Current experience points of the user.
    :param bar_length: The total length of the bar (in characters or emojis).
    :param filled_char: Character or emoji to represent filled portions.
    :param empty_char: Character or emoji to represent empty portions.
    :return: A string representing the experience bar.
    """
    # Calculate the current level
    current_level = exp_to_level(exp)
    
    # Get the total experience for the current and next levels
    current_level_exp = level_to_exp(current_level)
    next_level_exp = level_to_exp(current_level + 1)
    
    # Calculate progress towards the next level
    exp_in_current_level = exp - current_level_exp
    exp_needed_for_next_level = next_level_exp - current_level_exp
    
    # Calculate the number of filled segments in the bar
    filled_length = int((exp_in_current_level / exp_needed_for_next_level) * bar_length)
    
    # Create the bar string
    bar = filled_char * filled_length + empty_char * (bar_length - filled_length)
    
    return f"**lv. {current_level}** ({exp} exp)\n{bar}"

def get_stat_type_mapping():
    stat_type_mapping = {
        "boss_damage": "%",
        "crit_chance": "%",
        "penetration": "%",
        "combo_chance": "%",
        "strike_radius": "",
        "attack_cooldown": "s",
    }
    return stat_type_mapping

def get_player_stats_string(player: Player, player_gear: List[PlayerGear]) -> tuple:
    # Initialize the stats with base and gear_bonus for the first group of stats
    main_stats = {
        "strength": {"base": player.strength, "gear_bonus": 0},
        "persistence": {"base": player.persistence, "gear_bonus": 0},
        "intelligence": {"base": player.intelligence, "gear_bonus": 0},
        "efficiency": {"base": player.efficiency, "gear_bonus": 0},
        "luck": {"base": player.luck, "gear_bonus": 0},
    }

    # Initialize separate stats for the second group (boss_damage, crit_chance, penetration)
    extra_stats = {
        "boss_damage": 0,
        "crit_chance": 0,
        "penetration": 0,
        "combo_chance": 0,
        "strike_radius": 0,
        "attack_cooldown": 0,
    }

    # Loop through player gear to accumulate bonuses
    for pg in player_gear:
        gd: Gear = gear_data[pg.name]
        main_stats["strength"]["gear_bonus"] += gd.strength
        main_stats["persistence"]["gear_bonus"] += gd.persistence
        main_stats["intelligence"]["gear_bonus"] += gd.intelligence
        main_stats["efficiency"]["gear_bonus"] += gd.efficiency
        main_stats["luck"]["gear_bonus"] += gd.luck
        extra_stats["crit_chance"] += gd.crit_chance
        extra_stats["boss_damage"] += gd.boss_damage
        extra_stats["penetration"] += gd.penetration
        extra_stats["combo_chance"] += gd.combo_chance
        extra_stats["strike_radius"] += gd.strike_radius
        extra_stats["attack_cooldown"] += gd.attack_cooldown

    # Get the longest stat name for main stats to calculate uniform spacing
    max_stat_length_main = max(len(stat) for stat in main_stats)

    stat_emoji_mapping = get_stat_emoji_mapping()
    special_stat_emoji_mapping = get_special_stat_emoji_mapping()
    # Build the main stats string
    main_stats_string = "\n".join(
        f"{stat_emoji_mapping[stat]}{stat.capitalize().ljust(max_stat_length_main)} {values['base'] + values['gear_bonus']} ({values['base']} + {values['gear_bonus']})"
        for stat, values in main_stats.items()
    )

    # Get the longest stat name for extra stats
    max_stat_length_extra = max(len(stat) for stat in extra_stats)

    # Build the extra stats string
    extra_stats_string = "\n".join(
        f"{special_stat_emoji_mapping[stat]}{stat.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {value}{get_stat_type_mapping()[stat]}"
        for stat, value in extra_stats.items()
    )

    # Wrap both strings in code blocks for Discord and return as a tuple
    return f"```{main_stats_string}```", f"```{extra_stats_string}```"

def get_stat_emoji_mapping():
    emoji_mapping = {
        'strength': '💪',
        'persistence': '🔋',
        'intelligence': '🧠',
        'efficiency': '⚡️',
        'luck': '🍀',
    }
    return emoji_mapping

def get_special_stat_emoji_mapping():
    emoji_mapping = {
        'crit_chance': '🎯',
        'boss_damage': '💥',
        'penetration': '🗡️',
        'combo_chance': '🥊',
        'strike_radius': '🎆',
        'attack_cooldown': '🕒',
    }
    return emoji_mapping
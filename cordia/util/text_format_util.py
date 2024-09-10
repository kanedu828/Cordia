from typing import List
from cordia.model.gear_instance import GearInstance
from cordia.util.exp_util import exp_to_level, level_to_exp
from cordia.model.gear import Gear
from cordia.model.player import Player
from cordia.util.stat_mapping import get_stat_emoji, get_stat_modifier


def exp_bar(
    exp,
    bar_length=10,
    filled_char="<:cordia_exp_bar_filled:1282194013230727248>",
    empty_char="<:cordia_empty_bar:1282195811115208745>",
):
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


def hp_bar(current_health: int, max_health: int, bar_length=10):
    filled_emoji = "<:cordia_hp_bar_filled:1282187982127763606>"
    empty_emoji = "<:cordia_empty_bar:1282195811115208745>"

    # Calculate the number of filled segments
    filled_length = int(bar_length * current_health / max_health)
    empty_length = bar_length - filled_length

    # Create the health bar using the emojis
    bar = filled_emoji * filled_length + empty_emoji * empty_length

    # Return the health bar string
    return f"**Boss HP**: ({max(0, current_health)}/{max_health})\n{bar}\n"


def get_player_stats_string(player: Player, player_gear: List[GearInstance]) -> tuple:
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
        "damage": 0,
        "boss_damage": 0,
        "crit_chance": 0,
        "penetration": 0,
        "combo_chance": 0,
        "strike_radius": 0,
        "attack_cooldown": 0,
    }

    # Loop through player gear to accumulate bonuses
    for pg in player_gear:
        gd: Gear = pg.get_gear_data()
        bonus_stats = pg.get_bonus_stats()
        for s in bonus_stats["%"].keys():
            if s in main_stats:
                main_stats[s]["gear_bonus"] += int(
                    main_stats[s]["base"] * (bonus_stats["%"][s] / 100)
                )
            if s in extra_stats:
                extra_stats[s] += int(extra_stats[s] * (bonus_stats["%"][s] / 100))
        for s in bonus_stats["+"].keys():
            if s in main_stats:
                main_stats[s]["gear_bonus"] += bonus_stats["+"][s]
            if s in extra_stats:
                extra_stats[s] += bonus_stats["+"][s]
        upgrade_stats = pg.get_upgraded_stats()
        main_stats["strength"]["gear_bonus"] += upgrade_stats["strength"]
        main_stats["persistence"]["gear_bonus"] += upgrade_stats["persistence"]
        main_stats["intelligence"]["gear_bonus"] += upgrade_stats["intelligence"]
        main_stats["efficiency"]["gear_bonus"] += upgrade_stats["efficiency"]
        main_stats["luck"]["gear_bonus"] += upgrade_stats["luck"]
        extra_stats["damage"] += upgrade_stats["damage"]
        extra_stats["crit_chance"] += gd.crit_chance
        extra_stats["boss_damage"] += upgrade_stats["boss_damage"]
        extra_stats["penetration"] += gd.penetration
        extra_stats["combo_chance"] += gd.combo_chance
        extra_stats["strike_radius"] += gd.strike_radius
        extra_stats["attack_cooldown"] += gd.attack_cooldown

    # Get the longest stat name for main stats to calculate uniform spacing
    max_stat_length_main = max(len(stat) for stat in main_stats)

    # Build the main stats string
    main_stats_string = "\n".join(
        f"{get_stat_emoji(stat)}{stat.capitalize().ljust(max_stat_length_main)} {values['base'] + values['gear_bonus']} ({values['base']} + {values['gear_bonus']})"
        for stat, values in main_stats.items()
    )

    # Get the longest stat name for extra stats
    max_stat_length_extra = max(len(stat) for stat in extra_stats)

    # Build the extra stats string
    extra_stats_string = "\n".join(
        f"{get_stat_emoji(stat)}{stat.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {value}{get_stat_modifier(stat)}"
        for stat, value in extra_stats.items()
    )

    # Wrap both strings in code blocks for Discord and return as a tuple
    return f"```{main_stats_string}```", f"```{extra_stats_string}```"


# snake_case -> Snake Case
def snake_case_to_capital(snake_str):
    # Split by underscore and capitalize each word
    words = snake_str.split("_")
    return " ".join([word.capitalize() for word in words])


def get_stars_string(stars, max_stars):
    # Create the filled stars
    filled_stars = ["<:cordia_star:1281789019826557029>" for _ in range(stars)]
    # Create the empty stars
    empty_stars = [
        "<:cordia_empty_star:1281789033386741824>" for _ in range(max_stars - stars)
    ]

    # Combine both parts
    star_output = filled_stars + empty_stars

    # Split into chunks of 5 emojis for readability
    star_chunks = [
        "".join(star_output[i : i + 5]) for i in range(0, len(star_output), 5)
    ]

    # Join the chunks with a space
    return " ".join(star_chunks)

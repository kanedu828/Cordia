from typing import Counter, List
from cordia.model.gear_instance import GearInstance
from cordia.model.player_stats import PlayerStats
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

    return f"**lv. {current_level}** ({display_exp(exp)})\n{bar}\n"


def hp_bar(current_health: int, max_health: int, bar_length=10):
    filled_emoji = "<:cordia_hp_bar_filled:1282187982127763606>"
    empty_emoji = "<:cordia_empty_bar:1282195811115208745>"

    # Calculate the number of filled segments
    filled_length = int(bar_length * current_health / max_health)
    empty_length = bar_length - filled_length

    # Create the health bar using the emojis
    bar = filled_emoji * filled_length + empty_emoji * empty_length

    # Return the health bar string
    return f"**Boss HP**: ({max(0, current_health):,}/{max_health:,})\n{bar}\n"


def get_player_stats_string(player: Player, player_stats: PlayerStats) -> tuple:
    # Initialize the stats with base and gear_bonus for the first group of stats
    main_stats = {
        "strength": {
            "base": player.strength,
            "gear_bonus": player_stats.strength - player.strength,
        },
        "persistence": {
            "base": player.persistence,
            "gear_bonus": player_stats.persistence - player.persistence,
        },
        "intelligence": {
            "base": player.intelligence,
            "gear_bonus": player_stats.intelligence - player.intelligence,
        },
        "efficiency": {
            "base": player.efficiency,
            "gear_bonus": player_stats.efficiency - player.efficiency,
        },
        "luck": {"base": player.luck, "gear_bonus": player_stats.luck - player.luck},
    }

    # Initialize separate stats for the second group (boss_damage, crit_chance, penetration)
    extra_stats = {
        "damage": player_stats.damage,
        "spell_damage": player_stats.spell_damage,
        "boss_damage": player_stats.boss_damage,
        "crit_chance": player_stats.crit_chance,
        "penetration": player_stats.penetration,
        "combo_chance": player_stats.combo_chance,
        "strike_radius": player_stats.strike_radius,
        "attack_cooldown": player_stats.attack_cooldown,
    }

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
    filled_stars = ["<:cs:1281789019826557029>" for _ in range(min(stars, max_stars))]
    # Create the empty stars
    empty_stars = [
        "<:ces:1281789033386741824>" for _ in range(max_stars - len(filled_stars))
    ]
    # Create the chaos stars for stars beyond max_stars
    chaos_stars = [
        "<:ccs:1316684323856060476>" for _ in range(max(0, stars - max_stars))
    ]

    # Combine all parts
    star_output = filled_stars + empty_stars + chaos_stars

    # Split into chunks of 5 emojis for readability
    star_chunks = [
        "".join(star_output[i : i + 5]) for i in range(0, len(star_output), 5)
    ]

    # Join the chunks with a space
    return " ".join(star_chunks)


def display_gold(amount: int):
    gold_emoji = "<:cordia_gold:1284046011496529975>"
    return f"**{amount:,}** {gold_emoji} **Gold**"


def display_exp(amount: int):
    exp_emoji = "<:cordia_exp:1284045273793826877>"
    return f"**{amount:,}** {exp_emoji} **Exp**"

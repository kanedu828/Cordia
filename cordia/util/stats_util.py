import random
from typing import List

from cordia.model.gear_instance import GearInstance
from cordia.util.gear_util import get_weapon_from_player_gear
import discord
from cordia.model.gear import Gear
from cordia.model.player import Player
from cordia.util.exp_util import exp_to_level
from cordia.util.text_format_util import (
    exp_bar,
    get_player_stats_string,
)


def get_player_stats(player: Player, player_gear: List[GearInstance]):
    base_stats = {
        "strength": player.strength,
        "persistence": player.persistence,
        "intelligence": player.intelligence,
        "efficiency": player.efficiency,
        "luck": player.luck,
        "damage": 0,
        "boss_damage": 0,
        "crit_chance": 0,
        "penetration": 0,
        "combo_chance": 0,
        "strike_radius": 0,
        "attack_cooldown": 0,
        "spell_damage": 0,
    }

    stats = base_stats.copy()

    for pg in player_gear:
        gd: Gear = pg.get_gear_data()
        bonus_stats = pg.get_bonus_stats()
        for s in bonus_stats["%"].keys():
            stats[s] += int(base_stats[s] * (bonus_stats["%"][s] / 100))
        for s in bonus_stats["+"].keys():
            stats[s] += bonus_stats["+"][s]
        upgrade_stats = pg.get_upgraded_stats()
        # ADD UPGRADE STATS HERE
        stats["strength"] += upgrade_stats["strength"]
        stats["persistence"] += upgrade_stats["persistence"]
        stats["intelligence"] += upgrade_stats["intelligence"]
        stats["efficiency"] += upgrade_stats["efficiency"]
        stats["luck"] += upgrade_stats["luck"]
        stats["damage"] += upgrade_stats["damage"]
        stats["crit_chance"] += gd.crit_chance
        stats["boss_damage"] += upgrade_stats["boss_damage"]
        stats["penetration"] += gd.penetration
        stats["combo_chance"] += gd.combo_chance
        stats["strike_radius"] += gd.strike_radius
        stats["attack_cooldown"] += gd.attack_cooldown
        stats["spell_damage"] += upgrade_stats["spell_damage"]

    return stats


def get_stats_embed(player: Player, player_gear: List[GearInstance]):
    embed = discord.Embed(title=f"Your Stats")
    stats_text, special_stats_text = get_player_stats_string(player, player_gear)
    upgrade_points = get_upgrade_points(player)

    exp_bar_text = f"{exp_bar(player.exp)}\n\n"
    embed.add_field(name="", value=exp_bar_text, inline=False)
    if upgrade_points > 0:
        embed.add_field(
            name="",
            value=f"✨You have {upgrade_points} upgrade points!✨",
            inline=False,
        )
    else:
        embed.add_field(
            name="", value=f"You have {upgrade_points} upgrade points.", inline=False
        )
    embed.add_field(name="", value=stats_text)
    embed.add_field(name="", value=special_stats_text)
    weapon = get_weapon_from_player_gear(player_gear)
    spell = weapon.get_gear_data().spell
    if spell:
        embed.add_field(
            name="", value=weapon.get_spell_stats_string(False), inline=False
        )

    embed.add_field(name="Gold", value=f"🪙**{player.gold}**", inline=False)
    return embed


def get_upgrade_points(player: Player) -> int:
    points_per_level = 3
    init_base_stat_sum = 5
    base_stat_sum = (
        player.intelligence
        + player.strength
        + player.efficiency
        + player.persistence
        + player.luck
    )
    level = exp_to_level(player.exp)
    return max(level * points_per_level - base_stat_sum + init_base_stat_sum, 0)


def random_within_range(base_value) -> int:
    # Calculate the 25% range
    range_value = base_value * 0.25

    # Determine the minimum and maximum values within 25% of the base value
    min_value = int(base_value - range_value)
    max_value = int(base_value + range_value)

    # Return a random integer within the range
    return random.randint(min_value, max_value)


def level_difference_multiplier(player_level: int, monster_level: int) -> float:
    # Calculate the difference between player and monster levels
    level_difference = player_level - monster_level

    # Cap the level difference to a maximum of 5
    capped_difference = max(min(level_difference, 5), -5)

    # Calculate the multiplier
    multiplier = 1 + (capped_difference * 0.05)

    return round(multiplier, 2)


def calculate_weighted_monster_mean(monster_tuples):
    total_weight = 0
    weighted_level_sum = 0
    weighted_hp_sum = 0
    weighted_gold_sum = 0
    weighted_exp_sum = 0
    weighted_defense_sum = 0  # Add penetration calculation

    for monster, weight in monster_tuples:
        weighted_level_sum += monster.level * weight
        weighted_hp_sum += monster.hp * weight
        weighted_gold_sum += monster.gold * weight
        weighted_exp_sum += monster.exp * weight
        weighted_defense_sum += monster.defense * weight  # Apply weight to penetration
        total_weight += weight

    # Calculate the weighted means
    if total_weight:
        weighted_means = {
            "level": weighted_level_sum / total_weight,
            "hp": weighted_hp_sum / total_weight,
            "gold": weighted_gold_sum / total_weight,
            "exp": weighted_exp_sum / total_weight,
            "defense": weighted_defense_sum
            / total_weight,  # Add penetration to the result
        }
    else:
        weighted_means = {
            "level": 0,
            "hp": 0,
            "gold": 0,
            "exp": 0,
            "defense": 0,  # Set default penetration to 0
        }

    return weighted_means


def simulate_idle_damage(
    stat_value: float, monster_mean, player_stats, player_level
) -> float:
    stat_value = random_within_range(stat_value)
    stat_value *= level_difference_multiplier(player_level, monster_mean["level"])

    # Calculate crit
    stat_value += (stat_value * 1.5 - stat_value) * (player_stats["crit_chance"] / 100)

    # Penetration
    monster_defense_percentage = monster_mean["defense"] / 100
    monster_defense_percentage -= monster_defense_percentage * (
        min(player_stats["penetration"], 100) / 100
    )
    stat_value -= stat_value * monster_defense_percentage

    return stat_value

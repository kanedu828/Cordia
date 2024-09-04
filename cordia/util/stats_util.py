import random
from typing import List

import discord
from cordia.model.gear import Gear, PlayerGear
from cordia.model.player import Player
from cordia.data.gear import gear_data
from cordia.util.exp_util import exp_to_level
from cordia.util.text_format_util import exp_bar, get_player_stats_string


def get_player_stats(player: Player, player_gear: List[PlayerGear]):
    stats = {
        "strength": player.strength,
        "persistence": player.persistence,
        "intelligence": player.intelligence,
        "efficiency": player.efficiency,
        "luck": player.luck,
        "boss_damage": 0,
        "crit_chance": 0,
        "penetration": 0,
        "combo_chance": 0,
        "strike_radius": 0,
        "attack_cooldown": 0
    }
    for pg in player_gear:
        gd: Gear = gear_data[pg.name]
        stats["strength"] += gd.strength
        stats["persistence"] += gd.persistence
        stats["intelligence"] += gd.intelligence
        stats["efficiency"] += gd.efficiency
        stats["luck"] += gd.luck
        stats["crit_chance"] += gd.crit_chance
        stats["boss_damage"] += gd.boss_damage
        stats["penetration"] += gd.penetration
        stats["combo_chance"] += gd.combo_chance
        stats["strike_radius"] += gd.strike_radius
        stats["attack_cooldown"] += gd.attack_cooldown

    return stats

def get_stats_embed(player, player_gear):
    embed = discord.Embed(
        title=f"Your Stats"
    )
    stats_text, special_stats_text = get_player_stats_string(player, player_gear)
    upgrade_points = get_upgrade_points(player)

    exp_bar_text = f"{exp_bar(player.exp)}\n\n"
    embed.add_field(name="", value=exp_bar_text, inline=False)
    if upgrade_points > 0:
        embed.add_field(name="", value=f"✨You have {upgrade_points} upgrade points!✨", inline=False)
    else:
        embed.add_field(name="", value=f"You have {upgrade_points} upgrade points.", inline=False)
    embed.add_field(name="", value=stats_text)
    embed.add_field(name="", value=special_stats_text)
    return embed

def get_upgrade_points(player: Player) -> int:
    init_base_stat_sum = 5
    base_stat_sum = player.intelligence + player.strength + player.efficiency + player.persistence + player.luck
    level = exp_to_level(player.exp)
    return max(level - base_stat_sum + init_base_stat_sum, 0)
    
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
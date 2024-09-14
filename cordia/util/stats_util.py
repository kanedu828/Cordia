import random
from typing import Counter, List

from cordia.model.gear_instance import GearInstance
from cordia.model.gear import Gear
from cordia.model.player import Player
from cordia.model.player_gear import PlayerGear
from cordia.util.exp_util import exp_to_level
from cordia.data.gear_sets import gear_set_data


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
        stats["boss_damage"] += gd.boss_damage
        stats["penetration"] += gd.penetration
        stats["combo_chance"] += gd.combo_chance
        stats["strike_radius"] += gd.strike_radius
        stats["attack_cooldown"] += gd.attack_cooldown
        stats["spell_damage"] += upgrade_stats["spell_damage"]

    return stats


def get_total_gear_set_stats(player_gear: list[PlayerGear]):
    gear_sets = Counter()
    total_stats = {}
    for pg in player_gear:
        gd = pg.get_gear_data()
        if gd.gear_set:
            gear_sets[gd.gear_set] += 1
            set_stats = gear_set_data[gd.gear_set].get(gear_sets[gd.gear_set], {})
            total_stats = dict(Counter(total_stats) + Counter(set_stats))
    return total_stats


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
    return max(
        level * points_per_level
        + player.rebirth_points
        - base_stat_sum
        + init_base_stat_sum,
        0,
    )


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


def get_rebirth_points(level: int):
    return int(max(((level - 50) / 2) + 10, 0))

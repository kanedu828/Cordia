import random
from typing import List, Literal, Tuple
from cordia.model.gear_instance import GearInstance
from cordia.model.monster import Monster, MonsterType
from cordia.model.player import Player
from cordia.model.player_stats import PlayerStats
from cordia.util.exp_util import exp_to_level
from cordia.util.gear_util import get_weapon_from_player_gear
from cordia.util.stats_util import (
    level_difference_multiplier,
    random_within_range,
)


def get_random_battle_text(kills: int, monster: str) -> str:
    no_kill_text = [
        f"Despite your best efforts, you could not defeat a **{monster}**. Try again!",
        f"You were quickly overwhelmed by a **{monster}**. Try again!",
        f"Your strikes were not enough to defeat a **{monster}**. Try again!",
        f"You were no match for a **{monster}**. Try again!",
    ]

    single_kill_text = [
        f"Using all your might, you defeat a **{monster}**",
        f"After an epic battle, you defeat a **{monster}**",
        f"After a hard fought battle, you defeat a **{monster}**",
        f"After an intense clash, you emerge victorious against a **{monster}**!",
        f"With a final blow, a **{monster}** falls to your might!",
    ]

    multi_kill_text = [
        f"With your might, you overpower and kill **{kills}** **{monster}s**",
        f"In a show of grandeur, you defeat **{kills}** **{monster}s**",
        f"With your overwhelming strength, you defeat **{kills}** **{monster}s**",
    ]

    if kills == 0:
        return random.choice(no_kill_text)

    if kills == 1:
        return random.choice(single_kill_text)

    return random.choice(multi_kill_text)


def get_diminished_stat(base: int, stat: int, diminishing_scale_factor=0.8):
    # Any stat above base damage gives diminishing returns
    scaled_stat = stat
    if stat > base:
        scaled_stat = base + (scaled_stat - base) ** diminishing_scale_factor
    return scaled_stat


def calculate_attack_damage(
    monster: Monster,
    player_stats: PlayerStats,
    player: Player,
    player_gear: List[GearInstance],
    action: Literal["attack", "cast_spell"] = "attack",
) -> Tuple[int, bool]:
    # Multiplier depending on player's level compared to monster's
    level_damage_multiplier = level_difference_multiplier(
        exp_to_level(player.exp), monster.level
    )
    weapon = get_weapon_from_player_gear(player_gear)
    spell = weapon.get_gear_data().spell

    if action == "cast_spell" and spell:
        spell_daamge = player_stats.spell_damage + spell.damage
        scaled_stat = get_diminished_stat(
            spell_daamge, player_stats.__dict__[spell.scaling_stat]
        )
        damage = spell_daamge + (scaled_stat * spell.scaling_multiplier)
    else:
        scaled_strength = get_diminished_stat(
            player_stats.damage, player_stats.strength
        )
        damage = player_stats.damage + scaled_strength

    damage = random_within_range(damage)
    damage *= level_damage_multiplier

    # Calculate crit
    CRIT_MULTIPLIER = 1.5
    is_crit = random.random() < player_stats.crit_chance / 100
    if is_crit:
        damage *= CRIT_MULTIPLIER

    # Boss damage multiplier
    if monster.type == MonsterType.BOSS:
        damage += damage * (player_stats.boss_damage / 100)

    if action == "cast_spell" and spell and spell.scaling_stat == "intelligence":
        monster_resistance_percentage = monster.resistance / 100
        monster_resistance_percentage -= monster_resistance_percentage * (
            min(player_stats.spell_penetration, 100) / 100
        )
        damage -= damage * monster_resistance_percentage
    else:
        # Penetration multiplier. Cant be over 100%
        monster_defense_percentage = monster.defense / 100
        monster_defense_percentage -= monster_defense_percentage * (
            min(player_stats.penetration, 100) / 100
        )
        damage -= damage * monster_defense_percentage

    return int(damage), is_crit


def simulate_idle_damage(
    stat_value: float, monster_mean, player_stats: PlayerStats, player_level
) -> float:
    stat_value = random_within_range(stat_value)
    stat_value *= level_difference_multiplier(player_level, monster_mean["level"])

    # Calculate crit
    stat_value += (stat_value * 1.5 - stat_value) * (player_stats.crit_chance / 100)

    # Penetration
    monster_defense_percentage = monster_mean["defense"] / 100
    monster_defense_percentage -= monster_defense_percentage * (
        min(player_stats.penetration, 100) / 100
    )
    stat_value -= stat_value * monster_defense_percentage

    return stat_value

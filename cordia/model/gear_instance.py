from dataclasses import dataclass
from math import ceil
import math
from cordia.data.gear import gear_data
from cordia.model.gear import Gear
from cordia.model.player_stats import PlayerStats
from cordia.model.spells import SpellType
from cordia.util.stat_mapping import get_stat_emoji, get_stat_modifier


@dataclass(frozen=True)
class GearInstance:
    id: int
    discord_id: int
    name: str
    stars: int
    bonus: str
    slot: str = ""

    def get_gear_data(self) -> Gear:
        return gear_data[self.name]

    def get_upgrade_cost(self) -> int:
        gd = self.get_gear_data()
        base_cost = gd.level * 100
        gold_cost = int(base_cost + (self.stars * base_cost / 4))

        upgrade_item_cost = 0
        if self.stars >= 10:
            if gd.upgrade_item == "shard":
                upgrade_item_cost = max(math.floor((self.stars - 10) / 5), -1) + (
                    1 * ceil(gd.level / 25)
                )
            else:
                upgrade_item_cost = max(math.floor((self.stars - 10) / 5), -1) + 1

        cost = {"gold": gold_cost, "item": (gd.upgrade_item, upgrade_item_cost)}

        return cost

    def get_bonus_stats(self):
        bonus_stats = {
            "%": {
                "strength": 0,
                "persistence": 0,
                "intelligence": 0,
                "efficiency": 0,
                "luck": 0,
                "damage": 0,
                "boss_damage": 0,
                "spell_damage": 0,
            },
            "+": {
                "strength": 0,
                "persistence": 0,
                "intelligence": 0,
                "efficiency": 0,
                "luck": 0,
                "damage": 0,
                "boss_damage": 0,
                "spell_damage": 0,
            },
        }
        if self.bonus:
            split_bonus = self.bonus.split(";")
            for sb in split_bonus:
                sb_split = sb.split(":")
                stat, value, modifier = sb_split
                bonus_stats[modifier][stat] += int(value)
        return bonus_stats

    def get_upgraded_stats(self):
        gd = self.get_gear_data()

        # Base stats from the gear data
        base_stats = {
            "damage": gd.stats.damage,
            "strength": gd.stats.strength,
            "persistence": gd.stats.persistence,
            "intelligence": gd.stats.intelligence,
            "efficiency": gd.stats.efficiency,
            "luck": gd.stats.luck,
            "spell_damage": gd.stats.spell_damage,
        }

        if gd.spell:
            base_stats["spell_damage"] += gd.spell.damage

        upgraded_stats = base_stats.copy()

        # Calculate percentage increase per star
        stars_remaining = self.stars
        star_threshold = 5  # Each threshold is 5 stars
        percentage_increase = 10  # Starts at 10%

        while stars_remaining > 0:
            stars_to_process = min(stars_remaining, star_threshold)

            # Apply the increase for the current star threshold
            for stat, value in base_stats.items():
                increment = ceil((value * percentage_increase / 100)) * stars_to_process
                upgraded_stats[stat] += increment

            # Move to the next range
            stars_remaining -= stars_to_process
            percentage_increase += 10  # Increase percentage for the next set of stars

        return upgraded_stats

    def get_bonus_stats_string(self):
        bonus_str = ""
        if self.bonus:
            split_bonus = self.bonus.split(";")
            for sb in split_bonus:
                sb_split = sb.split(":")
                stat, value, modifier = sb_split
                if modifier == "%":
                    bonus_str += f"\n{value}{modifier} {get_stat_emoji(stat)}{stat}"
                elif modifier == "+":
                    bonus_str += f"\n{modifier}{value} {get_stat_emoji(stat)}{stat}"
        return f"```{bonus_str.replace('_', ' ').title()}```" if bonus_str else ""

    def get_main_stats_string(self) -> str:
        gd = self.get_gear_data()
        upgraded_stats = self.get_upgraded_stats()
        main_stats = [
            "damage",
            "spell_damage",
            "strength",
            "persistence",
            "intelligence",
            "efficiency",
            "luck",
        ]
        max_stat_length_extra = max(len(stat) for stat in main_stats)
        main_stats_string = ""

        # Get spell damage attributed to the weapon
        damage_from_spell = gd.spell.damage if gd.spell else 0

        # Calculate the spell damage ratio, handling potential division errors gracefully
        spell_damage_ratio = (
            gd.stats.spell_damage / (gd.stats.spell_damage + damage_from_spell)
            if (gd.stats.spell_damage + damage_from_spell) > 0
            else 1
        )

        upgraded_stats["spell_damage"] = int(
            upgraded_stats["spell_damage"] * spell_damage_ratio
        )

        for s in main_stats:
            base_value = gd.stats.__dict__[s]
            if base_value:
                upgrade_value = upgraded_stats[s] - base_value
                main_stats_string += (
                    f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} "
                    f"{upgraded_stats[s]} ({base_value} + {upgrade_value}){get_stat_modifier(s)}"
                )

        return f"```{main_stats_string}```"

    def get_secondary_stats_string(self) -> str:
        gd = self.get_gear_data()
        secondary_stats = [
            "boss_damage",
            "attack_cooldown",
            "crit_chance",
            "penetration",
            "spell_penetration",
            "combo_chance",
            "strike_radius",
        ]
        max_stat_length_extra = max(len(stat) for stat in secondary_stats)
        secondary_stats_string = ""
        for s in secondary_stats:
            if gd.stats.__dict__[s]:
                secondary_stats_string += f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {gd.stats.__dict__[s]}{get_stat_modifier(s)}"

        return f"```{secondary_stats_string}```" if secondary_stats_string else ""

    def get_spell_stats_string(self, split_spell_damage=False):
        wd = self.get_gear_data()
        if wd.spell.spell_type == SpellType.BUFF and wd.spell.buff:
            return wd.spell.get_spell_stats_string()
        bonus_stats = self.get_bonus_stats()

        # Get spell damage attributed to the spell
        spell_damage_ratio = wd.spell.damage / (wd.stats.spell_damage + wd.spell.damage)
        total_stats = int(
            self.get_upgraded_stats()["spell_damage"] * spell_damage_ratio
        )

        if not split_spell_damage:
            total_stats += bonus_stats["+"]["spell_damage"]
        # Bonus stats is excludeed from split text because split text is shown in gear menu, and bonus stats isnt
        # included in in split text there. (Since bonus text shown sep)
        split_text = f" ({wd.spell.damage} + {total_stats - wd.spell.damage})"
        spell_stats = {
            "spell_damage": f"{total_stats}",
            "spell_strike_radius": wd.spell.strike_radius,
            "spell_cooldown": wd.spell.cooldown,
            "scaling_multiplier": wd.spell.scaling_multiplier,
            "scaling_stat": wd.spell.scaling_stat.title(),
        }

        if split_spell_damage:
            spell_stats["spell_damage"] += split_text
        max_stat_length_extra = max(len(stat) for stat in spell_stats)

        spell_stats_string = "\n".join(
            f"{get_stat_emoji(stat)}{stat.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {value}{get_stat_modifier(stat)}"
            for stat, value in spell_stats.items()
        )
        spell_stats_string = (
            f"🔍{'Type'.ljust(max_stat_length_extra)} {wd.spell.spell_type.value.title()}\n"
            + spell_stats_string
        )
        return f"```{spell_stats_string}```"

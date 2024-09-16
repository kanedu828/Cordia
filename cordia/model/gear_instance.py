from dataclasses import dataclass
from math import ceil
import math
from cordia.data.gear import gear_data
from cordia.data.items import item_data
from cordia.model.gear import Gear
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
                bonus_stats[modifier][stat] = int(value)
        return bonus_stats

    def get_upgraded_stats(self):
        gd = self.get_gear_data()

        # Base stats from the gear data
        base_stats = {
            "damage": gd.damage,
            "strength": gd.strength,
            "persistence": gd.persistence,
            "intelligence": gd.intelligence,
            "efficiency": gd.efficiency,
            "luck": gd.luck,
            "spell_damage": 0,
        }

        if gd.spell:
            base_stats["spell_damage"] = gd.spell.damage

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
            "strength",
            "persistence",
            "intelligence",
            "efficiency",
            "luck",
        ]
        max_stat_length_extra = max(len(stat) for stat in main_stats)
        main_stats_string = ""

        for s in main_stats:
            base_value = gd.__dict__[s]
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
            "combo_chance",
            "strike_radius",
        ]
        max_stat_length_extra = max(len(stat) for stat in secondary_stats)
        secondary_stats_string = ""
        for s in secondary_stats:
            if gd.__dict__[s]:
                secondary_stats_string += f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {gd.__dict__[s]}{get_stat_modifier(s)}"

        return f"```{secondary_stats_string}```" if secondary_stats_string else ""

    def get_spell_stats_string(self, split_spell_damage=False):
        wd = self.get_gear_data()
        if wd.spell.spell_type == SpellType.BUFF and wd.spell.buff:
            return wd.spell.get_spell_stats_string()
        split_text = f" ({wd.spell.damage} + {self.get_upgraded_stats()['spell_damage'] - wd.spell.damage})"
        spell_stats = {
            "spell_damage": f"{self.get_upgraded_stats()['spell_damage']}",
            "magic_penetration": wd.spell.magic_penetration,
            "spell_strike_radius": wd.spell.strike_radius,
            "spell_cooldown": wd.spell.spell_cooldown,
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
        spell_stats_string = f"🔍{'Type'.ljust(max_stat_length_extra)} {wd.spell.spell_type.value.title()}\n" + spell_stats_string
        return f"```{spell_stats_string}```"

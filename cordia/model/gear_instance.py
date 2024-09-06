from dataclasses import dataclass
from cordia.data.gear import gear_data
from cordia.model.gear import Gear
from cordia.util.stat_mapping import get_stat_emoji, get_stat_modifier


@dataclass(frozen=True)
class GearInstance:
    id: int
    discord_id: int
    name: str
    stars: int
    bonus: str
    created_at: str
    updated_at: str

    def get_gear_data(self) -> Gear:
        return gear_data[self.name]
    
    def get_main_stats_string(self) -> str:
        gd = self.get_gear_data()
        main_stats = ["damage", "boss_damage", "strength", "persistence", "intelligence", "efficiency", "luck"]
        max_stat_length_extra = max(len(stat) for stat in main_stats)
        main_stats_string = ""
        for s in main_stats:
            if gd.__dict__[s]:
                main_stats_string += f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {gd.__dict__[s]}{get_stat_modifier(s)}"

        return f"```{main_stats_string}```"
    
    def get_secondary_stats_string(self) -> str:
        gd = self.get_gear_data()
        secondary_stats = ["attack_cooldown", "crit_chance", "penetration", "combo_chance", "strike_radius"]
        max_stat_length_extra = max(len(stat) for stat in secondary_stats)
        secondary_stats_string = ""
        for s in secondary_stats:
            if gd.__dict__[s]:
                secondary_stats_string += f"\n{get_stat_emoji(s)}{s.replace('_', ' ').capitalize().ljust(max_stat_length_extra)} {gd.__dict__[s]}{get_stat_modifier(s)}"

        return f"```{secondary_stats_string}```"
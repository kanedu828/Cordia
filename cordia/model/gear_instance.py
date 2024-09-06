from dataclasses import dataclass
from math import ceil
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
            "boss_damage": gd.boss_damage
        }
        
        upgraded_stats = base_stats.copy()
        
        # Calculate percentage increase per star
        stars_remaining = self.stars
        star_threshold = 5  # Each threshold is 5 stars
        percentage_increase = 10  # Starts at 10%

        while stars_remaining > 0:
            stars_to_process = min(stars_remaining, star_threshold)
            
            # Apply the increase for the current star threshold
            for stat, value in base_stats.items():
                increment = ceil((value * percentage_increase / 100) * stars_to_process)
                upgraded_stats[stat] += increment
            
            # Move to the next range
            stars_remaining -= stars_to_process
            percentage_increase += 10  # Increase percentage for the next set of stars
        
        return upgraded_stats
        
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
    

import math
import datetime
from typing import List
from cordia.dao.player_dao import PlayerDao
from cordia.data.locations import location_data
from cordia.dao.player_gear_dao import PlayerGearDao
from cordia.dao.gear_dao import GearDao
from cordia.data.gear import gear_data
import random

from cordia.data.monsters import monster_data
from cordia.model.player import Player
from cordia.model.gear import Gear, GearType, PlayerGear
from cordia.model.monster import Monster, MonsterType

class CordiaService:
    def __init__(self, player_dao: PlayerDao, gear_dao: GearDao, player_gear_dao: PlayerGearDao):
        self.player_dao = player_dao
        self.gear_dao = gear_dao
        self.player_gear_dao = player_gear_dao

        self.player_cooldowns = {}

    # Player
    async def get_player_by_discord_id(self, discord_id: int) -> Player:
        return await self.player_dao.get_by_discord_id(discord_id)
    
    async def insert_player(self, discord_id: int) -> Player:
        return await self.player_dao.insert_player(discord_id)

    async def get_or_insert_player(self, discord_id: int) -> Player:
        player = await self.get_player_by_discord_id(discord_id)
        if player:
            return player
        else:
            player = await self.insert_player(discord_id)
            gear_instance = await self.insert_gear(discord_id, "basic_sword")
            await self.equip_gear(discord_id, gear_instance["id"], GearType.WEAPON.value)
            return player

    async def increment_stat(self, discord_id: int, stat_name: str, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_stat_value = player.__dict__[stat_name] + increment_by
        await self.player_dao.update_stat(discord_id, stat_name, new_stat_value)

    async def increment_exp(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_exp = player.exp + increment_by
        await self.player_dao.update_exp(discord_id, new_exp)

    async def increment_gold(self, discord_id: int, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        new_gold = max(player.gold + increment_by, 0)  # Ensure gold doesn't go below 0
        await self.player_dao.update_gold(discord_id, new_gold)
    
    async def update_location(self, discord_id: int, location: str):
        if not location in location_data:
            raise ValueError(f'{location} is not a valid locatin')
        await self.player_dao.update_location(discord_id, location)

    # Gear
    async def insert_gear(self, discord_id, name):
        return await self.gear_dao.insert_gear(discord_id, name)

    # Player Gear
    async def get_player_gear(self, discord_id: int):
        return await self.player_gear_dao.get_player_gear(discord_id)

    async def equip_gear(self, discord_id: int, gear_id: int, slot: str):
        return await self.player_gear_dao.equip_gear(discord_id, gear_id, slot)

    async def remove_gear(self, discord_id: int, slot: str):
        await self.player_gear_dao.remove_gear(discord_id, slot)

    async def get_weapon(self, player_gear: List[PlayerGear]):
        return next((x for x in player_gear if x.slot == GearType.WEAPON.value), None)

    # Util
    def exp_to_level(self, exp):
        """Convert experience points to level."""
        base_exp = 5  # Base experience required for level 1
        level = math.floor(math.sqrt((exp + base_exp) / 5))
        return max(1, level)  # Ensure that the minimum level is 1

    def level_to_exp(self, level):
        """Convert level to the total experience required to reach that level."""
        base_exp = 5  # Base experience for level 1
        exp = 5 * (level ** 2) - base_exp
        return exp
    
    async def get_player_stats(self, player: Player, player_gear: List[PlayerGear]):
        stats = {
            "strength": player.strength,
            "persistence": player.persistence,
            "intelligence": player.intelligence,
            "efficiency": player.efficiency,
            "luck": player.luck,
            "boss_damage": 0,
            "crit_chance": 0,
            "penetration": 0,
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

        return stats

    def percent_to_next_level(self, exp):
        """Calculate the percentage of experience left to the next level."""
        current_level = self.exp_to_level(exp)
        current_level_exp = self.level_to_exp(current_level)
        next_level_exp = self.level_to_exp(current_level + 1)
        
        exp_in_current_level = exp - current_level_exp
        exp_needed_for_next_level = next_level_exp - current_level_exp
        
        percent_complete = (exp_in_current_level / exp_needed_for_next_level) * 100
        
        return percent_complete
    
    def random_within_range(self, base_value):
        # Calculate the 25% range
        range_value = base_value * 0.25
        
        # Determine the minimum and maximum values within 25% of the base value
        min_value = int(base_value - range_value)
        max_value = int(base_value + range_value)
        
        # Return a random integer within the range
        return random.randint(min_value, max_value)
    
    def level_difference_multiplier(self, player_level: int, monster_level: int) -> float:
        # Calculate the difference between player and monster levels
        level_difference = player_level - monster_level
        
        # Cap the level difference to a maximum of 5
        capped_difference = max(min(level_difference, 5), -5)
        
        # Calculate the multiplier
        multiplier = 1 + (capped_difference * 0.05)
        
        return round(multiplier, 2)


    # Battle
    async def calculate_attack_damage(self, monster: Monster, player: Player, player_gear: List[PlayerGear]) -> int:
        player_stats = await self.get_player_stats(player, player_gear)

        # Multiplier depending on player's level compared to monster's
        level_damage_multiplier = self.level_difference_multiplier(self.exp_to_level(player.exp), monster.level)
        damage = self.random_within_range(player_stats["strength"]) * level_damage_multiplier

        # Calculate crit
        crit_multiplier = 1.5
        if random.random() < player_stats["crit_chance"] / 100:
            damage *= crit_multiplier

        # Boss damage multiplier
        if monster.type == MonsterType.BOSS:
            damage += damage * (player_stats["boss_damage"] / 100)

        # Penetration multiplier. Cant be over 100%
        damage *= min(player_stats["penetration"] / 100, 1)

        return int(damage)

    async def attack(self, discord_id: int):
        player = await self.get_or_insert_player(discord_id)
        player_gear = await self.get_player_gear(discord_id)
        location = location_data[player.location]
        monster_name = location.get_random_monster()
        monster = monster_data[monster_name]

        current_time = datetime.datetime.now()

        # Check if the player is on cooldown
        if discord_id in self.player_cooldowns:
            cooldown_end = self.player_cooldowns[discord_id]
            if current_time < cooldown_end:
                # Player is still on cooldown
                return {
                    'kills': 0,
                    'exp': 0,
                    'gold': 0,
                    'loot': [],
                    'monster': '',
                    'on_cooldown': True,
                    'cooldown_expiration': cooldown_end,
                    'location': location.name,
                    'player_exp': player.exp,
                    'leveled_up': False
                }
        

        damage = await self.calculate_attack_damage(monster, player, player_gear)
        kill_rate = damage / monster.hp

        # If kill rate < 1, then that is the chance of successfully killing an enemy.
        # If kill rate >= 1, then that is the number of monsters slain
        if kill_rate < 1:
            kills = 1 if random.random() < kill_rate else 0
        kills = int(kill_rate)

        weapon = await self.get_weapon(player_gear)
        weapon_data = gear_data[weapon.name]

        exp_gained = self.random_within_range(int(monster.exp * kills))

        cooldown_expiration = current_time + datetime.timedelta(seconds=weapon_data.attack_cooldown)

        attack_results = {
            'kills': kills,
            'exp': exp_gained,
            'gold': self.random_within_range(int(monster.gold * kills)),
            'loot': [],
            'monster': monster.display_monster(),
            'location': location.name,
            'player_exp': player.exp + exp_gained,
            'on_cooldown': False,
            'cooldown_expiration': cooldown_expiration,
            'leveled_up': self.exp_to_level(player.exp + exp_gained) > self.exp_to_level(player.exp)
        }

        await self.increment_exp(discord_id, attack_results["exp"])
        await self.increment_gold(discord_id, attack_results["gold"])

        self.player_cooldowns[discord_id] = cooldown_expiration

        return attack_results

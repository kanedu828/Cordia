import datetime
from typing import List, Tuple
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
from cordia.util.exp_util import exp_to_level
from cordia.util.stats_util import get_player_stats, get_upgrade_points, level_difference_multiplier, random_within_range

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
        upgrade_points = get_upgrade_points(player)
        if increment_by > upgrade_points or increment_by < 0:
            raise ValueError('Invalid increment amount')
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

    # Battle
    async def calculate_attack_damage(self, monster: Monster, player: Player, player_gear: List[PlayerGear]) -> Tuple[int, bool]:
        player_stats = get_player_stats(player, player_gear)

        # Multiplier depending on player's level compared to monster's
        level_damage_multiplier = level_difference_multiplier(exp_to_level(player.exp), monster.level)
        damage = player_stats["strength"] * level_damage_multiplier

        damage = random_within_range(damage)

        # Calculate crit
        crit_multiplier = 1.5
        is_crit = random.random() < player_stats["crit_chance"] / 100
        if is_crit:
            damage *= crit_multiplier

        # Boss damage multiplier
        if monster.type == MonsterType.BOSS:
            damage += damage * (player_stats["boss_damage"] / 100)

        # Penetration multiplier. Cant be over 100%
        monster_defense_percentage = (monster.defense / 100)
        monster_defense_percentage -= monster_defense_percentage * (min(player_stats["penetration"], 100) / 100)
        damage -= damage * monster_defense_percentage

        return int(damage), is_crit

    async def attack(self, discord_id: int):
        player = await self.get_or_insert_player(discord_id)
        player_gear = await self.get_player_gear(discord_id)
        player_stats = get_player_stats(player, player_gear)
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
                    'location': location,
                    'player_exp': player.exp,
                    'leveled_up': False,
                    'is_crit': False,
                    'damage': 0,
                    'is_combo': False
                }
        

        damage, is_crit = await self.calculate_attack_damage(monster, player, player_gear)
        kill_rate = damage / monster.hp

        # If kill rate < 1, then that is the chance of successfully killing an enemy.
        # If kill rate >= 1, then that is the number of monsters slain
        if kill_rate < 1:
            kills = 1 if random.random() < kill_rate else 0

        kills = min(int(kill_rate), player_stats['strike_radius'])

        weapon = await self.get_weapon(player_gear)
        weapon_data = gear_data[weapon.name]

        exp_gained = random_within_range(int(monster.exp * kills))

        cooldown_expiration = current_time + datetime.timedelta(seconds=weapon_data.attack_cooldown)

        is_combo = random.random() < player_stats['combo_chance'] / 100
        if is_combo:
            cooldown_expiration = 1

        attack_results = {
            'kills': kills,
            'exp': exp_gained,
            'gold': random_within_range(int(monster.gold * kills)),
            'loot': [],
            'monster': monster.display_monster(),
            'location': location,
            'player_exp': player.exp + exp_gained,
            'on_cooldown': False,
            'cooldown_expiration': cooldown_expiration,
            'leveled_up': exp_to_level(player.exp + exp_gained) > exp_to_level(player.exp),
            'is_crit': is_crit,
            'damage': damage,
            'is_combo': is_combo
        }

        await self.increment_exp(discord_id, attack_results["exp"])
        await self.increment_gold(discord_id, attack_results["gold"])

        self.player_cooldowns[discord_id] = cooldown_expiration

        return attack_results

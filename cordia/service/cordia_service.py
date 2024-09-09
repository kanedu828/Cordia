import datetime
from typing import List, Literal, Tuple
from cordia.dao.boss_instance_dao import BossInstanceDao
from cordia.dao.item_dao import ItemDao
from cordia.dao.player_dao import PlayerDao
from cordia.data.locations import location_data
from cordia.dao.player_gear_dao import PlayerGearDao
from cordia.dao.gear_dao import GearDao
from cordia.data.gear import gear_data
from cordia.data.bosses import boss_data
import random

from cordia.data.monsters import monster_data
from cordia.model.attack_result import AttackResult
from cordia.model.boos_fight_result import BossFightResult
from cordia.model.boss_instance import BossInstance
from cordia.model.gear_instance import GearInstance
from cordia.model.player import Player
from cordia.model.gear import GearType
from cordia.model.monster import Monster, MonsterType
from cordia.util.exp_util import exp_to_level
from cordia.util.gear_util import get_weapon_from_player_gear
from cordia.util.stats_util import (
    calculate_weighted_monster_mean,
    get_player_stats,
    get_upgrade_points,
    level_difference_multiplier,
    random_within_range,
    simulate_idle_damage,
)


class CordiaService:
    def __init__(
        self,
        player_dao: PlayerDao,
        gear_dao: GearDao,
        player_gear_dao: PlayerGearDao,
        boss_instance_dao: BossInstanceDao,
        item_dao: ItemDao
    ):
        self.player_dao = player_dao
        self.gear_dao = gear_dao
        self.player_gear_dao = player_gear_dao
        self.boss_instance_dao = boss_instance_dao
        self.item_dao = item_dao

        self.player_cooldowns = {"attack": {}, "cast_spell": {}}
        self.boss_time_remaining = {}

    # Player
    async def get_player_by_discord_id(self, discord_id: int) -> Player | None:
        return await self.player_dao.get_by_discord_id(discord_id)

    async def insert_player(self, discord_id: int) -> Player:
        return await self.player_dao.insert_player(discord_id)

    async def get_or_insert_player(self, discord_id: int) -> Player:
        player = await self.get_player_by_discord_id(discord_id)
        if player:
            return player
        else:
            player = await self.insert_player(discord_id)
            return player

    async def increment_stat(self, discord_id: int, stat_name: str, increment_by: int):
        player = await self.player_dao.get_by_discord_id(discord_id)
        upgrade_points = get_upgrade_points(player)
        if increment_by > upgrade_points or increment_by < 0:
            raise ValueError("Invalid increment amount")
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
            raise ValueError(f"{location} is not a valid locatin")
        await self.player_dao.update_location(discord_id, location)

    async def update_last_idle_claim(self, discord_id: int, last_idle_claim: datetime):
        return await self.player_dao.update_last_idle_claim(discord_id, last_idle_claim)

    async def count_players_in_location(self, location: str) -> int:
        return await self.player_dao.count_players_in_location(location)

    async def update_last_boss_killed(self, discord_id):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        await self.player_dao.update_last_boss_killed(discord_id, current_time)

    # Gear
    async def insert_gear(self, discord_id: int, name: str):
        return await self.gear_dao.insert_gear(discord_id, name)

    async def get_gear_by_id(self, id: int) -> GearInstance:
        return await self.gear_dao.get_gear_by_id(id)

    async def get_armory(self, discord_id: int) -> List[GearInstance]:
        return await self.gear_dao.get_gear_by_discord_id(discord_id)

    async def increment_gear_stars(self, gear_id: int, stars: int):
        gear = await self.gear_dao.get_gear_by_id(gear_id)
        await self.gear_dao.update_gear_stars(gear_id, gear.stars + stars)

    # Player Gear
    async def get_player_gear(self, discord_id: int):
        return await self.player_gear_dao.get_player_gear(discord_id)

    async def equip_gear(self, discord_id: int, gear_id: int, slot: str):
        gi = await self.get_gear_by_id(gear_id)
        gd = gear_data[gi.name]
        current_time = datetime.datetime.now(datetime.timezone.utc)
        attack_cooldown_expiration = current_time + datetime.timedelta(
            seconds=gd.attack_cooldown
        )
        self.player_cooldowns["attack"][discord_id] = attack_cooldown_expiration
        if gd.spell:
            spell_cooldown_expiration = current_time + datetime.timedelta(
                seconds=gd.spell.spell_cooldown
            )
            self.player_cooldowns["cast_spell"][discord_id] = spell_cooldown_expiration
        return await self.player_gear_dao.equip_gear(discord_id, gear_id, slot)

    async def remove_gear(self, discord_id: int, slot: str):
        await self.player_gear_dao.remove_gear(discord_id, slot)

    def get_weapon(self, player_gear: List[GearInstance]) -> GearInstance:
        return next((x for x in player_gear if x.slot == GearType.WEAPON.value), None)

    async def get_player_gear_by_gear_id(self, gear_id: int) -> GearInstance:
        return await self.player_gear_dao.get_by_gear_id(gear_id)

    # Boss Instance
    async def get_boss_by_discord_id(self, discord_id: int) -> BossInstance:
        return await self.boss_instance_dao.get_boss_by_discord_id(discord_id)

    async def update_boss_hp(self, discord_id: int, current_hp: int):
        await self.boss_instance_dao.update_boss_hp(discord_id, current_hp)

    async def insert_boss(self, discord_id: int, name: str):
        current_time = datetime.datetime.now(
            datetime.timezone.utc
        )
        expiration_time = current_time + datetime.timedelta(hours=1)
        bd = boss_data[name]
        self.boss_time_remaining[discord_id] = expiration_time
        await self.boss_instance_dao.insert_boss(
            discord_id, bd.hp, name, expiration_time
        )

    async def delete_boss(self, discord_id):
        await self.boss_instance_dao.delete_boss_by_discord_id(discord_id)

    # Battle
    async def boss_fight(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> BossFightResult:
        boss_instance = await self.get_boss_by_discord_id(discord_id)
        if self.is_cooldown(discord_id, action):
            return BossFightResult(
                on_cooldown=True,
                cooldown_expiration=self.player_cooldowns[action][discord_id],
                boss_instance=boss_instance,
            )

        current_time = datetime.datetime.now(datetime.timezone.utc)

        if current_time > boss_instance.expiration_time:
            await self.delete_boss(discord_id)
            return BossFightResult(
                is_expired=True,
                boss_expiration=boss_instance.expiration_time,
                boss_instance=boss_instance,
            )

        player = await self.get_player_by_discord_id(discord_id)
        player_gear = await self.get_player_gear(discord_id)
        player_stats = get_player_stats(player, player_gear)
        weapon = get_weapon_from_player_gear(player_gear)
        weapon_data = gear_data[weapon.name]
        boss = boss_data[boss_instance.name]

        # Deal damage
        damage, is_crit = self.calculate_attack_damage(
            boss, player, player_gear, action
        )
        await self.update_boss_hp(discord_id, boss_instance.current_hp - damage)
        boss_instance.current_hp = boss_instance.current_hp - damage

        exp_gained = 0
        gold_gained = 0

        # If boss is killed
        new_gear_loot = []
        sold_gear_amount = 0
        if boss_instance.current_hp <= 0:
            exp_gained = random_within_range(
                int((boss.exp + min(player_stats["efficiency"], boss.exp)))
            )

            gold_gained = random_within_range(
                int((boss.gold + min(player_stats["luck"], boss.gold)))
            )

            await self.increment_exp(discord_id, exp_gained)
            await self.increment_gold(discord_id, gold_gained)

            # Handle gear drops
            gear_loot = boss.get_dropped_gear()

            for g in gear_loot:
                gd = gear_data[g]
                try:
                    await self.insert_gear(discord_id, g)
                    new_gear_loot.append(gd)
                except:
                    sold_gear_amount += gd.gold_value

            await self.increment_gold(discord_id, sold_gear_amount)
            await self.delete_boss(discord_id)
            await self.update_last_boss_killed(discord_id)

        # Get cooldown expiration
        cooldown_expiration = current_time + datetime.timedelta(
            seconds=weapon_data.attack_cooldown
        )

        is_combo = random.random() < player_stats["combo_chance"] / 100
        if is_combo:
            cooldown_expiration = current_time + datetime.timedelta(seconds=1)

        self.player_cooldowns[action][discord_id] = cooldown_expiration

        boss_fight_result = BossFightResult(
            boss_instance=boss_instance,
            killed=boss_instance.current_hp <= 0,
            exp=exp_gained,
            gold=gold_gained,
            gear_loot=new_gear_loot,
            sold_gear_amount=sold_gear_amount,
            on_cooldown=False,
            cooldown_expiration=cooldown_expiration,
            leveled_up=exp_to_level(player.exp + exp_gained) > exp_to_level(player.exp),
            is_crit=is_crit,
            damage=damage,
            is_combo=is_combo,
            boss_expiration=boss_instance.expiration_time,
            player_exp=player.exp + exp_gained,
            weapon=weapon_data
        )

        if action == "cast_spell" and weapon_data.spell:
            boss_fight_result.cooldown_expiration = current_time + datetime.timedelta(
                seconds=weapon_data.spell.spell_cooldown
            )
        return boss_fight_result

    async def idle_fight(self, discord_id: int):
        player: Player = await self.get_player_by_discord_id(discord_id)
        player_gear = await self.get_player_gear(discord_id)
        weapon = get_weapon_from_player_gear(player_gear)

        player_stats = get_player_stats(player, player_gear)
        last_idle_claim = player.last_idle_claim
        time_passed = min(
            datetime.datetime.now(datetime.timezone.utc) - last_idle_claim,
            datetime.timedelta(hours=8),
        )

        IDLE_FREQUENCY_MULTIPLIER = 20
        idle_frequency = (
            gear_data[get_weapon_from_player_gear(player_gear).name].attack_cooldown
            * IDLE_FREQUENCY_MULTIPLIER
        )

        location = location_data[player.location]
        monsters = location.monsters
        monsters = [(monster_data[m[0]], m[1]) for m in monsters]

        monster_mean = calculate_weighted_monster_mean(monsters)

        times_attacked = int(time_passed.total_seconds() / idle_frequency)

        gold_gained = monster_mean["gold"] + player_stats["luck"]
        exp_gained = monster_mean["exp"] + player_stats["efficiency"]
        damage = player_stats["damage"] + player_stats["persistence"]

        player_level = exp_to_level(player.exp)
        damage = simulate_idle_damage(damage, monster_mean, player_stats, player_level)

        # Kill rate, cannot exceed strike radius
        kill_rate = min(
            (damage / monster_mean["hp"]), gear_data[weapon.name].strike_radius
        )
        gold_gained *= kill_rate * times_attacked
        exp_gained *= kill_rate * times_attacked
        gold_gained = int(gold_gained)
        exp_gained = int(exp_gained)

        dpm = round(damage * 60 / idle_frequency, 2)

        if time_passed > datetime.timedelta(minutes=10):
            await self.update_last_idle_claim(
                discord_id, datetime.datetime.now(datetime.timezone.utc)
            )
            await self.increment_exp(discord_id, exp_gained)
            await self.increment_gold(discord_id, gold_gained)
        else:
            return {
                "dps": 0,
                "gold_gained": 0,
                "exp_gained": 0,
                "location": location_data[player.location],
                "time_passed": time_passed,
                "current_exp": player.exp,
                "leveled_up": False,
            }

        return {
            "dpm": dpm,
            "gold_gained": gold_gained,
            "exp_gained": exp_gained,
            "location": location_data[player.location],
            "time_passed": time_passed,
            "current_exp": player.exp + exp_gained,
            "leveled_up": exp_to_level(player.exp + exp_gained)
            > exp_to_level(player.exp),
        }

    def calculate_attack_damage(
        self,
        monster: Monster,
        player: Player,
        player_gear: List[GearInstance],
        action: Literal["attack", "cast_spell"] = "attack",
    ) -> Tuple[int, bool]:
        player_stats = get_player_stats(player, player_gear)
        # Multiplier depending on player's level compared to monster's
        level_damage_multiplier = level_difference_multiplier(
            exp_to_level(player.exp), monster.level
        )
        weapon = self.get_weapon(player_gear)
        spell = gear_data[weapon.name].spell

        if action == "cast_spell" and spell:
            damage = spell.damage + (
                player_stats[spell.scaling_stat] * spell.scaling_multiplier
            )
        else:
            damage = player_stats["damage"] + player_stats["strength"]

        damage = random_within_range(damage)
        damage *= level_damage_multiplier

        # Calculate crit
        CRIT_MULTIPLIER = 1.5
        is_crit = random.random() < player_stats["crit_chance"] / 100
        if is_crit:
            damage *= CRIT_MULTIPLIER

        # Boss damage multiplier
        if monster.type == MonsterType.BOSS:
            damage += damage * (player_stats["boss_damage"] / 100)

        if action == "cast_spell" and spell and spell.scaling_stat == "intelligence":
            monster_resistance_percentage = monster.resistance / 100
            monster_resistance_percentage -= monster_resistance_percentage * (
                min(spell.magic_penetration, 100) / 100
            )
            damage -= damage * monster_resistance_percentage
        else:
            # Penetration multiplier. Cant be over 100%
            monster_defense_percentage = monster.defense / 100
            monster_defense_percentage -= monster_defense_percentage * (
                min(player_stats["penetration"], 100) / 100
            )
            damage -= damage * monster_defense_percentage

        return int(damage), is_crit

    def is_cooldown(
        self, discord_id: int, action: Literal["attack", "cast_spell"]
    ) -> bool:
        # Check if the player is on cooldown
        current_time = datetime.datetime.now(datetime.timezone.utc)
        if discord_id in self.player_cooldowns[action]:
            cooldown_end = self.player_cooldowns[action][discord_id]
            if current_time < cooldown_end:
                # Player is still on cooldown
                return True
        return False

    async def attack(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> AttackResult:

        player = await self.get_or_insert_player(discord_id)
        player_gear = await self.get_player_gear(discord_id)
        player_stats = get_player_stats(player, player_gear)
        location = location_data[player.location]
        if self.is_cooldown(discord_id, action):
            return AttackResult(
                on_cooldown=True,
                cooldown_expiration=self.player_cooldowns[action][discord_id],
                location=location,
                player_exp=player.exp,
            )
        monster_name = location.get_random_monster()
        monster = monster_data[monster_name]

        current_time = datetime.datetime.now(datetime.timezone.utc)

        damage, is_crit = self.calculate_attack_damage(
            monster, player, player_gear, action
        )
        kill_rate = float(damage) / monster.hp

        weapon = self.get_weapon(player_gear)
        weapon_data = gear_data[weapon.name]
        # If kill rate < 1, then that is the chance of successfully killing an enemy.
        # If kill rate >= 1, then that is the number of monsters slain
        if kill_rate < 1:
            r = random.random()
            kills = 1 if r < kill_rate else 0
        else:
            kills = min(int(kill_rate), player_stats["strike_radius"])
            if action == "cast_spell" and weapon_data.spell:
                kills = min(int(kill_rate), weapon_data.spell.strike_radius)

        exp_gained = random_within_range(
            int((monster.exp + min(player_stats["efficiency"], monster.exp)) * kills)
        )

        gold_gained = random_within_range(
            int((monster.gold + min(player_stats["luck"], monster.gold)) * kills)
        )

        cooldown_expiration = current_time + datetime.timedelta(
            seconds=weapon_data.attack_cooldown
        )

        is_combo = random.random() < player_stats["combo_chance"] / 100
        if is_combo:
            cooldown_expiration = current_time + datetime.timedelta(seconds=1)

        # Handle gear drops
        gear_loot = monster.get_dropped_gear(kills)
        sold_gear_amount = 0
        new_gear_loot = []
        for g in gear_loot:
            gd = gear_data[g]
            try:
                await self.insert_gear(discord_id, g)
                new_gear_loot.append(gd)
            except:
                sold_gear_amount += gd.gold_value

        await self.increment_gold(discord_id, sold_gear_amount)

        attack_result = AttackResult(
            kills=kills,
            exp=exp_gained,
            gold=gold_gained,
            monster=monster.display_monster(),
            location=location,
            player_exp=player.exp + exp_gained,
            leveled_up=exp_to_level(player.exp + exp_gained) > exp_to_level(player.exp),
            is_crit=is_crit,
            damage=damage,
            is_combo=is_combo,
            cooldown_expiration=cooldown_expiration,
            gear_loot=new_gear_loot,
            sold_gear_amount=sold_gear_amount,
            weapon=weapon_data
        )

        if action == "cast_spell" and weapon_data.spell:
            attack_result.cooldown_expiration = current_time + datetime.timedelta(
                seconds=weapon_data.spell.spell_cooldown
        )

        await self.increment_exp(discord_id, attack_result.exp)
        await self.increment_gold(discord_id, attack_result.gold)

        self.player_cooldowns[action][discord_id] = cooldown_expiration

        return attack_result

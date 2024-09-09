import datetime
import random
from typing import Literal
from cordia.model.attack_result import AttackResult
from cordia.model.boos_fight_result import BossFightResult
from cordia.model.player import Player
from cordia.service.boss_service import BossService
from cordia.service.cooldown_service import CooldownService
from cordia.service.gear_service import GearService
from cordia.service.loot_service import LootService
from cordia.service.player_service import PlayerService
from cordia.util.battle_util import calculate_attack_damage
from cordia.util.exp_util import exp_to_level
from cordia.util.gear_util import get_weapon_from_player_gear
from cordia.util.stats_util import (
    calculate_weighted_monster_mean,
    get_player_stats,
    simulate_idle_damage,
)
from cordia.data.gear import gear_data
from cordia.data.bosses import boss_data
from cordia.data.monsters import monster_data
from cordia.data.locations import location_data


class BattleService:
    def __init__(
        self,
        player_service: PlayerService,
        gear_service: GearService,
        boss_service: BossService,
        cooldown_service: CooldownService,
        loot_service: LootService,
    ):
        self.player_service = player_service
        self.gear_service = gear_service
        self.boss_service = boss_service
        self.cooldown_service = cooldown_service
        self.loot_service = loot_service

    async def boss_fight(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> BossFightResult:
        boss_instance = await self.boss_service.get_boss_by_discord_id(discord_id)
        if self.cooldown_service.is_on_cooldown(discord_id, action):
            return BossFightResult(
                on_cooldown=True,
                cooldown_expiration=self.cooldown_service.get_cooldown_expiration(
                    discord_id, action
                ),
                boss_instance=boss_instance,
            )

        current_time = datetime.datetime.now(datetime.timezone.utc)

        if current_time > boss_instance.expiration_time:
            await self.boss_service.delete_boss(discord_id)
            return BossFightResult(
                is_expired=True,
                boss_expiration=boss_instance.expiration_time,
                boss_instance=boss_instance,
            )

        player = await self.player_service.get_player_by_discord_id(discord_id)
        player_gear = await self.gear_service.get_player_gear(discord_id)
        player_stats = get_player_stats(player, player_gear)
        weapon = get_weapon_from_player_gear(player_gear)
        weapon_data = gear_data[weapon.name]
        boss = boss_data[boss_instance.name]

        # Deal damage
        damage, is_crit = calculate_attack_damage(boss, player, player_gear, action)
        await self.boss_service.update_boss_hp(
            discord_id, boss_instance.current_hp - damage
        )
        boss_instance.current_hp = boss_instance.current_hp - damage

        exp_gained = 0
        gold_gained = 0

        # If boss is killed
        new_gear_loot = []
        sold_gear_amount = 0
        if boss_instance.current_hp <= 0:
            exp_gained, gold_gained, new_gear_loot, sold_gear_amount = (
                await self.loot_service.handle_loot(discord_id, boss, player_stats, 1)
            )
            await self.player_service.update_last_boss_killed(discord_id)
            await self.boss_service.delete_boss(discord_id)

        # Get cooldown expiration
        cooldown_expiration = current_time + datetime.timedelta(
            seconds=weapon_data.attack_cooldown
        )

        is_combo = random.random() < player_stats["combo_chance"] / 100
        if is_combo:
            cooldown_expiration = current_time + datetime.timedelta(seconds=1)

        self.cooldown_service.set_cooldown(discord_id, action, cooldown_expiration)

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
            weapon=weapon_data,
        )

        if action == "cast_spell" and weapon_data.spell:
            boss_fight_result.cooldown_expiration = current_time + datetime.timedelta(
                seconds=weapon_data.spell.spell_cooldown
            )
        return boss_fight_result

    async def idle_fight(self, discord_id: int):
        player: Player = await self.player_service.get_player_by_discord_id(discord_id)
        player_gear = await self.gear_service.get_player_gear(discord_id)
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
            await self.player_service.update_last_idle_claim(
                discord_id, datetime.datetime.now(datetime.timezone.utc)
            )
            await self.player_service.increment_exp(discord_id, exp_gained)
            await self.player_service.increment_gold(discord_id, gold_gained)
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

    async def attack(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> AttackResult:
        player = await self.player_service.get_or_insert_player(discord_id)
        player_gear = await self.gear_service.get_player_gear(discord_id)
        player_stats = get_player_stats(player, player_gear)
        location = location_data[player.location]
        if self.cooldown_service.is_on_cooldown(discord_id, action):
            return AttackResult(
                on_cooldown=True,
                cooldown_expiration=self.cooldown_service.get_cooldown_expiration(
                    discord_id, action
                ),
                location=location,
                player_exp=player.exp,
            )
        monster_name = location.get_random_monster()
        monster = monster_data[monster_name]

        current_time = datetime.datetime.now(datetime.timezone.utc)

        damage, is_crit = calculate_attack_damage(monster, player, player_gear, action)
        kill_rate = float(damage) / monster.hp

        weapon = get_weapon_from_player_gear(player_gear)
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

        cooldown_expiration = current_time + datetime.timedelta(
            seconds=weapon_data.attack_cooldown
        )

        is_combo = random.random() < player_stats["combo_chance"] / 100
        if is_combo:
            cooldown_expiration = current_time + datetime.timedelta(seconds=1)

        exp_gained, gold_gained, new_gear_loot, sold_gear_amount = (
            await self.loot_service.handle_loot(
                discord_id, monster, player_stats, kills
            )
        )

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
            weapon=weapon_data,
        )

        if action == "cast_spell" and weapon_data.spell:
            attack_result.cooldown_expiration = current_time + datetime.timedelta(
                seconds=weapon_data.spell.spell_cooldown
            )

        self.cooldown_service.set_cooldown(discord_id, action, cooldown_expiration)

        return attack_result

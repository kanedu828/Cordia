from typing import List, Literal

from cordia.model.attack_result import AttackResult
from cordia.model.boos_fight_result import BossFightResult
from cordia.model.boss_instance import BossInstance
from cordia.model.gear_instance import GearInstance
from cordia.model.player import Player

from cordia.service.battle_service import BattleService
from cordia.service.boss_service import BossService
from cordia.service.gear_service import GearService
from cordia.service.player_service import PlayerService


class CordiaService:
    def __init__(
        self,
        player_service: PlayerService,
        gear_service: GearService,
        boss_service: BossService,
        battle_service: BattleService,
    ):
        self.player_service = player_service
        self.gear_service = gear_service
        self.boss_service = boss_service
        self.battle_service = battle_service

    # Player
    async def get_player_by_discord_id(self, discord_id: int) -> Player | None:
        return await self.player_service.get_player_by_discord_id(discord_id)

    async def insert_player(self, discord_id: int) -> Player:
        return await self.player_service.insert_player(discord_id)

    async def get_or_insert_player(self, discord_id: int) -> Player:
        player = await self.get_player_by_discord_id(discord_id)
        if player:
            return player
        else:
            player = await self.insert_player(discord_id)
            return player

    async def increment_stat(self, discord_id: int, stat_name: str, increment_by: int):
        await self.player_service.increment_stat(discord_id, stat_name, increment_by)

    async def increment_gold(self, discord_id: int, increment_by: int):
        await self.player_service.increment_gold(discord_id, increment_by)

    async def update_location(self, discord_id: int, location: str):
        await self.player_service.update_location(discord_id, location)

    async def count_players_in_location(self, location: str) -> int:
        return await self.player_service.count_players_in_location(location)

    # Gear
    async def insert_gear(self, discord_id: int, name: str):
        return await self.gear_service.insert_gear(discord_id, name)

    async def get_gear_by_id(self, id: int) -> GearInstance:
        return await self.gear_service.get_gear_by_id(id)

    async def get_armory(self, discord_id: int) -> List[GearInstance]:
        return await self.gear_service.get_armory(discord_id)

    async def increment_gear_stars(self, gear_id: int, stars: int):
        await self.gear_service.increment_gear_stars(gear_id, stars)

    # Player Gear
    async def get_player_gear(self, discord_id: int):
        return await self.gear_service.get_player_gear(discord_id)

    async def equip_gear(self, discord_id: int, gear_id: int, slot: str):
        return await self.gear_service.equip_gear(discord_id, gear_id, slot)

    async def remove_gear(self, discord_id: int, slot: str):
        await self.gear_service.remove_gear(discord_id, slot)

    async def get_player_gear_by_gear_id(self, gear_id: int) -> GearInstance:
        return await self.gear_service.get_player_gear_by_gear_id(gear_id)

    # Boss Instance
    async def get_boss_by_discord_id(self, discord_id: int) -> BossInstance:
        return await self.boss_service.get_boss_by_discord_id(discord_id)

    async def update_boss_hp(self, discord_id: int, current_hp: int):
        await self.boss_service.update_boss_hp(discord_id, current_hp)

    async def insert_boss(self, discord_id: int, name: str):
        await self.boss_service.insert_boss(discord_id, name)

    async def delete_boss(self, discord_id):
        await self.boss_service.delete_boss(discord_id)

    # Battle
    async def boss_fight(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> BossFightResult:
        return await self.battle_service.boss_fight(discord_id, action)

    async def idle_fight(self, discord_id: int):
        return await self.battle_service.idle_fight(discord_id)

    async def attack(
        self, discord_id: int, action: Literal["attack", "cast_spell"] = "attack"
    ) -> AttackResult:
        return await self.battle_service.attack(discord_id, action)

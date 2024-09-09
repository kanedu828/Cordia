import datetime
from typing import List
from cordia.dao.gear_dao import GearDao
from cordia.dao.player_gear_dao import PlayerGearDao
from cordia.model.gear import GearType
from cordia.model.gear_instance import GearInstance
from cordia.data.gear import gear_data


class GearService:
    def __init__(self, gear_dao: GearDao, player_gear_dao: PlayerGearDao):
        self.gear_dao = gear_dao
        self.player_gear_dao = player_gear_dao

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

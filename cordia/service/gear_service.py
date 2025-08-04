import logging
from typing import List
from cordia.dao.gear_dao import GearDao
from cordia.dao.player_gear_dao import PlayerGearDao
from cordia.model.gear import GearType
from cordia.model.gear_instance import GearInstance
from cordia.service.player_service import PlayerService
from cordia.util.exp_util import exp_to_level
# Set up logger for this module
logger = logging.getLogger(__name__)


class GearService:
    def __init__(self, gear_dao: GearDao, player_gear_dao: PlayerGearDao, player_service: PlayerService):
        self.gear_dao = gear_dao
        self.player_gear_dao = player_gear_dao
        self.player_service = player_service
        logger.info("GearService initialized")

    # Gear
    async def insert_gear(self, discord_id: int, name: str):
        logger.info(f"Inserting gear for user {discord_id}: {name}")
        gear = await self.gear_dao.insert_gear(discord_id, name)
        logger.info(f"Created gear instance {gear.id} for user {discord_id}: {name}")
        return gear

    async def get_gear_by_id(self, id: int) -> GearInstance:
        logger.debug(f"Getting gear by ID: {id}")
        gear = await self.gear_dao.get_gear_by_id(id)
        if gear:
            gear_data = gear.get_gear_data()
            logger.debug(f"Found gear {id}: {gear.name} (level {gear_data.level})")
        else:
            logger.debug(f"No gear found for ID: {id}")
        return gear

    async def get_armory(self, discord_id: int) -> List[GearInstance]:
        logger.debug(f"Getting armory for user {discord_id}")
        armory = await self.gear_dao.get_gear_by_discord_id(discord_id)
        logger.debug(f"Retrieved {len(armory)} gear items for user {discord_id}")
        return armory

    async def increment_gear_stars(self, gear_id: int, stars: int):
        logger.info(f"Incrementing stars for gear {gear_id} by {stars}")
        gear = await self.gear_dao.get_gear_by_id(gear_id)
        new_stars = gear.stars + stars
        await self.gear_dao.update_gear_stars(gear_id, new_stars)
        logger.info(f"Updated gear {gear_id} stars: {new_stars}")

    async def update_gear_bonus(self, gear_id: int, bonus: str):
        logger.info(f"Updating bonus for gear {gear_id} to {bonus}")
        await self.gear_dao.update_bonus(gear_id, bonus)
        logger.debug(f"Updated gear {gear_id} bonus: {bonus}")

    async def equip_highest_level_gear(self, discord_id: int) -> list[str]:
        player = await self.player_service.get_player_by_discord_id(discord_id=discord_id)
        level = exp_to_level(player.exp)
        logger.info(f"Equipping highest level gear for user {discord_id} at level {level}")
        armory = await self.get_armory(discord_id)
        armory = [a for a in armory if a.get_gear_data().level <= level]
        armory.sort(key=lambda x: x.get_gear_data().level, reverse=True)
        equipped_types = set()
        equipped_gear = []
        for i in armory:
            gd = i.get_gear_data()
            if gd.type not in equipped_types:
                await self.equip_gear(discord_id, i.id, gd.type.value)
                equipped_types.add(gd.type)
                equipped_gear.append(gd.name)
                logger.debug(f"Equipped {gd.name} for user {discord_id}")
        logger.info(f"Equipped {len(equipped_gear)} gear items for user {discord_id}: {equipped_gear}")
        return equipped_gear

    # Player Gear
    async def get_player_gear(self, discord_id: int):
        logger.debug(f"Getting equipped gear for user {discord_id}")
        player_gear = await self.player_gear_dao.get_player_gear(discord_id)
        logger.debug(f"Retrieved {len(player_gear)} equipped gear items for user {discord_id}")
        return player_gear

    async def equip_gear(self, discord_id: int, gear_id: int, slot: str):
        logger.info(f"Equipping gear {gear_id} to slot {slot} for user {discord_id}")
        result = await self.player_gear_dao.equip_gear(discord_id, gear_id, slot)
        logger.info(f"Equipped gear {gear_id} to slot {slot} for user {discord_id}")
        return result

    async def remove_all_gear(self, discord_id: int):
        logger.info(f"Removing all gear for user {discord_id}")
        await self.player_gear_dao.remove_all_gear(discord_id)
        logger.info(f"Removed all gear for user {discord_id}")

    def get_weapon(self, player_gear: List[GearInstance]) -> GearInstance:
        weapon = next((x for x in player_gear if x.slot == GearType.WEAPON.value), None)
        if weapon:
            logger.debug(f"Found weapon: {weapon.name}")
        else:
            logger.debug("No weapon found in player gear")
        return weapon

    async def get_player_gear_by_gear_id(self, gear_id: int) -> GearInstance:
        logger.debug(f"Getting player gear by gear ID: {gear_id}")
        player_gear = await self.player_gear_dao.get_by_gear_id(gear_id)
        if player_gear:
            logger.debug(f"Found player gear {gear_id} for user {player_gear.discord_id}")
        else:
            logger.debug(f"No player gear found for gear ID: {gear_id}")
        return player_gear

    def get_gear_stats(self) -> dict:
        """Get statistics about gear operations for monitoring."""
        stats = {
            "service_name": "GearService"
        }
        logger.debug(f"Gear service stats: {stats}")
        return stats

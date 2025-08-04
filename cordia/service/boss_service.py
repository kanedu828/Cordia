import datetime
import logging
from cordia.dao.boss_instance_dao import BossInstanceDao
from cordia.model.boss_instance import BossInstance
from cordia.data.bosses import boss_data

# Set up logger for this module
logger = logging.getLogger(__name__)


class BossService:
    def __init__(self, boss_instance_dao: BossInstanceDao):
        self.boss_instance_dao = boss_instance_dao
        self.boss_time_remaining = {}
        logger.info("BossService initialized")

    async def get_boss_by_discord_id(self, discord_id: int) -> BossInstance:
        logger.debug(f"Getting boss for user {discord_id}")
        boss = await self.boss_instance_dao.get_boss_by_discord_id(discord_id)
        if boss:
            logger.debug(f"Found boss for user {discord_id}: {boss.name} with {boss.current_hp} HP")
        else:
            logger.debug(f"No boss found for user {discord_id}")
        return boss

    async def update_boss_hp(self, discord_id: int, current_hp: int):
        logger.info(f"Updating boss HP for user {discord_id} to {current_hp}")
        await self.boss_instance_dao.update_boss_hp(discord_id, current_hp)

    async def insert_boss(self, discord_id: int, name: str):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        expiration_time = current_time + datetime.timedelta(hours=1)
        bd = boss_data[name]
        self.boss_time_remaining[discord_id] = expiration_time
        logger.info(f"Inserting boss for user {discord_id}: {name} with {bd.hp} HP, expires at {expiration_time}")
        await self.boss_instance_dao.insert_boss(
            discord_id, bd.hp, name, expiration_time
        )

    def get_boss_time_remaining(self, discord_id: int):
        remaining_time = self.boss_time_remaining.get(discord_id, None)
        logger.debug(f"Getting boss time remaining for user {discord_id}: {remaining_time}")
        return remaining_time

    async def delete_boss(self, discord_id):
        logger.info(f"Deleting boss for user {discord_id}")
        await self.boss_instance_dao.delete_boss_by_discord_id(discord_id)

    def get_boss_stats(self) -> dict:
        """Get statistics about current boss instances for monitoring."""
        stats = {
            "active_bosses": len(self.boss_time_remaining)
        }
        logger.debug(f"Boss stats: {stats}")
        return stats

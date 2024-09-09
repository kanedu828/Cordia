import datetime
from cordia.dao.boss_instance_dao import BossInstanceDao
from cordia.model.boss_instance import BossInstance
from cordia.data.bosses import boss_data


class BossService:
    def __init__(self, boss_instance_dao: BossInstanceDao):
        self.boss_instance_dao = boss_instance_dao

        self.boss_time_remaining = {}

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
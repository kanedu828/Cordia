import unittest
import datetime
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.boss_service import BossService
from cordia.model.boss_instance import BossInstance


class TestBossService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_boss_instance_dao = Mock()
        self.boss_service = BossService(self.mock_boss_instance_dao)

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.boss_service.boss_instance_dao, self.mock_boss_instance_dao)
        self.assertIsInstance(self.boss_service.boss_time_remaining, dict)
        self.assertEqual(len(self.boss_service.boss_time_remaining), 0)

    @patch('cordia.service.boss_service.logger')
    async def test_get_boss_by_discord_id_found(self, mock_logger):
        """Test getting a boss that exists."""
        discord_id = 123456789
        mock_boss = Mock(spec=BossInstance)
        mock_boss.name = "test_boss"
        mock_boss.current_hp = 100
        self.mock_boss_instance_dao.get_boss_by_discord_id.return_value = mock_boss

        result = await self.boss_service.get_boss_by_discord_id(discord_id)

        self.mock_boss_instance_dao.get_boss_by_discord_id.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_boss)
        mock_logger.debug.assert_called()

    @patch('cordia.service.boss_service.logger')
    async def test_get_boss_by_discord_id_not_found(self, mock_logger):
        """Test getting a boss that doesn't exist."""
        discord_id = 123456789
        self.mock_boss_instance_dao.get_boss_by_discord_id.return_value = None

        result = await self.boss_service.get_boss_by_discord_id(discord_id)

        self.mock_boss_instance_dao.get_boss_by_discord_id.assert_called_once_with(discord_id)
        self.assertIsNone(result)
        mock_logger.debug.assert_called()

    @patch('cordia.service.boss_service.logger')
    async def test_update_boss_hp(self, mock_logger):
        """Test updating boss HP."""
        discord_id = 123456789
        current_hp = 75

        await self.boss_service.update_boss_hp(discord_id, current_hp)

        self.mock_boss_instance_dao.update_boss_hp.assert_called_once_with(discord_id, current_hp)
        mock_logger.info.assert_called()

    @patch('cordia.service.boss_service.logger')
    @patch('cordia.service.boss_service.boss_data')
    @patch('cordia.service.boss_service.datetime')
    async def test_insert_boss(self, mock_datetime, mock_boss_data, mock_logger):
        """Test inserting a new boss."""
        discord_id = 123456789
        name = "test_boss"
        mock_boss_data_instance = Mock()
        mock_boss_data_instance.hp = 200
        mock_boss_data.__getitem__.return_value = mock_boss_data_instance
        
        mock_now = Mock()
        mock_datetime.now.return_value = mock_now
        mock_expiration = Mock()
        mock_now.__add__.return_value = mock_expiration

        await self.boss_service.insert_boss(discord_id, name)

        self.mock_boss_instance_dao.insert_boss.assert_called_once_with(
            discord_id, mock_boss_data_instance.hp, name, mock_expiration
        )
        self.assertIn(discord_id, self.boss_service.boss_time_remaining)
        self.assertEqual(self.boss_service.boss_time_remaining[discord_id], mock_expiration)
        mock_logger.info.assert_called()

    @patch('cordia.service.boss_service.logger')
    def test_get_boss_time_remaining_found(self, mock_logger):
        """Test getting boss time remaining when boss exists."""
        discord_id = 123456789
        expected_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        self.boss_service.boss_time_remaining[discord_id] = expected_time

        result = self.boss_service.get_boss_time_remaining(discord_id)

        self.assertEqual(result, expected_time)
        mock_logger.debug.assert_called()

    @patch('cordia.service.boss_service.logger')
    def test_get_boss_time_remaining_not_found(self, mock_logger):
        """Test getting boss time remaining when boss doesn't exist."""
        discord_id = 123456789

        result = self.boss_service.get_boss_time_remaining(discord_id)

        self.assertIsNone(result)
        mock_logger.debug.assert_called()

    @patch('cordia.service.boss_service.logger')
    async def test_delete_boss(self, mock_logger):
        """Test deleting a boss."""
        discord_id = 123456789

        await self.boss_service.delete_boss(discord_id)

        self.mock_boss_instance_dao.delete_boss_by_discord_id.assert_called_once_with(discord_id)
        mock_logger.info.assert_called()

    def test_get_boss_stats(self):
        """Test getting boss service statistics."""
        # Add some test data
        self.boss_service.boss_time_remaining[123] = Mock()
        self.boss_service.boss_time_remaining[456] = Mock()

        stats = self.boss_service.get_boss_stats()

        self.assertIn("active_bosses", stats)
        self.assertEqual(stats["active_bosses"], 2)

    def test_boss_time_remaining_storage(self):
        """Test that boss time remaining is stored correctly."""
        discord_id = 123456789
        test_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        
        self.boss_service.boss_time_remaining[discord_id] = test_time
        
        self.assertIn(discord_id, self.boss_service.boss_time_remaining)
        self.assertEqual(self.boss_service.boss_time_remaining[discord_id], test_time)

    def test_multiple_bosses(self):
        """Test handling multiple bosses."""
        user1 = 123456789
        user2 = 987654321
        time1 = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        time2 = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
        
        self.boss_service.boss_time_remaining[user1] = time1
        self.boss_service.boss_time_remaining[user2] = time2
        
        self.assertEqual(len(self.boss_service.boss_time_remaining), 2)
        self.assertEqual(self.boss_service.boss_time_remaining[user1], time1)
        self.assertEqual(self.boss_service.boss_time_remaining[user2], time2)


if __name__ == "__main__":
    unittest.main() 
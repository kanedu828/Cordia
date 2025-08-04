import unittest
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.achievement_service import AchievementService
from cordia.model.achievement_instance import AchievementInstance
from cordia.model.player_stats import PlayerStats


class TestAchievementService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_achievement_dao = Mock()
        self.achievement_service = AchievementService(self.mock_achievement_dao)

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.achievement_service.achievement_dao, self.mock_achievement_dao)

    @patch('cordia.service.achievement_service.logger')
    async def test_get_achievements_by_discord_id(self, mock_logger):
        """Test getting achievements for a user."""
        discord_id = 123456789
        mock_achievements = [Mock(spec=AchievementInstance), Mock(spec=AchievementInstance)]
        self.mock_achievement_dao.get_achievements_by_discord_id.return_value = mock_achievements

        result = await self.achievement_service.get_achievements_by_discord_id(discord_id)

        self.mock_achievement_dao.get_achievements_by_discord_id.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_achievements)
        mock_logger.debug.assert_called()

    @patch('cordia.service.achievement_service.logger')
    async def test_get_achievement_stat_bonuses(self, mock_logger):
        """Test getting achievement stat bonuses."""
        discord_id = 123456789
        
        # Mock achievements with different stat modifiers
        mock_achievement1 = Mock(spec=AchievementInstance)
        mock_achievement1.count = 10
        mock_achievement1.get_achievement_data.return_value = Mock(
            stat_modifier="+",
            monster_killed_increment=5,
            stat_bonus=PlayerStats(strength=5)
        )
        
        mock_achievement2 = Mock(spec=AchievementInstance)
        mock_achievement2.count = 20
        mock_achievement2.get_achievement_data.return_value = Mock(
            stat_modifier="%",
            monster_killed_increment=10,
            stat_bonus=PlayerStats(intelligence=10)
        )
        
        mock_achievements = [mock_achievement1, mock_achievement2]
        self.mock_achievement_dao.get_achievements_by_discord_id.return_value = mock_achievements

        result = await self.achievement_service.get_achievement_stat_bonuses(discord_id)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        additive, percentage = result
        
        self.assertIsInstance(additive, PlayerStats)
        self.assertIsInstance(percentage, PlayerStats)
        mock_logger.debug.assert_called()

    @patch('cordia.service.achievement_service.logger')
    @patch('cordia.service.achievement_service.achievement_data')
    async def test_increment_achievement_valid(self, mock_achievement_data, mock_logger):
        """Test incrementing achievement for valid monster."""
        discord_id = 123456789
        monster = "rat"
        count = 5
        mock_achievement_data.__contains__.return_value = True

        await self.achievement_service.increment_achievement(discord_id, monster, count)

        self.mock_achievement_dao.insert_or_increment_achievement.assert_called_once_with(
            discord_id, monster, count
        )
        mock_logger.info.assert_called()
        mock_logger.debug.assert_called()

    @patch('cordia.service.achievement_service.logger')
    @patch('cordia.service.achievement_service.achievement_data')
    async def test_increment_achievement_invalid_monster(self, mock_achievement_data, mock_logger):
        """Test incrementing achievement for invalid monster."""
        discord_id = 123456789
        monster = "invalid_monster"
        count = 5
        mock_achievement_data.__contains__.return_value = False

        await self.achievement_service.increment_achievement(discord_id, monster, count)

        self.mock_achievement_dao.insert_or_increment_achievement.assert_not_called()
        mock_logger.debug.assert_called()

    @patch('cordia.service.achievement_service.logger')
    async def test_update_achievement_count(self, mock_logger):
        """Test updating achievement count."""
        discord_id = 123456789
        monster = "rat"
        count = 15

        await self.achievement_service.update_achievement_count(discord_id, monster, count)

        self.mock_achievement_dao.update_achievement_count.assert_called_once_with(
            discord_id, monster, count
        )
        mock_logger.info.assert_called()

    @patch('cordia.service.achievement_service.logger')
    async def test_delete_achievement(self, mock_logger):
        """Test deleting achievement."""
        discord_id = 123456789
        monster = "rat"

        await self.achievement_service.delete_achievement(discord_id, monster)

        self.mock_achievement_dao.delete_achievement.assert_called_once_with(discord_id, monster)
        mock_logger.info.assert_called()

    def test_get_achievement_stats(self):
        """Test getting achievement service statistics."""
        with patch('cordia.service.achievement_service.achievement_data') as mock_achievement_data:
            mock_achievement_data.__len__.return_value = 25
            
            stats = self.achievement_service.get_achievement_stats()

            self.assertIn("service_name", stats)
            self.assertIn("total_achievements", stats)
            self.assertEqual(stats["service_name"], "AchievementService")
            self.assertEqual(stats["total_achievements"], 25)

    @patch('cordia.service.achievement_service.logger')
    async def test_get_achievement_stat_bonuses_empty(self, mock_logger):
        """Test getting achievement stat bonuses when no achievements exist."""
        discord_id = 123456789
        self.mock_achievement_dao.get_achievements_by_discord_id.return_value = []

        result = await self.achievement_service.get_achievement_stat_bonuses(discord_id)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        additive, percentage = result
        
        self.assertIsInstance(additive, PlayerStats)
        self.assertIsInstance(percentage, PlayerStats)
        # Both should be empty PlayerStats
        self.assertEqual(additive.strength, 0)
        self.assertEqual(percentage.intelligence, 0)

    @patch('cordia.service.achievement_service.logger')
    async def test_increment_achievement_default_count(self, mock_logger):
        """Test incrementing achievement with default count."""
        discord_id = 123456789
        monster = "rat"
        with patch('cordia.service.achievement_service.achievement_data') as mock_achievement_data:
            mock_achievement_data.__contains__.return_value = True

            await self.achievement_service.increment_achievement(discord_id, monster)

            self.mock_achievement_dao.insert_or_increment_achievement.assert_called_once_with(
                discord_id, monster, 1
            )

    def test_achievement_data_structure(self):
        """Test that achievement data has the expected structure."""
        with patch('cordia.service.achievement_service.achievement_data') as mock_achievement_data:
            # Test that the service can handle achievement data
            mock_achievement_data.__contains__.return_value = True
            mock_achievement_data.__len__.return_value = 10
            
            stats = self.achievement_service.get_achievement_stats()
            self.assertEqual(stats["total_achievements"], 10)


if __name__ == "__main__":
    unittest.main() 
import unittest
import datetime
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.player_service import PlayerService
from cordia.model.player import Player
from cordia.util.errors import NotEnoughGoldError
from cordia.util.constants import MAX_GOLD


class TestPlayerService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_player_dao = Mock()
        self.player_service = PlayerService(self.mock_player_dao)

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.player_service.player_dao, self.mock_player_dao)

    @patch('cordia.service.player_service.logger')
    async def test_get_player_by_discord_id_found(self, mock_logger):
        """Test getting a player that exists."""
        discord_id = 123456789
        mock_player = Mock(spec=Player)
        mock_player.level = 10
        mock_player.exp = 1000
        mock_player.gold = 500
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        result = await self.player_service.get_player_by_discord_id(discord_id)

        self.mock_player_dao.get_by_discord_id.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_player)
        mock_logger.debug.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_get_player_by_discord_id_not_found(self, mock_logger):
        """Test getting a player that doesn't exist."""
        discord_id = 123456789
        self.mock_player_dao.get_by_discord_id.return_value = None

        result = await self.player_service.get_player_by_discord_id(discord_id)

        self.mock_player_dao.get_by_discord_id.assert_called_once_with(discord_id)
        self.assertIsNone(result)
        mock_logger.debug.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_insert_player(self, mock_logger):
        """Test inserting a new player."""
        discord_id = 123456789
        mock_player = Mock(spec=Player)
        mock_player.level = 1
        mock_player.exp = 0
        mock_player.gold = 0
        self.mock_player_dao.insert_player.return_value = mock_player

        result = await self.player_service.insert_player(discord_id)

        self.mock_player_dao.insert_player.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_player)
        mock_logger.info.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_get_or_insert_player_existing(self, mock_logger):
        """Test get_or_insert_player when player exists."""
        discord_id = 123456789
        mock_player = Mock(spec=Player)
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        result = await self.player_service.get_or_insert_player(discord_id)

        self.mock_player_dao.get_by_discord_id.assert_called_once_with(discord_id)
        self.mock_player_dao.insert_player.assert_not_called()
        self.assertEqual(result, mock_player)

    @patch('cordia.service.player_service.logger')
    async def test_get_or_insert_player_new(self, mock_logger):
        """Test get_or_insert_player when player doesn't exist."""
        discord_id = 123456789
        mock_player = Mock(spec=Player)
        self.mock_player_dao.get_by_discord_id.return_value = None
        self.mock_player_dao.insert_player.return_value = mock_player

        result = await self.player_service.get_or_insert_player(discord_id)

        self.mock_player_dao.get_by_discord_id.assert_called_once_with(discord_id)
        self.mock_player_dao.insert_player.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_player)

    @patch('cordia.service.player_service.logger')
    @patch('cordia.service.player_service.get_upgrade_points')
    async def test_increment_stat_success(self, mock_get_upgrade_points, mock_logger):
        """Test successfully incrementing a stat."""
        discord_id = 123456789
        stat_name = "strength"
        increment_by = 5
        mock_player = Mock()
        mock_player.__dict__ = {"strength": 10}
        mock_get_upgrade_points.return_value = 10
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        await self.player_service.increment_stat(discord_id, stat_name, increment_by)

        self.mock_player_dao.update_stat.assert_called_once_with(discord_id, stat_name, 15)
        mock_logger.info.assert_called()

    @patch('cordia.service.player_service.logger')
    @patch('cordia.service.player_service.get_upgrade_points')
    async def test_increment_stat_invalid_amount(self, mock_get_upgrade_points, mock_logger):
        """Test incrementing stat with invalid amount."""
        discord_id = 123456789
        stat_name = "strength"
        increment_by = 15
        mock_player = Mock()
        mock_get_upgrade_points.return_value = 10
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        with self.assertRaises(ValueError):
            await self.player_service.increment_stat(discord_id, stat_name, increment_by)

        self.mock_player_dao.update_stat.assert_not_called()

    @patch('cordia.service.player_service.logger')
    async def test_increment_exp(self, mock_logger):
        """Test incrementing experience."""
        discord_id = 123456789
        increment_by = 100
        mock_player = Mock()
        mock_player.exp = 500
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        await self.player_service.increment_exp(discord_id, increment_by)

        self.mock_player_dao.update_exp.assert_called_once_with(discord_id, 600)
        mock_logger.info.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_increment_gold_success(self, mock_logger):
        """Test successfully incrementing gold."""
        discord_id = 123456789
        increment_by = 100
        mock_player = Mock()
        mock_player.gold = 500
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        await self.player_service.increment_gold(discord_id, increment_by)

        self.mock_player_dao.update_gold.assert_called_once_with(discord_id, 600)
        mock_logger.info.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_increment_gold_negative(self, mock_logger):
        """Test incrementing gold that would result in negative value."""
        discord_id = 123456789
        increment_by = -600
        mock_player = Mock()
        mock_player.gold = 500
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        with self.assertRaises(NotEnoughGoldError):
            await self.player_service.increment_gold(discord_id, increment_by)

        self.mock_player_dao.update_gold.assert_not_called()
        mock_logger.error.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_increment_gold_exceeds_max(self, mock_logger):
        """Test incrementing gold that would exceed max limit."""
        discord_id = 123456789
        increment_by = 100
        mock_player = Mock()
        mock_player.gold = MAX_GOLD
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        await self.player_service.increment_gold(discord_id, increment_by)

        self.mock_player_dao.update_gold.assert_not_called()
        mock_logger.warning.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_increment_rebirth_points(self, mock_logger):
        """Test incrementing rebirth points."""
        discord_id = 123456789
        increment_by = 5
        mock_player = Mock()
        mock_player.rebirth_points = 10
        self.mock_player_dao.get_by_discord_id.return_value = mock_player

        await self.player_service.increment_rebirth_points(discord_id, increment_by)

        self.mock_player_dao.update_rebirth_points.assert_called_once_with(discord_id, 15)
        mock_logger.info.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_update_location_success(self, mock_logger):
        """Test successfully updating location."""
        discord_id = 123456789
        location = "forest"
        with patch('cordia.service.player_service.location_data', {"forest": Mock()}):
            await self.player_service.update_location(discord_id, location)

        self.mock_player_dao.update_location.assert_called_once_with(discord_id, location)
        mock_logger.info.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_update_location_invalid(self, mock_logger):
        """Test updating location with invalid location."""
        discord_id = 123456789
        location = "invalid_location"
        with patch('cordia.service.player_service.location_data', {"forest": Mock()}):
            with self.assertRaises(ValueError):
                await self.player_service.update_location(discord_id, location)

        self.mock_player_dao.update_location.assert_not_called()
        mock_logger.error.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_count_players_in_location(self, mock_logger):
        """Test counting players in location."""
        location = "forest"
        expected_count = 5
        self.mock_player_dao.count_players_in_location.return_value = expected_count

        result = await self.player_service.count_players_in_location(location)

        self.mock_player_dao.count_players_in_location.assert_called_once_with(location)
        self.assertEqual(result, expected_count)
        mock_logger.debug.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_update_last_boss_killed(self, mock_logger):
        """Test updating last boss killed timestamp."""
        discord_id = 123456789
        with patch('datetime.datetime') as mock_datetime:
            mock_now = Mock()
            mock_datetime.now.return_value = mock_now

            await self.player_service.update_last_boss_killed(discord_id)

        self.mock_player_dao.update_last_boss_killed.assert_called_once_with(discord_id, mock_now)
        mock_logger.info.assert_called()

    @patch('cordia.service.player_service.logger')
    async def test_rebirth_player(self, mock_logger):
        """Test rebirthing a player."""
        discord_id = 123456789

        await self.player_service.rebirth_player(discord_id)

        self.mock_player_dao.reset_player_stats.assert_called_once_with(discord_id)
        mock_logger.info.assert_called()

    def test_get_player_stats(self):
        """Test getting player service statistics."""
        stats = self.player_service.get_player_stats()

        self.assertIn("service_name", stats)
        self.assertIn("max_gold_limit", stats)
        self.assertEqual(stats["service_name"], "PlayerService")
        self.assertEqual(stats["max_gold_limit"], MAX_GOLD)


if __name__ == "__main__":
    unittest.main() 
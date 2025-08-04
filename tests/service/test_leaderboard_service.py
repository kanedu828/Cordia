import unittest
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.leaderboard_service import LeaderboardService
from cordia.model.player import Player
from cordia.model.daily_leaderboard import DailyLeaderboard


class TestLeaderboardService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_player_dao = Mock()
        self.mock_daily_leaderboard_dao = Mock()
        self.mock_bot = Mock()
        self.leaderboard_service = LeaderboardService(
            self.mock_player_dao,
            self.mock_daily_leaderboard_dao,
            self.mock_bot
        )

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.leaderboard_service.player_dao, self.mock_player_dao)
        self.assertEqual(self.leaderboard_service.daily_leaderboard_dao, self.mock_daily_leaderboard_dao)
        self.assertEqual(self.leaderboard_service.bot, self.mock_bot)
        self.assertIsInstance(self.leaderboard_service.leaderboard_user_cache, dict)
        self.assertEqual(len(self.leaderboard_service.leaderboard_user_cache), 0)

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_top_100_players_by_column(self, mock_logger):
        """Test getting top 100 players by column."""
        column = "exp"
        mock_players = [Mock(spec=Player), Mock(spec=Player)]
        self.mock_player_dao.get_top_100_players_by_column.return_value = mock_players

        result = await self.leaderboard_service.get_top_100_players_by_column(column)

        self.mock_player_dao.get_top_100_players_by_column.assert_called_once_with(column)
        self.assertEqual(result, mock_players)
        mock_logger.debug.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_player_rank_by_column(self, mock_logger):
        """Test getting player rank by column."""
        discord_id = 123456789
        column = "exp"
        expected_rank = 5
        self.mock_player_dao.get_player_rank_by_column.return_value = expected_rank

        result = await self.leaderboard_service.get_player_rank_by_column(discord_id, column)

        self.mock_player_dao.get_player_rank_by_column.assert_called_once_with(discord_id, column)
        self.assertEqual(result, expected_rank)
        mock_logger.debug.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_leaderboard_user_cached(self, mock_logger):
        """Test getting leaderboard user from cache."""
        discord_id = 123456789
        expected_username = "TestUser"
        self.leaderboard_service.leaderboard_user_cache[discord_id] = expected_username

        result = await self.leaderboard_service.get_leaderboard_user(discord_id)

        self.assertEqual(result, expected_username)
        mock_logger.debug.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_leaderboard_user_fetch_success(self, mock_logger):
        """Test getting leaderboard user by fetching from Discord."""
        discord_id = 123456789
        expected_username = "TestUser"
        mock_user = Mock()
        mock_user.name = expected_username
        self.mock_bot.fetch_user.return_value = mock_user

        result = await self.leaderboard_service.get_leaderboard_user(discord_id)

        self.mock_bot.fetch_user.assert_called_once_with(discord_id)
        self.assertEqual(result, expected_username)
        self.assertEqual(self.leaderboard_service.leaderboard_user_cache[discord_id], expected_username)
        mock_logger.debug.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_leaderboard_user_fetch_failure(self, mock_logger):
        """Test getting leaderboard user when Discord fetch fails."""
        discord_id = 123456789
        self.mock_bot.fetch_user.side_effect = Exception("User not found")

        result = await self.leaderboard_service.get_leaderboard_user(discord_id)

        self.mock_bot.fetch_user.assert_called_once_with(discord_id)
        self.assertEqual(result, f"User_{discord_id}")
        self.assertNotIn(discord_id, self.leaderboard_service.leaderboard_user_cache)
        mock_logger.error.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_upsert_daily_leaderboard(self, mock_logger):
        """Test upserting daily leaderboard."""
        discord_id = 123456789
        exp = 1000
        gold = 500
        monsters_killed = 25

        await self.leaderboard_service.upsert_daily_leaderboard(discord_id, exp, gold, monsters_killed)

        self.mock_daily_leaderboard_dao.upsert_daily_leaderboard.assert_called_once_with(
            discord_id, exp, gold, monsters_killed
        )
        mock_logger.info.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_top_100_daily_players_by_column(self, mock_logger):
        """Test getting top 100 daily players by column."""
        column = "exp"
        mock_players = [Mock(spec=DailyLeaderboard), Mock(spec=DailyLeaderboard)]
        self.mock_daily_leaderboard_dao.get_top_100_daily_players_by_column.return_value = mock_players

        result = await self.leaderboard_service.get_top_100_daily_players_by_column(column)

        self.mock_daily_leaderboard_dao.get_top_100_daily_players_by_column.assert_called_once_with(column)
        self.assertEqual(result, mock_players)
        mock_logger.debug.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_player_daily_rank_by_column(self, mock_logger):
        """Test getting player daily rank by column."""
        discord_id = 123456789
        column = "exp"
        expected_rank = 10
        self.mock_daily_leaderboard_dao.get_player_daily_rank_by_column.return_value = expected_rank

        result = await self.leaderboard_service.get_player_daily_rank_by_column(discord_id, column)

        self.mock_daily_leaderboard_dao.get_player_daily_rank_by_column.assert_called_once_with(discord_id, column)
        self.assertEqual(result, expected_rank)
        mock_logger.debug.assert_called()

    @patch('cordia.service.leaderboard_service.logger')
    async def test_award_trophies_to_top_players(self, mock_logger):
        """Test awarding trophies to top players."""
        # Mock top players for each category
        mock_player1 = Mock()
        mock_player1.discord_id = 123456789
        mock_player2 = Mock()
        mock_player2.discord_id = 987654321
        mock_player3 = Mock()
        mock_player3.discord_id = 555666777
        
        self.mock_daily_leaderboard_dao.get_top_100_daily_players_by_column.return_value = [
            mock_player1, mock_player2, mock_player3
        ]

        await self.leaderboard_service.award_trophies_to_top_players()

        # Should call increment_trophies for top 3 players in each category
        expected_calls = [
            ((123456789,),),
            ((987654321,),),
            ((555666777,),),
            ((123456789,),),
            ((987654321,),),
            ((555666777,),),
            ((123456789,),),
            ((987654321,),),
            ((555666777,),),
        ]
        
        self.mock_player_dao.increment_trophies.assert_has_calls(expected_calls)
        self.assertEqual(self.mock_player_dao.increment_trophies.call_count, 9)  # 3 categories * 3 players
        mock_logger.info.assert_called()

    def test_get_leaderboard_stats(self):
        """Test getting leaderboard service statistics."""
        # Add some test data to cache
        self.leaderboard_service.leaderboard_user_cache[123] = "User1"
        self.leaderboard_service.leaderboard_user_cache[456] = "User2"

        stats = self.leaderboard_service.get_leaderboard_stats()

        self.assertIn("cached_users", stats)
        self.assertIn("max_cache_size", stats)
        self.assertEqual(stats["cached_users"], 2)
        self.assertEqual(stats["max_cache_size"], 1000)

    def test_cache_management(self):
        """Test that the cache works correctly."""
        discord_id = 123456789
        username = "TestUser"
        
        # Test adding to cache
        self.leaderboard_service.leaderboard_user_cache[discord_id] = username
        self.assertIn(discord_id, self.leaderboard_service.leaderboard_user_cache)
        self.assertEqual(self.leaderboard_service.leaderboard_user_cache[discord_id], username)
        
        # Test cache size
        self.assertEqual(len(self.leaderboard_service.leaderboard_user_cache), 1)

    @patch('cordia.service.leaderboard_service.logger')
    async def test_get_leaderboard_user_cache_limit(self, mock_logger):
        """Test that cache doesn't grow beyond limit."""
        # Fill cache to limit
        for i in range(1001):
            self.leaderboard_service.leaderboard_user_cache[i] = f"User{i}"
        
        # Try to add another user
        discord_id = 999999
        mock_user = Mock()
        mock_user.name = "NewUser"
        self.mock_bot.fetch_user.return_value = mock_user

        result = await self.leaderboard_service.get_leaderboard_user(discord_id)

        # Should still work but not cache the new user
        self.assertEqual(result, "NewUser")
        self.assertNotIn(discord_id, self.leaderboard_service.leaderboard_user_cache)

    def test_scheduler_initialization(self):
        """Test that the scheduler is properly initialized."""
        self.assertIsNotNone(self.leaderboard_service.scheduler)
        self.assertTrue(self.leaderboard_service.scheduler.running)


if __name__ == "__main__":
    unittest.main() 
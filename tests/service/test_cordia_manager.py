import unittest
from unittest.mock import Mock, patch
from cordia.service.cordia_service import CordiaManager


class TestCordiaManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_bot = Mock()
        self.mock_player_service = Mock()
        self.mock_gear_service = Mock()
        self.mock_boss_service = Mock()
        self.mock_battle_service = Mock()
        self.mock_item_service = Mock()
        self.mock_leaderboard_service = Mock()
        self.mock_achievement_service = Mock()
        self.mock_market_service = Mock()
        self.mock_vote_service = Mock()
        
        self.cordia_manager = CordiaManager(
            self.mock_bot,
            self.mock_player_service,
            self.mock_gear_service,
            self.mock_boss_service,
            self.mock_battle_service,
            self.mock_item_service,
            self.mock_leaderboard_service,
            self.mock_achievement_service,
            self.mock_market_service,
            self.mock_vote_service,
        )

    def test_initialization(self):
        """Test that the manager initializes correctly."""
        self.assertEqual(self.cordia_manager.bot, self.mock_bot)
        self.assertEqual(self.cordia_manager.player_service, self.mock_player_service)
        self.assertEqual(self.cordia_manager.gear_service, self.mock_gear_service)
        self.assertEqual(self.cordia_manager.boss_service, self.mock_boss_service)
        self.assertEqual(self.cordia_manager.battle_service, self.mock_battle_service)
        self.assertEqual(self.cordia_manager.item_service, self.mock_item_service)
        self.assertEqual(self.cordia_manager.leaderboard_service, self.mock_leaderboard_service)
        self.assertEqual(self.cordia_manager.achievement_service, self.mock_achievement_service)
        self.assertEqual(self.cordia_manager.market_service, self.mock_market_service)
        self.assertEqual(self.cordia_manager.vote_service, self.mock_vote_service)

    def test_all_services_present(self):
        """Test that all expected services are present."""
        expected_services = [
            "player_service",
            "gear_service",
            "boss_service", 
            "battle_service",
            "item_service",
            "leaderboard_service",
            "achievement_service",
            "market_service",
            "vote_service"
        ]
        
        for service_name in expected_services:
            self.assertTrue(hasattr(self.cordia_manager, service_name))

    @patch('cordia.service.cordia_service.logger')
    def test_get_manager_stats(self, mock_logger):
        """Test getting manager statistics."""
        stats = self.cordia_manager.get_manager_stats()

        self.assertIn("service_name", stats)
        self.assertIn("services", stats)
        self.assertEqual(stats["service_name"], "CordiaManager")
        self.assertIsInstance(stats["services"], list)
        self.assertEqual(len(stats["services"]), 9)
        mock_logger.debug.assert_called()

    def test_services_list_completeness(self):
        """Test that the services list in stats is complete."""
        stats = self.cordia_manager.get_manager_stats()
        services_list = stats["services"]
        
        expected_services = [
            "player_service",
            "gear_service", 
            "boss_service",
            "battle_service",
            "item_service",
            "leaderboard_service",
            "achievement_service",
            "market_service",
            "vote_service"
        ]
        
        for service in expected_services:
            self.assertIn(service, services_list)

    def test_service_accessibility(self):
        """Test that all services are accessible through the manager."""
        services = [
            self.cordia_manager.player_service,
            self.cordia_manager.gear_service,
            self.cordia_manager.boss_service,
            self.cordia_manager.battle_service,
            self.cordia_manager.item_service,
            self.cordia_manager.leaderboard_service,
            self.cordia_manager.achievement_service,
            self.cordia_manager.market_service,
            self.cordia_manager.vote_service,
        ]
        
        for service in services:
            self.assertIsNotNone(service)
            self.assertIsInstance(service, Mock)


if __name__ == "__main__":
    unittest.main() 
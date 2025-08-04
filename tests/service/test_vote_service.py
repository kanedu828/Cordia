import unittest
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.vote_service import VoteService


class TestVoteService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_item_service = Mock()
        self.vote_service = VoteService(self.mock_item_service)

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.vote_service.item_service, self.mock_item_service)

    @patch('cordia.service.vote_service.logger')
    @patch('cordia.service.vote_service.random')
    async def test_give_vote_reward(self, mock_random, mock_logger):
        """Test giving a vote reward."""
        discord_id = 123456789
        mock_random.choice.return_value = ("basic_core", [2, 5])
        mock_random.randint.return_value = 3

        result = await self.vote_service.give_vote_reward(discord_id)

        self.mock_item_service.insert_item.assert_called_once_with(discord_id, "basic_core", 3)
        self.assertEqual(result, ("basic_core", 3))
        mock_logger.info.assert_called()

    @patch('cordia.service.vote_service.logger')
    @patch('cordia.service.vote_service.random')
    async def test_give_vote_reward_different_reward(self, mock_random, mock_logger):
        """Test giving a different vote reward."""
        discord_id = 123456789
        mock_random.choice.return_value = ("supreme_core", [1, 2])
        mock_random.randint.return_value = 2

        result = await self.vote_service.give_vote_reward(discord_id)

        self.mock_item_service.insert_item.assert_called_once_with(discord_id, "supreme_core", 2)
        self.assertEqual(result, ("supreme_core", 2))
        mock_logger.info.assert_called()

    @patch('cordia.service.vote_service.logger')
    @patch('cordia.service.vote_service.random')
    async def test_give_vote_reward_chaos_core(self, mock_random, mock_logger):
        """Test giving chaos core as vote reward."""
        discord_id = 123456789
        mock_random.choice.return_value = ("chaos_core", [1, 1])
        mock_random.randint.return_value = 1

        result = await self.vote_service.give_vote_reward(discord_id)

        self.mock_item_service.insert_item.assert_called_once_with(discord_id, "chaos_core", 1)
        self.assertEqual(result, ("chaos_core", 1))
        mock_logger.info.assert_called()

    def test_rewards_structure(self):
        """Test that rewards have the expected structure."""
        rewards = self.vote_service.give_vote_reward.__wrapped__.__defaults__[0]
        
        for reward in rewards:
            self.assertIsInstance(reward, tuple)
            self.assertEqual(len(reward), 2)
            self.assertIsInstance(reward[0], str)
            self.assertIsInstance(reward[1], list)
            self.assertEqual(len(reward[1]), 2)
            self.assertIsInstance(reward[1][0], int)
            self.assertIsInstance(reward[1][1], int)
            self.assertLessEqual(reward[1][0], reward[1][1])

    def test_get_vote_stats(self):
        """Test getting vote service statistics."""
        stats = self.vote_service.get_vote_stats()

        self.assertIn("service_name", stats)
        self.assertEqual(stats["service_name"], "VoteService")


if __name__ == "__main__":
    unittest.main() 
import unittest
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.loot_service import LootService
from cordia.model.monster import Monster
from cordia.model.player_stats import PlayerStats
from cordia.model.gear_instance import GearInstance
from cordia.model.item import Item


class TestLootService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_gear_service = Mock()
        self.mock_player_service = Mock()
        self.mock_item_service = Mock()
        self.loot_service = LootService(
            self.mock_gear_service,
            self.mock_player_service,
            self.mock_item_service
        )

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.loot_service.gear_service, self.mock_gear_service)
        self.assertEqual(self.loot_service.player_service, self.mock_player_service)
        self.assertEqual(self.loot_service.item_service, self.mock_item_service)

    @patch('cordia.service.loot_service.logger')
    @patch('cordia.service.loot_service.random_within_range')
    @patch('cordia.service.loot_service.get_diminished_stat')
    async def test_handle_loot_success(self, mock_get_diminished_stat, mock_random_within_range, mock_logger):
        """Test handling loot successfully."""
        discord_id = 123456789
        mock_monster = Mock(spec=Monster)
        mock_monster.name = "rat"
        mock_monster.exp = 10
        mock_monster.gold = 5
        mock_monster.get_dropped_gear.return_value = ["basic_sword"]
        mock_monster.get_dropped_items.return_value = [("basic_core", 2)]
        
        mock_player_stats = Mock(spec=PlayerStats)
        mock_player_stats.efficiency = 10
        mock_player_stats.luck = 5
        kills = 3
        
        mock_get_diminished_stat.side_effect = [2, 1]  # For exp and gold
        mock_random_within_range.side_effect = [35, 18]  # exp_gained, gold_gained
        
        # Mock gear data
        mock_gear_data = Mock()
        mock_gear_data.gold_value = 10
        with patch('cordia.service.loot_service.gear_data') as mock_gear_data_dict:
            mock_gear_data_dict.__getitem__.return_value = mock_gear_data
            
            # Mock item data
            mock_item_data = Mock()
            with patch('cordia.service.loot_service.item_data') as mock_item_data_dict:
                mock_item_data_dict.__getitem__.return_value = mock_item_data
                
                result = await self.loot_service.handle_loot(discord_id, mock_monster, mock_player_stats, kills)

        exp_gained, gold_gained, new_gear_loot, sold_gear_amount, item_drops = result
        
        self.assertEqual(exp_gained, 35)
        self.assertEqual(gold_gained, 18)
        self.assertEqual(len(new_gear_loot), 1)
        self.assertEqual(sold_gear_amount, 0)
        self.assertEqual(len(item_drops), 1)
        
        # Verify service calls
        self.mock_player_service.increment_exp.assert_called_once_with(discord_id, 35)
        self.mock_player_service.increment_gold.assert_called_once_with(discord_id, 18)
        self.mock_gear_service.insert_gear.assert_called_once_with(discord_id, "basic_sword")
        self.mock_item_service.insert_item.assert_called_once_with(discord_id, "basic_core", 2)
        
        mock_logger.info.assert_called()

    @patch('cordia.service.loot_service.logger')
    @patch('cordia.service.loot_service.random_within_range')
    @patch('cordia.service.loot_service.get_diminished_stat')
    async def test_handle_loot_gear_insertion_failure(self, mock_get_diminished_stat, mock_random_within_range, mock_logger):
        """Test handling loot when gear insertion fails."""
        discord_id = 123456789
        mock_monster = Mock(spec=Monster)
        mock_monster.name = "rat"
        mock_monster.exp = 10
        mock_monster.gold = 5
        mock_monster.get_dropped_gear.return_value = ["basic_sword"]
        mock_monster.get_dropped_items.return_value = []
        
        mock_player_stats = Mock(spec=PlayerStats)
        mock_player_stats.efficiency = 10
        mock_player_stats.luck = 5
        kills = 1
        
        mock_get_diminished_stat.side_effect = [2, 1]
        mock_random_within_range.side_effect = [12, 6]
        
        # Mock gear data
        mock_gear_data = Mock()
        mock_gear_data.gold_value = 10
        with patch('cordia.service.loot_service.gear_data') as mock_gear_data_dict:
            mock_gear_data_dict.__getitem__.return_value = mock_gear_data
            
            # Make gear insertion fail
            self.mock_gear_service.insert_gear.side_effect = Exception("Database error")
            
            result = await self.loot_service.handle_loot(discord_id, mock_monster, mock_player_stats, kills)

        exp_gained, gold_gained, new_gear_loot, sold_gear_amount, item_drops = result
        
        self.assertEqual(exp_gained, 12)
        self.assertEqual(gold_gained, 6)
        self.assertEqual(len(new_gear_loot), 0)
        self.assertEqual(sold_gear_amount, 10)  # Gear was sold instead
        self.assertEqual(len(item_drops), 0)
        
        # Verify service calls
        self.mock_player_service.increment_exp.assert_called_once_with(discord_id, 12)
        self.mock_player_service.increment_gold.assert_called_once_with(discord_id, 16)  # 6 + 10 from sold gear
        mock_logger.debug.assert_called()

    @patch('cordia.service.loot_service.logger')
    @patch('cordia.service.loot_service.random_within_range')
    @patch('cordia.service.loot_service.get_diminished_stat')
    async def test_handle_loot_no_drops(self, mock_get_diminished_stat, mock_random_within_range, mock_logger):
        """Test handling loot when no drops occur."""
        discord_id = 123456789
        mock_monster = Mock(spec=Monster)
        mock_monster.name = "rat"
        mock_monster.exp = 10
        mock_monster.gold = 5
        mock_monster.get_dropped_gear.return_value = []
        mock_monster.get_dropped_items.return_value = []
        
        mock_player_stats = Mock(spec=PlayerStats)
        mock_player_stats.efficiency = 10
        mock_player_stats.luck = 5
        kills = 1
        
        mock_get_diminished_stat.side_effect = [2, 1]
        mock_random_within_range.side_effect = [12, 6]
        
        result = await self.loot_service.handle_loot(discord_id, mock_monster, mock_player_stats, kills)

        exp_gained, gold_gained, new_gear_loot, sold_gear_amount, item_drops = result
        
        self.assertEqual(exp_gained, 12)
        self.assertEqual(gold_gained, 6)
        self.assertEqual(len(new_gear_loot), 0)
        self.assertEqual(sold_gear_amount, 0)
        self.assertEqual(len(item_drops), 0)
        
        # Verify service calls
        self.mock_player_service.increment_exp.assert_called_once_with(discord_id, 12)
        self.mock_player_service.increment_gold.assert_called_once_with(discord_id, 6)
        self.mock_gear_service.insert_gear.assert_not_called()
        self.mock_item_service.insert_item.assert_not_called()

    @patch('cordia.service.loot_service.logger')
    @patch('cordia.service.loot_service.random_within_range')
    @patch('cordia.service.loot_service.get_diminished_stat')
    async def test_handle_loot_multiple_items(self, mock_get_diminished_stat, mock_random_within_range, mock_logger):
        """Test handling loot with multiple items."""
        discord_id = 123456789
        mock_monster = Mock(spec=Monster)
        mock_monster.name = "rat"
        mock_monster.exp = 10
        mock_monster.gold = 5
        mock_monster.get_dropped_gear.return_value = []
        mock_monster.get_dropped_items.return_value = [("basic_core", 2), ("quality_core", 1)]
        
        mock_player_stats = Mock(spec=PlayerStats)
        mock_player_stats.efficiency = 10
        mock_player_stats.luck = 5
        kills = 1
        
        mock_get_diminished_stat.side_effect = [2, 1]
        mock_random_within_range.side_effect = [12, 6]
        
        # Mock item data
        mock_item_data = Mock()
        with patch('cordia.service.loot_service.item_data') as mock_item_data_dict:
            mock_item_data_dict.__getitem__.return_value = mock_item_data
            
            result = await self.loot_service.handle_loot(discord_id, mock_monster, mock_player_stats, kills)

        exp_gained, gold_gained, new_gear_loot, sold_gear_amount, item_drops = result
        
        self.assertEqual(len(item_drops), 2)
        self.mock_item_service.insert_item.assert_any_call(discord_id, "basic_core", 2)
        self.mock_item_service.insert_item.assert_any_call(discord_id, "quality_core", 1)

    def test_get_loot_stats(self):
        """Test getting loot service statistics."""
        stats = self.loot_service.get_loot_stats()

        self.assertIn("service_name", stats)
        self.assertEqual(stats["service_name"], "LootService")

    @patch('cordia.service.loot_service.logger')
    @patch('cordia.service.loot_service.random_within_range')
    @patch('cordia.service.loot_service.get_diminished_stat')
    async def test_handle_loot_zero_kills(self, mock_get_diminished_stat, mock_random_within_range, mock_logger):
        """Test handling loot with zero kills."""
        discord_id = 123456789
        mock_monster = Mock(spec=Monster)
        mock_monster.name = "rat"
        mock_monster.exp = 10
        mock_monster.gold = 5
        mock_monster.get_dropped_gear.return_value = []
        mock_monster.get_dropped_items.return_value = []
        
        mock_player_stats = Mock(spec=PlayerStats)
        mock_player_stats.efficiency = 10
        mock_player_stats.luck = 5
        kills = 0
        
        mock_get_diminished_stat.side_effect = [0, 0]
        mock_random_within_range.side_effect = [0, 0]
        
        result = await self.loot_service.handle_loot(discord_id, mock_monster, mock_player_stats, kills)

        exp_gained, gold_gained, new_gear_loot, sold_gear_amount, item_drops = result
        
        self.assertEqual(exp_gained, 0)
        self.assertEqual(gold_gained, 0)
        self.assertEqual(len(new_gear_loot), 0)
        self.assertEqual(sold_gear_amount, 0)
        self.assertEqual(len(item_drops), 0)


if __name__ == "__main__":
    unittest.main() 
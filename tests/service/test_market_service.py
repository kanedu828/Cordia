import unittest
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.market_service import MarketService
from cordia.model.market_item import MarketItem
from cordia.model.item_instance import ItemInstance
from cordia.util.errors import InvalidItemError, NotEnoughItemsError, InvalidInputError


class TestMarketService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_market_item_dao = Mock()
        self.mock_item_service = Mock()
        self.mock_player_service = Mock()
        self.market_service = MarketService(
            self.mock_market_item_dao,
            self.mock_item_service,
            self.mock_player_service
        )

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.market_service.market_item_dao, self.mock_market_item_dao)
        self.assertEqual(self.market_service.item_service, self.mock_item_service)
        self.assertEqual(self.market_service.player_service, self.mock_player_service)

    @patch('cordia.service.market_service.logger')
    async def test_get_all_market_items(self, mock_logger):
        """Test getting all market items."""
        mock_items = [Mock(spec=MarketItem), Mock(spec=MarketItem)]
        self.mock_market_item_dao.get_all_market_items.return_value = mock_items

        result = await self.market_service.get_all_market_items()

        self.mock_market_item_dao.get_all_market_items.assert_called_once()
        self.assertEqual(result, mock_items)
        mock_logger.debug.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_buy_market_item_success(self, mock_logger):
        """Test buying a market item successfully."""
        market_item_id = 1
        discord_id = 123456789
        mock_market_item = Mock(spec=MarketItem)
        mock_market_item.item_name = "basic_core"
        mock_market_item.count = 5
        mock_market_item.price = 100
        mock_market_item.discord_id = 987654321
        self.mock_market_item_dao.get_market_item_by_id.return_value = mock_market_item

        result = await self.market_service.buy_market_item(market_item_id, discord_id)

        self.mock_market_item_dao.get_market_item_by_id.assert_called_once_with(market_item_id)
        self.mock_player_service.increment_gold.assert_any_call(discord_id, -100)
        self.mock_item_service.insert_item.assert_called_once_with(discord_id, "basic_core", 5)
        self.mock_player_service.increment_gold.assert_any_call(987654321, 95)  # 100 - 5% tax
        self.mock_market_item_dao.delete_market_item.assert_called_once_with(market_item_id)
        self.assertEqual(result, mock_market_item)
        mock_logger.info.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_buy_market_item_not_found(self, mock_logger):
        """Test buying a market item that doesn't exist."""
        market_item_id = 999
        discord_id = 123456789
        self.mock_market_item_dao.get_market_item_by_id.return_value = None

        with self.assertRaises(InvalidItemError):
            await self.market_service.buy_market_item(market_item_id, discord_id)

        self.mock_market_item_dao.get_market_item_by_id.assert_called_once_with(market_item_id)
        self.mock_player_service.increment_gold.assert_not_called()
        self.mock_item_service.insert_item.assert_not_called()
        mock_logger.error.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_list_market_item_success(self, mock_logger):
        """Test listing a market item successfully."""
        discord_id = 123456789
        item_name = "basic_core"
        price = 50
        count = 3
        
        mock_item = Mock(spec=ItemInstance)
        mock_item.count = 5
        self.mock_item_service.get_item.return_value = mock_item
        
        mock_market_item = Mock(spec=MarketItem)
        self.mock_market_item_dao.insert_market_item.return_value = mock_market_item

        result = await self.market_service.list_market_item(discord_id, item_name, price, count)

        self.mock_item_service.get_item.assert_called_once_with(discord_id, item_name)
        self.mock_item_service.insert_item.assert_called_once_with(discord_id, item_name, -3)
        self.mock_market_item_dao.insert_market_item.assert_called_once_with(discord_id, item_name, price, count)
        self.assertEqual(result, mock_market_item)
        mock_logger.info.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_list_market_item_invalid_count(self, mock_logger):
        """Test listing a market item with invalid count."""
        discord_id = 123456789
        item_name = "basic_core"
        price = 50
        count = 0

        with self.assertRaises(InvalidItemError):
            await self.market_service.list_market_item(discord_id, item_name, price, count)

        self.mock_item_service.get_item.assert_not_called()
        self.mock_market_item_dao.insert_market_item.assert_not_called()
        mock_logger.error.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_list_market_item_item_not_found(self, mock_logger):
        """Test listing a market item when item doesn't exist in inventory."""
        discord_id = 123456789
        item_name = "basic_core"
        price = 50
        count = 3
        
        self.mock_item_service.get_item.return_value = None

        with self.assertRaises(NotEnoughItemsError):
            await self.market_service.list_market_item(discord_id, item_name, price, count)

        self.mock_item_service.get_item.assert_called_once_with(discord_id, item_name)
        self.mock_market_item_dao.insert_market_item.assert_not_called()
        mock_logger.error.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_list_market_item_invalid_price(self, mock_logger):
        """Test listing a market item with invalid price."""
        discord_id = 123456789
        item_name = "basic_core"
        price = -10
        count = 3
        
        mock_item = Mock(spec=ItemInstance)
        self.mock_item_service.get_item.return_value = mock_item

        with self.assertRaises(InvalidInputError):
            await self.market_service.list_market_item(discord_id, item_name, price, count)

        self.mock_item_service.get_item.assert_called_once_with(discord_id, item_name)
        self.mock_market_item_dao.insert_market_item.assert_not_called()
        mock_logger.error.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_unlist_market_item(self, mock_logger):
        """Test unlisting a market item."""
        market_item_id = 1
        mock_market_item = Mock(spec=MarketItem)
        mock_market_item.discord_id = 123456789
        mock_market_item.item_name = "basic_core"
        mock_market_item.count = 3
        self.mock_market_item_dao.get_market_item_by_id.return_value = mock_market_item

        await self.market_service.unlist_market_item(market_item_id)

        self.mock_market_item_dao.get_market_item_by_id.assert_called_once_with(market_item_id)
        self.mock_item_service.insert_item.assert_called_once_with(123456789, "basic_core", 3)
        self.mock_market_item_dao.delete_market_item.assert_called_once_with(market_item_id)
        mock_logger.info.assert_called()

    @patch('cordia.service.market_service.logger')
    async def test_find_items_by_name(self, mock_logger):
        """Test finding items by name."""
        item_name = "basic_core"
        mock_items = [Mock(spec=MarketItem), Mock(spec=MarketItem)]
        self.mock_market_item_dao.get_market_items_by_name.return_value = mock_items

        result = await self.market_service.find_items_by_name(item_name)

        self.mock_market_item_dao.get_market_items_by_name.assert_called_once_with(item_name)
        self.assertEqual(result, mock_items)
        mock_logger.debug.assert_called()

    def test_get_market_stats(self):
        """Test getting market service statistics."""
        stats = self.market_service.get_market_stats()

        self.assertIn("service_name", stats)
        self.assertEqual(stats["service_name"], "MarketService")

    @patch('cordia.service.market_service.logger')
    async def test_buy_market_item_tax_calculation(self, mock_logger):
        """Test that tax is calculated correctly when buying market items."""
        market_item_id = 1
        discord_id = 123456789
        mock_market_item = Mock(spec=MarketItem)
        mock_market_item.item_name = "basic_core"
        mock_market_item.count = 1
        mock_market_item.price = 100
        mock_market_item.discord_id = 987654321
        self.mock_market_item_dao.get_market_item_by_id.return_value = mock_market_item

        await self.market_service.buy_market_item(market_item_id, discord_id)

        # Tax should be 5% of 100 = 5, so seller gets 95
        self.mock_player_service.increment_gold.assert_any_call(987654321, 95)

    @patch('cordia.service.market_service.logger')
    async def test_list_market_item_insufficient_quantity(self, mock_logger):
        """Test listing a market item when player doesn't have enough."""
        discord_id = 123456789
        item_name = "basic_core"
        price = 50
        count = 10
        
        mock_item = Mock(spec=ItemInstance)
        mock_item.count = 5  # Player only has 5, trying to list 10
        self.mock_item_service.get_item.return_value = mock_item

        with self.assertRaises(NotEnoughItemsError):
            await self.market_service.list_market_item(discord_id, item_name, price, count)

        self.mock_item_service.get_item.assert_called_once_with(discord_id, item_name)
        self.mock_market_item_dao.insert_market_item.assert_not_called()


if __name__ == "__main__":
    unittest.main() 
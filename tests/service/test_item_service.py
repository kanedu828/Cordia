import unittest
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.item_service import ItemService
from cordia.model.item_instance import ItemInstance
from cordia.util.errors import NotEnoughItemsError


class TestItemService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_item_dao = Mock()
        self.item_service = ItemService(self.mock_item_dao)

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.item_service.item_dao, self.mock_item_dao)

    @patch('cordia.service.item_service.logger')
    async def test_insert_item_new_item(self, mock_logger):
        """Test inserting a new item."""
        discord_id = 123456789
        name = "basic_core"
        count = 5
        mock_item = None
        mock_inserted_item = Mock(spec=ItemInstance)
        mock_inserted_item.count = 5
        self.mock_item_dao.get_item.return_value = mock_item
        self.mock_item_dao.insert_item.return_value = mock_inserted_item

        await self.item_service.insert_item(discord_id, name, count)

        self.mock_item_dao.get_item.assert_called_once_with(discord_id, name)
        self.mock_item_dao.insert_item.assert_called_once_with(discord_id, name, count)
        self.mock_item_dao.delete_item.assert_not_called()
        mock_logger.info.assert_called()

    @patch('cordia.service.item_service.logger')
    async def test_insert_item_existing_item(self, mock_logger):
        """Test inserting an item when it already exists."""
        discord_id = 123456789
        name = "basic_core"
        count = 5
        mock_item = Mock(spec=ItemInstance)
        mock_item.count = 10
        mock_inserted_item = Mock(spec=ItemInstance)
        mock_inserted_item.count = 15
        self.mock_item_dao.get_item.return_value = mock_item
        self.mock_item_dao.insert_item.return_value = mock_inserted_item

        await self.item_service.insert_item(discord_id, name, count)

        self.mock_item_dao.get_item.assert_called_once_with(discord_id, name)
        self.mock_item_dao.insert_item.assert_called_once_with(discord_id, name, count)
        self.mock_item_dao.delete_item.assert_not_called()
        mock_logger.info.assert_called()

    @patch('cordia.service.item_service.logger')
    async def test_insert_item_negative_result(self, mock_logger):
        """Test inserting an item that results in negative count."""
        discord_id = 123456789
        name = "basic_core"
        count = -15
        mock_item = Mock(spec=ItemInstance)
        mock_item.count = 10
        self.mock_item_dao.get_item.return_value = mock_item

        with self.assertRaises(NotEnoughItemsError):
            await self.item_service.insert_item(discord_id, name, count)

        self.mock_item_dao.get_item.assert_called_once_with(discord_id, name)
        self.mock_item_dao.insert_item.assert_not_called()
        mock_logger.error.assert_called()

    @patch('cordia.service.item_service.logger')
    async def test_insert_item_zero_count(self, mock_logger):
        """Test inserting an item that results in zero count."""
        discord_id = 123456789
        name = "basic_core"
        count = -10
        mock_item = Mock(spec=ItemInstance)
        mock_item.count = 10
        mock_inserted_item = Mock(spec=ItemInstance)
        mock_inserted_item.count = 0
        self.mock_item_dao.get_item.return_value = mock_item
        self.mock_item_dao.insert_item.return_value = mock_inserted_item

        await self.item_service.insert_item(discord_id, name, count)

        self.mock_item_dao.get_item.assert_called_once_with(discord_id, name)
        self.mock_item_dao.insert_item.assert_called_once_with(discord_id, name, count)
        self.mock_item_dao.delete_item.assert_called_once_with(discord_id, name)
        mock_logger.debug.assert_called()

    @patch('cordia.service.item_service.logger')
    async def test_get_inventory(self, mock_logger):
        """Test getting player inventory."""
        discord_id = 123456789
        mock_inventory = [Mock(spec=ItemInstance), Mock(spec=ItemInstance)]
        self.mock_item_dao.get_all_items_for_user.return_value = mock_inventory

        result = await self.item_service.get_inventory(discord_id)

        self.mock_item_dao.get_all_items_for_user.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_inventory)
        mock_logger.debug.assert_called()

    @patch('cordia.service.item_service.logger')
    async def test_get_item_found(self, mock_logger):
        """Test getting a specific item that exists."""
        discord_id = 123456789
        name = "basic_core"
        mock_item = Mock(spec=ItemInstance)
        mock_item.count = 5
        self.mock_item_dao.get_item.return_value = mock_item

        result = await self.item_service.get_item(discord_id, name)

        self.mock_item_dao.get_item.assert_called_once_with(discord_id, name)
        self.assertEqual(result, mock_item)
        mock_logger.debug.assert_called()

    @patch('cordia.service.item_service.logger')
    async def test_get_item_not_found(self, mock_logger):
        """Test getting a specific item that doesn't exist."""
        discord_id = 123456789
        name = "basic_core"
        self.mock_item_dao.get_item.return_value = None

        result = await self.item_service.get_item(discord_id, name)

        self.mock_item_dao.get_item.assert_called_once_with(discord_id, name)
        self.assertIsNone(result)
        mock_logger.debug.assert_called()

    @patch('cordia.service.item_service.logger')
    async def test_get_cores_for_user(self, mock_logger):
        """Test getting cores for a user."""
        discord_id = 123456789
        mock_cores = [Mock(spec=ItemInstance), Mock(spec=ItemInstance)]
        self.mock_item_dao.get_cores_for_user.return_value = mock_cores

        result = await self.item_service.get_cores_for_user(discord_id)

        self.mock_item_dao.get_cores_for_user.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_cores)
        mock_logger.debug.assert_called()

    def test_get_item_stats(self):
        """Test getting item service statistics."""
        stats = self.item_service.get_item_stats()

        self.assertIn("service_name", stats)
        self.assertEqual(stats["service_name"], "ItemService")


if __name__ == "__main__":
    unittest.main() 
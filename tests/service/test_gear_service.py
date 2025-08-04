import unittest
from unittest.mock import Mock, AsyncMock, patch
from cordia.service.gear_service import GearService
from cordia.model.gear_instance import GearInstance
from cordia.model.gear import GearType


class TestGearService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_gear_dao = Mock()
        self.mock_player_gear_dao = Mock()
        self.gear_service = GearService(self.mock_gear_dao, self.mock_player_gear_dao)

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertEqual(self.gear_service.gear_dao, self.mock_gear_dao)
        self.assertEqual(self.gear_service.player_gear_dao, self.mock_player_gear_dao)

    @patch('cordia.service.gear_service.logger')
    async def test_insert_gear(self, mock_logger):
        """Test inserting gear."""
        discord_id = 123456789
        name = "basic_sword"
        mock_gear = Mock(spec=GearInstance)
        mock_gear.id = 1
        self.mock_gear_dao.insert_gear.return_value = mock_gear

        result = await self.gear_service.insert_gear(discord_id, name)

        self.mock_gear_dao.insert_gear.assert_called_once_with(discord_id, name)
        self.assertEqual(result, mock_gear)
        mock_logger.info.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_get_gear_by_id_found(self, mock_logger):
        """Test getting gear by ID when it exists."""
        gear_id = 1
        mock_gear = Mock(spec=GearInstance)
        mock_gear.name = "basic_sword"
        mock_gear.level = 1
        self.mock_gear_dao.get_gear_by_id.return_value = mock_gear

        result = await self.gear_service.get_gear_by_id(gear_id)

        self.mock_gear_dao.get_gear_by_id.assert_called_once_with(gear_id)
        self.assertEqual(result, mock_gear)
        mock_logger.debug.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_get_gear_by_id_not_found(self, mock_logger):
        """Test getting gear by ID when it doesn't exist."""
        gear_id = 999
        self.mock_gear_dao.get_gear_by_id.return_value = None

        result = await self.gear_service.get_gear_by_id(gear_id)

        self.mock_gear_dao.get_gear_by_id.assert_called_once_with(gear_id)
        self.assertIsNone(result)
        mock_logger.debug.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_get_armory(self, mock_logger):
        """Test getting player armory."""
        discord_id = 123456789
        mock_armory = [Mock(spec=GearInstance), Mock(spec=GearInstance)]
        self.mock_gear_dao.get_gear_by_discord_id.return_value = mock_armory

        result = await self.gear_service.get_armory(discord_id)

        self.mock_gear_dao.get_gear_by_discord_id.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_armory)
        mock_logger.debug.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_increment_gear_stars(self, mock_logger):
        """Test incrementing gear stars."""
        gear_id = 1
        stars = 2
        mock_gear = Mock(spec=GearInstance)
        mock_gear.stars = 3
        self.mock_gear_dao.get_gear_by_id.return_value = mock_gear

        await self.gear_service.increment_gear_stars(gear_id, stars)

        self.mock_gear_dao.get_gear_by_id.assert_called_once_with(gear_id)
        self.mock_gear_dao.update_gear_stars.assert_called_once_with(gear_id, 5)
        mock_logger.info.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_update_gear_bonus(self, mock_logger):
        """Test updating gear bonus."""
        gear_id = 1
        bonus = "strength"

        await self.gear_service.update_gear_bonus(gear_id, bonus)

        self.mock_gear_dao.update_bonus.assert_called_once_with(gear_id, bonus)
        mock_logger.info.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_equip_highest_level_gear(self, mock_logger):
        """Test equipping highest level gear."""
        discord_id = 123456789
        level = 10
        
        # Mock armory with different gear types
        mock_gear1 = Mock(spec=GearInstance)
        mock_gear1.get_gear_data.return_value = Mock(type=GearType.WEAPON, level=5, name="sword")
        mock_gear2 = Mock(spec=GearInstance)
        mock_gear2.get_gear_data.return_value = Mock(type=GearType.TOP, level=8, name="armor")
        mock_gear3 = Mock(spec=GearInstance)
        mock_gear3.get_gear_data.return_value = Mock(type=GearType.WEAPON, level=3, name="dagger")
        
        mock_armory = [mock_gear1, mock_gear2, mock_gear3]
        self.mock_gear_dao.get_gear_by_discord_id.return_value = mock_armory

        result = await self.gear_service.equip_highest_level_gear(discord_id, level)

        # Should equip the highest level gear of each type
        self.assertIn("sword", result)
        self.assertIn("armor", result)
        mock_logger.info.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_get_player_gear(self, mock_logger):
        """Test getting player equipped gear."""
        discord_id = 123456789
        mock_player_gear = [Mock(spec=GearInstance), Mock(spec=GearInstance)]
        self.mock_player_gear_dao.get_player_gear.return_value = mock_player_gear

        result = await self.gear_service.get_player_gear(discord_id)

        self.mock_player_gear_dao.get_player_gear.assert_called_once_with(discord_id)
        self.assertEqual(result, mock_player_gear)
        mock_logger.debug.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_equip_gear(self, mock_logger):
        """Test equipping gear."""
        discord_id = 123456789
        gear_id = 1
        slot = "weapon"

        await self.gear_service.equip_gear(discord_id, gear_id, slot)

        self.mock_player_gear_dao.equip_gear.assert_called_once_with(discord_id, gear_id, slot)
        mock_logger.info.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_remove_all_gear(self, mock_logger):
        """Test removing all gear."""
        discord_id = 123456789

        await self.gear_service.remove_all_gear(discord_id)

        self.mock_player_gear_dao.remove_all_gear.assert_called_once_with(discord_id)
        mock_logger.info.assert_called()

    def test_get_weapon_found(self):
        """Test getting weapon from player gear."""
        mock_weapon = Mock(spec=GearInstance)
        mock_weapon.slot = GearType.WEAPON.value
        mock_weapon.name = "sword"
        mock_player_gear = [mock_weapon, Mock(spec=GearInstance)]

        result = self.gear_service.get_weapon(mock_player_gear)

        self.assertEqual(result, mock_weapon)

    def test_get_weapon_not_found(self):
        """Test getting weapon when no weapon is equipped."""
        mock_player_gear = [Mock(spec=GearInstance), Mock(spec=GearInstance)]

        result = self.gear_service.get_weapon(mock_player_gear)

        self.assertIsNone(result)

    @patch('cordia.service.gear_service.logger')
    async def test_get_player_gear_by_gear_id_found(self, mock_logger):
        """Test getting player gear by gear ID when it exists."""
        gear_id = 1
        mock_player_gear = Mock(spec=GearInstance)
        mock_player_gear.discord_id = 123456789
        self.mock_player_gear_dao.get_by_gear_id.return_value = mock_player_gear

        result = await self.gear_service.get_player_gear_by_gear_id(gear_id)

        self.mock_player_gear_dao.get_by_gear_id.assert_called_once_with(gear_id)
        self.assertEqual(result, mock_player_gear)
        mock_logger.debug.assert_called()

    @patch('cordia.service.gear_service.logger')
    async def test_get_player_gear_by_gear_id_not_found(self, mock_logger):
        """Test getting player gear by gear ID when it doesn't exist."""
        gear_id = 999
        self.mock_player_gear_dao.get_by_gear_id.return_value = None

        result = await self.gear_service.get_player_gear_by_gear_id(gear_id)

        self.mock_player_gear_dao.get_by_gear_id.assert_called_once_with(gear_id)
        self.assertIsNone(result)
        mock_logger.debug.assert_called()

    def test_get_gear_stats(self):
        """Test getting gear service statistics."""
        stats = self.gear_service.get_gear_stats()

        self.assertIn("service_name", stats)
        self.assertEqual(stats["service_name"], "GearService")


if __name__ == "__main__":
    unittest.main() 
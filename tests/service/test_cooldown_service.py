import unittest
import datetime
from unittest.mock import patch
from cordia.service.cooldown_service import CooldownService


class TestCooldownService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.cooldown_service = CooldownService()

    def test_initialization(self):
        """Test that the service initializes correctly."""
        self.assertIsInstance(self.cooldown_service.cooldowns, dict)
        self.assertIn("attack", self.cooldown_service.cooldowns)
        self.assertIn("cast_spell", self.cooldown_service.cooldowns)
        self.assertEqual(len(self.cooldown_service.cooldowns["attack"]), 0)
        self.assertEqual(len(self.cooldown_service.cooldowns["cast_spell"]), 0)

    def test_set_cooldown(self):
        """Test setting a cooldown for a user."""
        discord_id = 123456789
        action = "attack"
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        
        self.cooldown_service.set_cooldown(discord_id, action, expiration_time)
        
        self.assertIn(discord_id, self.cooldown_service.cooldowns[action])
        self.assertEqual(self.cooldown_service.cooldowns[action][discord_id], expiration_time)

    def test_is_on_cooldown_true(self):
        """Test that is_on_cooldown returns True when user is on cooldown."""
        discord_id = 123456789
        action = "attack"
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        
        self.cooldown_service.set_cooldown(discord_id, action, expiration_time)
        
        self.assertTrue(self.cooldown_service.is_on_cooldown(discord_id, action))

    def test_is_on_cooldown_false(self):
        """Test that is_on_cooldown returns False when user is not on cooldown."""
        discord_id = 123456789
        action = "attack"
        
        self.assertFalse(self.cooldown_service.is_on_cooldown(discord_id, action))

    def test_is_on_cooldown_expired(self):
        """Test that is_on_cooldown returns False when cooldown has expired."""
        discord_id = 123456789
        action = "attack"
        expiration_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=5)
        
        self.cooldown_service.set_cooldown(discord_id, action, expiration_time)
        
        self.assertFalse(self.cooldown_service.is_on_cooldown(discord_id, action))

    def test_get_cooldown_expiration(self):
        """Test getting cooldown expiration time."""
        discord_id = 123456789
        action = "attack"
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        
        self.cooldown_service.set_cooldown(discord_id, action, expiration_time)
        
        result = self.cooldown_service.get_cooldown_expiration(discord_id, action)
        self.assertEqual(result, expiration_time)

    def test_get_cooldown_expiration_none(self):
        """Test getting cooldown expiration when no cooldown exists."""
        discord_id = 123456789
        action = "attack"
        
        result = self.cooldown_service.get_cooldown_expiration(discord_id, action)
        self.assertIsNone(result)

    def test_clear_cooldown(self):
        """Test clearing a cooldown."""
        discord_id = 123456789
        action = "attack"
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        
        self.cooldown_service.set_cooldown(discord_id, action, expiration_time)
        self.assertIn(discord_id, self.cooldown_service.cooldowns[action])
        
        self.cooldown_service.clear_cooldown(discord_id, action)
        self.assertNotIn(discord_id, self.cooldown_service.cooldowns[action])

    def test_clear_cooldown_nonexistent(self):
        """Test clearing a cooldown that doesn't exist."""
        discord_id = 123456789
        action = "attack"
        
        # Should not raise an exception
        self.cooldown_service.clear_cooldown(discord_id, action)

    def test_multiple_users_cooldowns(self):
        """Test that cooldowns work correctly with multiple users."""
        user1 = 123456789
        user2 = 987654321
        action = "cast_spell"
        expiration1 = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        expiration2 = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
        
        self.cooldown_service.set_cooldown(user1, action, expiration1)
        self.cooldown_service.set_cooldown(user2, action, expiration2)
        
        self.assertTrue(self.cooldown_service.is_on_cooldown(user1, action))
        self.assertTrue(self.cooldown_service.is_on_cooldown(user2, action))
        self.assertEqual(len(self.cooldown_service.cooldowns[action]), 2)

    def test_different_actions(self):
        """Test that different actions have separate cooldowns."""
        discord_id = 123456789
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        
        self.cooldown_service.set_cooldown(discord_id, "attack", expiration)
        self.cooldown_service.set_cooldown(discord_id, "cast_spell", expiration)
        
        self.assertTrue(self.cooldown_service.is_on_cooldown(discord_id, "attack"))
        self.assertTrue(self.cooldown_service.is_on_cooldown(discord_id, "cast_spell"))

    def test_get_cooldown_stats(self):
        """Test getting cooldown statistics."""
        discord_id = 123456789
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        
        self.cooldown_service.set_cooldown(discord_id, "attack", expiration)
        self.cooldown_service.set_cooldown(discord_id, "cast_spell", expiration)
        
        stats = self.cooldown_service.get_cooldown_stats()
        
        self.assertIn("attack_cooldowns", stats)
        self.assertIn("cast_spell_cooldowns", stats)
        self.assertIn("total_cooldowns", stats)
        self.assertEqual(stats["attack_cooldowns"], 1)
        self.assertEqual(stats["cast_spell_cooldowns"], 1)
        self.assertEqual(stats["total_cooldowns"], 2)

    def test_invalid_action(self):
        """Test that invalid actions raise appropriate errors."""
        discord_id = 123456789
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        
        # These should not raise exceptions but should not work as expected
        with self.assertRaises(KeyError):
            self.cooldown_service.set_cooldown(discord_id, "invalid_action", expiration)


if __name__ == "__main__":
    unittest.main() 
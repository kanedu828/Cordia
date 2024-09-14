import unittest
import re
from cordia.model.monster import Monster, MonsterType
from cordia.data.monsters import monster_data  # Existing regular monster data
from cordia.data.bosses import boss_data  # Importing the boss data for testing
from cordia.data.gear import gear_data  # For gear_loot validation
from cordia.data.shop_items import shop_item_data
from cordia.data.items import item_data
from cordia.model.shop_item import ShopItemType


class TestShopItemData(unittest.TestCase):

    def test_item_is_valid(self):
        """Test that item key is valid"""
        for shop_item_key, shop_item in shop_item_data.items():
            with self.subTest(monster=shop_item_key):
                if shop_item.type == ShopItemType.GEAR:
                    self.assertIn(shop_item_key, gear_data)
                else:
                    self.assertIn(shop_item_key, item_data)

    def test_item_cost_is_valid(self):
        """Test that item cost item is valid."""
        for shop_item_key, shop_item in shop_item_data.items():
            with self.subTest(monster=shop_item_key):
                self.assertIn(shop_item.item_cost[0], item_data)

    def test_key_matches_item_name(self):
        """Test key matches item name"""
        for shop_item_key, shop_item in shop_item_data.items():
            with self.subTest(monster=shop_item_key):
                self.assertEqual(shop_item.item_name, shop_item_key)


if __name__ == "__main__":
    unittest.main()
